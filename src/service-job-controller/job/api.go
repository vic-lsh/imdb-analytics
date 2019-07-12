package job

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"math/rand"
	"net/http"
	"strconv"
	"sync"

	pb "../genproto"
	"github.com/gorilla/mux"
)

type jobService struct {
	jobs map[int]*pb.Job
	mu   sync.Mutex
}

func (js *jobService) CreateJob(ctx context.Context, req *pb.CreateJobRequest) (*pb.CreateJobResponse, error) {
	return &pb.CreateJobResponse{Successful: true}, nil
}

func (js *jobService) GetJob(ctx context.Context, req *pb.GetJobRequest) (*pb.Job, error) {
	return &pb.Job{}, nil
}

func (js *jobService) DeleteJob(ctx context.Context, req *pb.DeleteJobRequest) (*pb.Empty, error) {
	return &pb.Empty{}, nil
}

// Handler encapsulates input and output channels for TVJob
type Handler struct {
	in  chan interface{}
	out chan<- *ExtractionJob
}

// Routes return a router with routes associated with TVSeriesExtractionJobs
func Routes(in chan interface{}, out chan<- *ExtractionJob) *mux.Router {
	r := mux.NewRouter()
	h := &Handler{in: in, out: out}
	r.HandleFunc("/", h.homeHandler)
	r.HandleFunc("/jobs/{id}", h.getJob).Methods("GET")
	r.HandleFunc("/jobs", h.postJob).Methods("POST")

	r.Use(loggingMiddleware)

	return r
}

// homeHandler responds a helper message that directs client to use
// the actual API at `/jobs`.
func (h *Handler) homeHandler(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(&map[string]interface{}{
		"Message": "This is the home route of the extractor service API. " +
			"To make RESTful calls visit `/jobs.`",
	})
}

// getJob handles querying job with a specific ID.
func (h *Handler) getJob(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	params := mux.Vars(r)
	id, err := strconv.Atoi(params["id"])
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(&map[string]interface{}{
			"Message": fmt.Sprintf("Job number must be a number."),
		})
		return
	}

	h.in <- id
	var out interface{} = <-h.in

	switch resp := out.(type) {

	case *ExtractionJob:
		json.NewEncoder(w).Encode(resp.marshall())

	case InChanError:
		switch resp {
		case ErrorJobNotFound:
			w.WriteHeader(http.StatusNotFound)
			json.NewEncoder(w).Encode(&map[string]interface{}{
				"Message": fmt.Sprintf("Job %d does not exist.", id),
			})

		case ErrorInternalError:
			w.WriteHeader(http.StatusInternalServerError)
			json.NewEncoder(w).Encode(&map[string]interface{}{
				"Message": fmt.Sprintf("An error has occured decoding your request."),
			})
		}

	default:
		w.WriteHeader(http.StatusNotFound)
		json.NewEncoder(w).Encode(&map[string]interface{}{
			"Message": "No job exists yet.",
		})
	}
}

// postJob creates a new job.
func (h *Handler) postJob(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	name, ok := r.URL.Query()["name"]
	if !ok {
		w.WriteHeader(http.StatusBadRequest)
		json.NewEncoder(w).Encode(&map[string]interface{}{
			"Message": "`name` is a required query.",
		})
		return
	}

	j := ExtractionJob{
		ID:     rand.Intn(1000000000),
		Name:   name[0],
		Status: NotProcessed,
	}

	h.out <- &j
	w.WriteHeader(http.StatusAccepted)
	json.NewEncoder(w).Encode(j.marshall())
}

func loggingMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Println(r.Method, r.RequestURI)
		next.ServeHTTP(w, r)
	})
}
