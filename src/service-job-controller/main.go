package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	pb "./genproto"
	"./job"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
)

var (
	envFpath           = "dev.env"
	portEnvKey         = "PORT"
	extractorAPIEnvKey = "EXTRACTOR_API"
)

func router(in chan interface{}, out chan *job.ExtractionJob, port string) {
	r := job.Routes(in, out)

	fmt.Printf("Router running on port %s\n", port)
	log.Fatal(http.ListenAndServe(fmt.Sprintf("0.0.0.0:%s", port), r))
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
			in <- job.ErrorInternalError
			continue
		}
		if j, found := jobs[id]; found {
			in <- j
			continue
		}
		in <- job.ErrorJobNotFound
	}
}

func extractorExecutesJob(jobs map[int]*job.ExtractionJob, id int, ec pb.ExtractorServiceClient) {
	show, err := ec.InitiateExtraction(context.Background(), &pb.ExtractionRequest{ItemName: jobs[id].Name})
	if err != nil {
		log.Fatalln("Error in getting show", err)
	}
	log.Println(show)
	jobs[id].Status = job.CompletedSucceeded
}

func processJobs(jobs map[int]*job.ExtractionJob, jobsPending *[]int, ec pb.ExtractorServiceClient) {
	for {
		if len(*jobsPending) == 0 {
			time.Sleep(5 * time.Second)
			continue
		}
		id := (*jobsPending)[0]
		extractorExecutesJob(jobs, id, ec)
		*jobsPending = (*jobsPending)[1:]
	}
}

func mustHaveEnv(key string) (val string) {
	val, exists := os.LookupEnv(key)
	if !exists {
		log.Fatalf("`%s` should be assigned by an environment variable. Exiting...\n", key)
	}
	return val
}

func main() {
	if err := godotenv.Load(envFpath); err != nil {
		log.Fatalln("Error loading .env file")
	}

	port := mustHaveEnv(portEnvKey)
	extractorAPI := mustHaveEnv(extractorAPIEnvKey)

	conn, err := grpc.Dial(extractorAPI, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("%s\n", err)
	}
	defer conn.Close()
	extractorClient := pb.NewExtractorServiceClient(conn)

	var wg sync.WaitGroup
	wg.Add(1)

	jobs := make(map[int]*job.ExtractionJob)
	var jobsPending []int

	in := make(chan interface{})
	out := make(chan *job.ExtractionJob)

	go func() {
		go receiveJobs(jobs, &jobsPending, out)
		go sendJob(jobs, in)
		go processJobs(jobs, &jobsPending, extractorClient)
		router(in, out, port)
		wg.Done()
	}()

	wg.Wait()
}
