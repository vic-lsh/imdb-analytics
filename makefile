APP_NAME = "SITE ANALYZER"

run:
	@echo "==================== BUILD AND START $(APP_NAME) ====================="
	docker-compose up -d --build

run-debug:
	@echo "============ BUILD AND START $(APP_NAME) (DEBUG MODE) ================="
	docker-compose up --build

run-demo:
	@echo "============ BUILD, START $(APP_NAME), AND LOAD SAMPLE DATA ============"
	docker-compose up -d --build; chmod +x demo.sh; ./demo.sh

stop:
	@echo "======================= STOPPING $(APP_NAME) ========================"
	docker-compose stop

remove:
	@echo "======================= REMOVING $(APP_NAME) ========================"
	docker-compose down