SERVICE_NAME = JobService
LANG = go

run:
	go build -o bin/exec .;./bin/exec

.PHONY: genproto
genproto:
	@echo "============ Generating protos for $(SERVICE_NAME):$(LANG) =============="
	protoc -I ../../pb ../../pb/imdb.proto --go_out==plugins=grpc:genproto