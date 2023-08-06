.PHONY:all flake8 check-black black test lint-dockerfile
all: flake8 check-black test lint-dockerfile

flake8:
	flake8 .

check-black:
	black --check .

black:
	black .

test:
	pytest --cov=tuxbuild .

lint-dockerfile:
	docker run --rm -i hadolint/hadolint < Dockerfile
