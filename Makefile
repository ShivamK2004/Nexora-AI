.PHONY: install run test docker
install:
	python -m pip install -r requirements.txt
run:
	uvicorn backend.app.main:app --reload
test:
	python -m unittest discover -s tests -v
docker:
	docker compose up --build
