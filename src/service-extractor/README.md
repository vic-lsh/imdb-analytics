# Extractor service

The extractor service extracts information from IMDb, given a title. 

## Design decisions

The service is intentionally kept to a simple request-response model: it simply returns scraped IMDb data given the title, or error message(s) if the extraction failed. 

The service should not care about "stateful information", such as the number of pending extraction jobs, or the minimum time intervals between extraction jobs such that we're not harassing the end server. Such logic should be handled by services utilizing the Extractor Service: it is the caller's responsibility to keep track of pending jobs, how frequently should an extractor be called, etc.

It is best to think of the Extractor Service as anonymous workers: they receive jobs (a show's name), perform the job, and terminate. The service is intended to be lightweight (little start-up and teardown overhead), performant (fast execution), and resilient (provide useful feedback messages if an extraction job fails).

## APIs overview

Extracting information from IMDb is as simple as:

```python
mgr = IMDb_Queries_Manager(ExtractorConfig())
mgr.add_query("Game of Thrones")    # add a single query
mgr.add_multiple_queries(["Friends", "Chernobyl", "Breaking Bad"])      # or, multiple queries
success = mgr.execute()
```

Extraction is also available through remote procedure calls (RPC). For instance, in `golang`, you may initiate an extraction like so:

```go
// Assuming .proto files are set up, and `extractorAPI` is defined...

// Establish ExtractorAPI connection
conn, err := grpc.Dial(extractorAPI, grpc.WithInsecure())
if err != nil {
    log.Fatalf("%s\n", err)
}
defer conn.Close()
ec := pb.NewExtractorServiceClient(conn)

// Perform extraction. `InitiateExtraction` is an RPC call.
show, err := ec.InitiateExtraction(context.Background(), 
    &pb.ExtractionRequest{
        ItemName: "Game of Thrones"
    }
)

if err != nil {
    log.Fatalln("Error in getting show", err)
}
log.Println(show)
```

RPC is implemented using the [gRPC](https://grpc.io) framework. 
