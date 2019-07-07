APP_NAME = "SITE ANALYZER"

run:
	@echo "==================== BUILD AND START $(APP_NAME) ====================="
	docker-compose up --build

run-demo:
	@echo "============ BUILD, START $(APP_NAME), AND LOAD SAMPLE DATA ============"
	docker-compose up --build; chmod +x demo.sh; ./demo.sh