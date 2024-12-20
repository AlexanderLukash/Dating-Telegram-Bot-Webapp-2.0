DC = docker compose -p dating-bot
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose/app.yaml
FRONT_FILE = docker_compose/frontend.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = api


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: all
all:
	${DC} -f ${STORAGES_FILE} -f ${FRONT_FILE} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-logs
app-logs:
	${LOGS} -f ${APP_CONTAINER} -f

.PHONY: frontend
frontend:
	${DC} -f ${FRONT_FILE} ${ENV} up --build -d

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest
