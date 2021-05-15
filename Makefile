start-dev:
	docker-compose up

start-prod:
	docker-compose up --build --detach 

rebuild:
		docker-compose up --build

test:
	sudo docker run prlmntq_etl_twitter sh -c 'python3  src/test.py'
