package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"sync"
	"time"

	"./job"
)

func router(in chan interface{}, out chan *job.ExtractionJob) {
	r := job.Routes(in, out)

	var PORT = 3777
	fmt.Printf("Router running on port %d\n", PORT)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", PORT), r))
}

func receiveJobs(jobs map[int]*job.ExtractionJob, jobsPending *[]int, out chan *job.ExtractionJob) {
	for job := range out {
		jobs[job.ID] = job
		*jobsPending = append(*jobsPending, job.ID)
		fmt.Println(*job)
	}
}

func sendJob(jobs map[int]*job.ExtractionJob, in chan interface{}) {
	for input := range in {
		id, ok := input.(int)
		if !ok {
			in <- -2
			continue
		}
		if job, found := jobs[id]; found {
			in <- job
			continue
		}
		in <- -1
	}
}

func extractorExecutesJob(jobs map[int]*job.ExtractionJob, id int) {
	baseURL, err := url.Parse("http://127.0.0.1:5000/")
	if err != nil {
		log.Fatalln("Malformed URL: ", err.Error())
	}

	params := url.Values{}
	params.Add("name", jobs[id].Name)
	baseURL.RawQuery = params.Encode()

	fmt.Printf("Encoded URL is %q\n", baseURL.String())

	resp, err := http.Post(baseURL.String(), "", nil)
	if err != nil {
		fmt.Println("Resp err")
		log.Fatalln(err)
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
		jobs[id].Status = job.CompletedFailed
		return
	}
	log.Println(string(body))
	jobs[id].Status = job.CompletedSucceeded
}

func processJobs(jobs map[int]*job.ExtractionJob, jobsPending *[]int) {
	for true {
		if len(*jobsPending) == 0 {
			time.Sleep(5 * time.Second)
			continue
		}
		id := (*jobsPending)[0]
		extractorExecutesJob(jobs, id)
		*jobsPending = (*jobsPending)[1:]
	}
}

func main() {
	var wg sync.WaitGroup
	wg.Add(1)

	jobs := make(map[int]*job.ExtractionJob)
	var jobsPending []int

	in := make(chan interface{})
	out := make(chan *job.ExtractionJob)

	go func() {
		go receiveJobs(jobs, &jobsPending, out)
		go sendJob(jobs, in)
		go processJobs(jobs, &jobsPending)
		router(in, out)
		wg.Done()
	}()

	wg.Wait()
}
