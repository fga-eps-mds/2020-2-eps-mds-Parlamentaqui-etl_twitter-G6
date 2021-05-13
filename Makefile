start-dev:
	docker-compose up

start-prod:
	docker-compose up --build --detach 

rebuild:
		docker-compose up --build

test:
	sudo docker-compose run prlmntq_etl_twitter python  src/test.py
