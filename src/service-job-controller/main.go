package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"os"
	"sync"
	"time"

	pb "./genproto"
	"./job"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
)

// var serverAddr = flag.String("server_addr", "localhost:8989", "The server address in the format of host:port")

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

func extractorExecutesJob(jobs map[int]*job.ExtractionJob, id int, extractorAPI string) {
	baseURL, err := url.Parse(extractorAPI)
	if err != nil {
		log.Fatalln("Malformed URL: ", err.Error())
	}

	params := url.Values{}
	params.Add("name", jobs[id].Name)
	baseURL.RawQuery = params.Encode()

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

func processJobs(jobs map[int]*job.ExtractionJob, jobsPending *[]int, extractorAPI string) {
	for {
		if len(*jobsPending) == 0 {
			time.Sleep(5 * time.Second)
			continue
		}
		id := (*jobsPending)[0]
		extractorExecutesJob(jobs, id, extractorAPI)
		*jobsPending = (*jobsPending)[1:]
	}
}

func main() {
	conn, err := grpc.Dial(":8989", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("%s\n", err)
	}
	defer conn.Close()

	client := pb.NewExtractorServiceClient(conn)
	show, err := client.InitiateExtraction(context.Background(), &pb.ExtractionRequest{ItemName: "Chernobyl"})
	if err != nil {
		log.Fatalln("Error in getting show", err)
	}
	log.Println(show)
	os.Exit(0)

	var wg sync.WaitGroup
	wg.Add(1)

	if err := godotenv.Load("dev.env"); err != nil {
		log.Fatal("Error loading .env file")
	}
	port := os.Getenv("PORT")
	extractorAPI := os.Getenv("EXTRACTOR_API")

	jobs := make(map[int]*job.ExtractionJob)
	var jobsPending []int

	in := make(chan interface{})
	out := make(chan *job.ExtractionJob)

	go func() {
		go receiveJobs(jobs, &jobsPending, out)
		go sendJob(jobs, in)
		go processJobs(jobs, &jobsPending, extractorAPI)
		router(in, out, port)
		wg.Done()
	}()

	wg.Wait()
}
