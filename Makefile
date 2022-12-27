init:
	mkdir data
	mkdir logs
	mkdir attachments
	cp .env.example .env

up:
	docker-compose up -d
	pip3 install -r requirements.txt

down:
	docker-compose down

run:
	python3 main.py


