init:
	pip3 install -r requirements.txt

run:
	python3 src/run.py

docker-deploy:
	docker build -f dockerfile.prod -t vicleelsh/imdbapp-extractor-service .; \
	docker push vicleelsh/imdbapp-extractor-service

test:
	py.test tests

proto_dir = ../../pb
proto_fpath = $(proto_dir)/imdb.proto
genproto:
	python3 -m grpc_tools.protoc -I$(proto_dir) --python_out=./src --grpc_python_out=./src $(proto_fpath)
