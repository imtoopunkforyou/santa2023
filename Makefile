# To use you need to enter `make <command>`

# =============
# configuration
# =============
.PHONY: make
make:
	cat ./Makefile
# ======
# docker
# ======
.PHONY: up
up:
	docker build . --tag santa && docker run -d --expose 8888 --env-file .env --name santa2023 santa
.PHONY: down
down:
	docker stop santa2023 && docker rm santa2023
# ============
# dev commands
# ============
.PHONY: pre-commit
pre-commit:
	isort --sp setup.cfg ./ && \
	flake8 ./
