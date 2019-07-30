package main

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"net"
	"os"
	"sync"
	"time"

	pb "./genproto"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

var (
	envFpath           = "dev.env"
	portEnvKey         = "PORT"
	extractorAPIEnvKey = "EXTRACTOR_API"
)

type jobServer struct {
	jobsMap     map[int64]*pb.Job
	pendingJobs []int64
	mu          *sync.Mutex
	ec          pb.ExtractorServiceClient
}

// CreateJob stores a new Job instance in jobServer, and enqueues the new job to the pendings list
func (s *jobServer) CreateJob(ctx context.Context, req *pb.CreateJobRequest) (*pb.CreateJobResponse, error) {
	jid := rand.Int63()
	jobCreated := &pb.Job{Id: jid, TargetName: req.TargetName, Status: pb.Job_NOT_PROCESSED}
	s.jobsMap[jid] = jobCreated
	s.pendingJobs = append(s.pendingJobs, jid)
	return &pb.CreateJobResponse{Successful: true, Job: jobCreated}, nil
}

func (s *jobServer) GetJob(ctx context.Context, req *pb.GetJobRequest) (*pb.Job, error) {
	if job, ok := s.jobsMap[req.Id]; ok {
		return job, nil
	}
	return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Job with ID '%d' not found.", req.Id))
}

func (s *jobServer) GetJobStatus(ctx context.Context, req *pb.GetJobRequest) (*pb.JobStatusQueryResponse, error) {
	if job, ok := s.jobsMap[req.Id]; ok {
		return &pb.JobStatusQueryResponse{
			Status:    job.Status,
			StatusMsg: mapJobStatusToMsg(job.Status),
		}, nil
	}
	return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Job with ID '%d' not found.", req.Id))
}

func (s *jobServer) DeleteJob(ctx context.Context, req *pb.DeleteJobRequest) (*pb.DeleteJobResponse, error) {
	_, ok := s.jobsMap[req.Id]
	if ok {
		delete(s.jobsMap, req.Id)
	}
	return &pb.DeleteJobResponse{Successful: ok}, nil
}

// processJobs pops Jobs from the waiting queue, calls ExtractorService to perform job,
// and updates the jobs' status based on whether the extraction ended successfully
func (s *jobServer) processJobs() {
	for {
		if len(s.pendingJobs) < 0 {
			time.Sleep(10 * time.Second)
			continue
		}
		if jid, ok := s.popJob(); ok {
			job := s.jobsMap[jid]
			_, err := s.ec.InitiateExtraction(context.Background(),
				&pb.ExtractionRequest{ItemName: job.TargetName})
			if err != nil {
				log.Println("Error in getting show", err)
				job.Status = pb.Job_COMPLETED_FAILURE
			}
			job.Status = pb.Job_COMPLETED_SUCCESS
		} else {
			log.Println("Attempted to pop from pending jobs but there is no pending jobs.")
		}
	}
}

func (s *jobServer) popJob() (int64, bool) {
	if len(s.pendingJobs) > 0 {
		s.mu.Lock()
		defer s.mu.Unlock()
		ret := s.pendingJobs[0]
		s.pendingJobs = s.pendingJobs[1:]
		return ret, true
	}
	return -1, false
}

func mapJobStatusToMsg(status pb.Job_Status) string {
	statusMsgs := map[pb.Job_Status]string{
		pb.Job_NOT_PROCESSED:     "Not Processed",
		pb.Job_PROCESSING:        "Processing",
		pb.Job_COMPLETED_SUCCESS: "Completed Successfully",
		pb.Job_COMPLETED_FAILURE: "Completion failed",
	}
	if msg, ok := statusMsgs[status]; ok {
		return msg
	}
	return fmt.Sprintf("ERR: Job Status Message not found for status '%d'", status)
}

func mustHaveEnv(key string) (val string) {
	val, exists := os.LookupEnv(key)
	if !exists {
		log.Fatalf("`%s` should be assigned by an environment variable. Exiting...\n", key)
	}
	return val
}

func makeExtractorClient(API string) (pb.ExtractorServiceClient, *grpc.ClientConn, error) {
	conn, err := grpc.Dial(API, grpc.WithInsecure())
	if err != nil {
		return nil, nil, err
	}
	extractorClient := pb.NewExtractorServiceClient(conn)
	return extractorClient, conn, nil
}

func makeJobServiceServer(port string, ec pb.ExtractorServiceClient) (*grpc.Server, net.Listener, error) {
	lis, err := net.Listen("tcp", fmt.Sprintf(":%s", port))
	if err != nil {
		return nil, nil, err
	}
	fmt.Printf("Initiating JobService server, listening at port %s\n", port)

	grpcServer := grpc.NewServer()
	pb.RegisterJobServiceServer(grpcServer, &jobServer{
		jobsMap:     make(map[int64]*pb.Job),
		pendingJobs: make([]int64, 10),
		mu:          &sync.Mutex{},
		ec:          ec,
	})
	
	return grpcServer, lis, nil
}

func main() {
	if err := godotenv.Load(envFpath); err != nil {
		log.Fatalln("Error loading .env file")
	}
	port := mustHaveEnv(portEnvKey)
	extractorAPI := mustHaveEnv(extractorAPIEnvKey)

	extractorClient, conn, err := makeExtractorClient(extractorAPI)
	if err != nil {
		log.Fatalf("%s\n", err)
	}
	defer conn.Close()

	server, lis, err := makeJobServiceServer(port, extractorClient)
	if err != nil {
		log.Fatalf("%s\n", err)
	}
	server.Serve(lis)
}
