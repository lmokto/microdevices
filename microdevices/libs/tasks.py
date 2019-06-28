from ..celery import app
from .mock import generate_random


@app.task
def add(x, y):
    return x + y


@app.task
def emit(**kwargs):
    return str(generate_random(10, 20, 1))


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
