SERVICE_NAME = JobService
LANG = go
IDENTIFIER = $(SERVICE_NAME):$(LANG)

run:
	@echo "============ Build and run $(IDENTIFIER) =============="
	go build -o bin/exec .;./bin/exec

.PHONY: genproto
genproto:
	@echo "============ Generating protos for $(IDENTIFIER) =============="
	protoc -I ../../pb ../../pb/imdb.proto --go_out==plugins=grpc:genproto