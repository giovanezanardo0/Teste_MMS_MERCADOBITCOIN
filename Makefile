export PYTHONPATH=$(shell pwd)/src/

run:
	@uvicorn src.main:app --reload

load-data:
	@python src/mms.py

requirements:
	@pip install -r requirements.txt

test:
	@pytest -c ./tests/pytest.ini  ./tests/

clean:
	@del /s __pycache__ .pytest_cache