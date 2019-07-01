package main

import (
	"fmt"
	"log"
	"net/http"
	"sync"

	"github.com/vic-lee/site-analyzer/src/service-extractor/api/job"
)

func router(in chan interface{}, out chan job.TVSeriesExtractionJob) {
	r := job.Routes(in, out)

	var PORT = 4000
	fmt.Printf("Router running on port %d\n", PORT)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", PORT), r))
}

func receiveJobs(jobs map[int]job.TVSeriesExtractionJob, out chan job.TVSeriesExtractionJob) {
	for job := range out {
		jobs[job.ID] = job
		fmt.Println(jobs)
	}
}

func sendJob(jobs map[int]job.TVSeriesExtractionJob, in chan interface{}) {
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

func main() {
	var wg sync.WaitGroup
	wg.Add(1)

	jobs := make(map[int]job.TVSeriesExtractionJob)

	in := make(chan interface{})
	out := make(chan job.TVSeriesExtractionJob)

	go func() {
		go receiveJobs(jobs, out)
		go sendJob(jobs, in)
		router(in, out)
		wg.Done()
	}()

	wg.Wait()
}
