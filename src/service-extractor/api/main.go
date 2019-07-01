package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/vic-lee/site-analyzer/src/service-extractor/api/job"
)

func router(in chan job.TVSeriesExtractionJob, out chan job.TVSeriesExtractionJob) {
	r := job.Routes(in, out)

	var PORT = 4000
	fmt.Printf("Router running on port %d\n", PORT)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", PORT), r))
}

func main() {
	jobs := make(map[int]job.TVSeriesExtractionJob)

	in := make(chan job.TVSeriesExtractionJob)
	out := make(chan job.TVSeriesExtractionJob)

	go router(in, out)

	for job := range out {
		jobs[job.ID] = job
	}
}
