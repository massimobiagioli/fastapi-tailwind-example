.PHONY: help run

help:
	@echo "Available commands:"
	@echo "  run  : Launch the server with uvicorn"

run:
	python -m uvicorn app.main:app --reload 