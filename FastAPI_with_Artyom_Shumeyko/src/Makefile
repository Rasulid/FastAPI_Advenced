run:
	uvicorn main:app --reload

worker:tasks
	celery -A tasks.tasks:celery worker --loglevel=INFO

redis_cli:
	redis-cli

flower:tasks
	celery -A tasks.tasks:celery flower --loglevel=INFO

venv:
	 source /home/rasulabduvaitov/Desktop/learning/FastAPI_with_Artyom_Shumeyko/venv/bin/activate