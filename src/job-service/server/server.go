package server

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"strings"
	"sync"
	"time"

	pb "../genproto"

	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

// JobServer handles job-related API calls
type JobServer struct {
	JobsMap         map[int64]*pb.Job
	JobsNameToIDMap map[string]int64
	PendingJobs     []int64
	Mu              *sync.Mutex
	Ec              pb.ExtractorServiceClient
}

// CreateJob stores a new Job instance in JobServer, and enqueues the new job to the pendings list.
// If a Job with the same TargetName is found, that job is returned instead (no job will be created).
// Client can query that Job using its JobID, or delete this Job so that a new Job can be created.
func (s *JobServer) CreateJob(ctx context.Context, req *pb.CreateJobRequest) (*pb.CreateJobResponse, error) {
	reqName := fmt.Sprint(strings.ToLower(req.TargetName))

	if existingJID, ok := s.JobsNameToIDMap[reqName]; ok {
		jobFound := s.JobsMap[existingJID]
		log.Printf("Found Job '%d' with matching target name '%s': {%+v}\n", existingJID, jobFound.TargetName, jobFound)
		return &pb.CreateJobResponse{Created: false, Job: jobFound}, nil
	}

	jid := rand.Int63()
	jobCreated := &pb.Job{Id: jid, TargetName: req.TargetName, Status: pb.Job_NOT_PROCESSED}

	s.JobsMap[jid] = jobCreated
	s.JobsNameToIDMap[reqName] = jid
	s.PendingJobs = append(s.PendingJobs, jid)

	log.Printf("Job '%d' created: {%+v}\n", jid, jobCreated)
	return &pb.CreateJobResponse{Created: true, Job: jobCreated}, nil
}

// GetJob returns a Job instance if found, or an NotFound error if not found
func (s *JobServer) GetJob(ctx context.Context, req *pb.GetJobRequest) (*pb.Job, error) {
	if job, ok := s.JobsMap[req.Id]; ok {
		log.Printf("Job '%d' found, returning job {%+v}\n", job.Id, job)
		return job, nil
	}
	return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Job with ID '%d' not found.", req.Id))
}

// GetJobStatus returns the Status of the queried job, if found, or an NotFound error if not found
func (s *JobServer) GetJobStatus(ctx context.Context, req *pb.GetJobRequest) (*pb.JobStatusQueryResponse, error) {
	if job, ok := s.JobsMap[req.Id]; ok {
		return &pb.JobStatusQueryResponse{
			Status:    job.Status,
			StatusMsg: mapJobStatusToMsg(job.Status),
		}, nil
	}
	return nil, status.Errorf(codes.NotFound, fmt.Sprintf("Job with ID '%d' not found.", req.Id))
}

// DeleteJob deletes a job if found; it returns true if a job is found and deleted, otherwise false
func (s *JobServer) DeleteJob(ctx context.Context, req *pb.DeleteJobRequest) (*pb.DeleteJobResponse, error) {
	_, ok := s.JobsMap[req.Id]
	if ok {
		s.Mu.Lock()
		defer s.Mu.Unlock()

		jobToBeDeleted := s.JobsMap[req.Id]
		delete(s.JobsMap, req.Id)

		k := targetNameToMapKey(jobToBeDeleted.TargetName)
		if _, ok := s.JobsNameToIDMap[k]; ok {
			delete(s.JobsNameToIDMap, k)
		}
	}
	return &pb.DeleteJobResponse{Successful: ok}, nil
}

func targetNameToMapKey(targetName string) string {
	return fmt.Sprint(strings.ToLower(targetName))
}

// ProcessJobs pops Jobs from the waiting queue, calls ExtractorService to perform job,
// and updates the jobs' status based on whether the extraction ended successfully
func (s *JobServer) ProcessJobs() {
	for {
		if len(s.PendingJobs) <= 0 {
			time.Sleep(10 * time.Second)
			continue
		}
		if jid, ok := s.popJob(); ok {
			job := s.JobsMap[jid]
			log.Printf("Going to process job '%d': {%+v}\n", jid, job)
			_, err := s.Ec.InitiateExtraction(context.Background(),
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

func (s *JobServer) popJob() (int64, bool) {
	log.Printf("len of pending jobs: %d", len(s.PendingJobs))
	s.Mu.Lock()
	defer s.Mu.Unlock()
	for {
		if len(s.PendingJobs) > 0 {
			ret := s.PendingJobs[0]
			s.PendingJobs = s.PendingJobs[1:]
			// It is possible a JobID exists in the PendingList, but not in the JobsMap.
			// When performing Job deletion, the PendingList is not updated to remove Jobs
			// that no longer exist. The function continues to find a pending JobID that
			// exists in the JobsMap, or until there is no pending jobs left. 
			if _, ok := s.JobsMap[ret]; !ok {
				continue
			}
			return ret, true
		}
		return -1, false
	}
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
