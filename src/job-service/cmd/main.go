package main

import (
	"fmt"
	"log"
	"net"
	"os"
	"sync"

	pb "../genproto"
	server "../server"

	"github.com/joho/godotenv"
	"google.golang.org/grpc"
)

var (
	envFpath           = "dev.env"
	portEnvKey         = "PORT"
	extractorAPIEnvKey = "EXTRACTOR_API"
)

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
	pb.RegisterJobServiceServer(grpcServer, &server.JobServer{
		JobsMap:     make(map[int64]*pb.Job),
		PendingJobs: make([]int64, 10),
		Mu:          &sync.Mutex{},
		Ec:          ec,
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
