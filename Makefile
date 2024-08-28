run:
	python3 bot.py

build:
	docker build --platform linux/arm64 -t 192.168.1.101:5000/chumlee-bot .

push:
	docker push 192.168.1.101:5000/chumlee-bot
