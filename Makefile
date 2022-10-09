run:
	python3 bot.py

build:
	docker build -t 192.168.1.100:5050/chumlee-bot .

push:
	docker push 192.168.1.100:5050/chumlee-bot
