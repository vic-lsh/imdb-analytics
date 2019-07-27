APP_NAME = "SITE ANALYZER"

run:
	@echo "==================== BUILD AND START $(APP_NAME) ====================="
	docker-compose -f docker-compose-dev.yml up -d --build

run-demo:
	@echo "============ BUILD, START $(APP_NAME), AND LOAD SAMPLE DATA ============"
	docker-compose -f docker-compose-dev.yml up -d --build; chmod +x build/demo.sh; ./build/demo.sh

dev:
	@echo "============ BUILD AND START $(APP_NAME) (DEV MODE) ================="
	docker-compose -f docker-compose-dev.yml up --build

prod:
	@echo "========== BUILD AND START $(APP_NAME) (PRODUCTION MODE) ==============="
	docker-compose -f docker-compose-prod.yml up --build

stop:
	@echo "======================= STOPPING $(APP_NAME) ========================"
	docker-compose stop

remove:
	@echo "======================= REMOVING $(APP_NAME) ========================"
	docker-compose down
