init:
	npm install

run:
	npm start

docker-deploy:
	docker build -f dockerfile.prod -t vicleelsh/imdbapp-web .;	\
	docker push vicleelsh/imdbapp-web
