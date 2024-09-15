docker-repo := "192.168.1.101:5000"
image-name := "chumlee-bot"
image-tag := "latest"

run:
	poetry run python src/bot.py

build-production:
	docker build --platform linux/arm64 -t {{docker-repo}}/{{image-name}}:{{image-tag}} .

publish: build-production
	docker push {{docker-repo}}/{{image-name}}:{{image-tag}}
