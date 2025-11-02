"""Simple RQ worker runner for DevArena.

Run this with: python3 backend/worker.py
or use `rq worker` directly after installing RQ.
"""
from redis import StrictRedis
from rq import Worker, Queue, Connection

listen = ['grading']

redis_conn = StrictRedis(host='localhost', port=6379, decode_responses=True)

if __name__ == '__main__':
    with Connection(redis_conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
