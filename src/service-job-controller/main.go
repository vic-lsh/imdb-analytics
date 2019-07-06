package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	job "./job"
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
	// const pyScriptName = "run.py"
	// const dir = "../extractor"

	// cmd := exec.Command("python3", pyScriptName, jobs[id].Name)
	// cmd.Dir = dir
	// var stderr bytes.Buffer
	// cmd.Stderr = &stderr

	// if err := cmd.Run(); err != nil {
	// 	jobs[id].Status = job.CompletedFailed
	// 	fmt.Printf("Failed posting %s", jobs[id].Name)
	// } else {
	// 	jobs[id].Status = job.CompletedSucceeded
	// 	fmt.Printf("POSTED %s\n", jobs[id].Name)
	// }

	req, err := http.NewRequest("POST", "http://127.0.0.1:5000/", nil)
	if err != nil {
		log.Fatalln(err)
	}

	q := req.URL.Query()
	q.Add("name", jobs[id].Name)
	req.URL.RawQuery = q.Encode()
	fmt.Println(req.URL.String())

	resp, err := http.Post(req.URL.String(), "application/json", nil)
	if err != nil {
		log.Fatalln(err)
	}
	log.Println(resp.Body)
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
