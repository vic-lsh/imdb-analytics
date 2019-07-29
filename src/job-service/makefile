SERVICE_NAME = JobService
LANG = go
IDENTIFIER = $(SERVICE_NAME):$(LANG)

run:
	@echo "============ Build and run $(IDENTIFIER) =============="
	go build -o bin/exec .;./bin/exec

build:
	@echo "=============== Build $(IDENTIFIER) ================="
	go build -o bin/exec .

docker-deploy:
	docker build -f dockerfile.prod -t vicleelsh/imdbapp-job-service .;	\
	docker push vicleelsh/imdbapp-job-service

test:
	go test ./...

.PHONY: genproto
genproto:
	@echo "============ Generating protos for $(IDENTIFIER) =============="
	protoc -I ../../pb --go_out=plugins=grpc:genproto ../../pb/imdb.proto