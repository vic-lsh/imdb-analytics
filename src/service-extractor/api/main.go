package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/vic-lee/site-analyzer/src/service-extractor/api/job"
)

func main() {
	r := job.Routes()

	var PORT = 4000
	fmt.Printf("Router running on port %d\n", PORT)
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", PORT), r))
}
