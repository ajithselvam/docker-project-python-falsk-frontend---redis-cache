from flask import Flask
import redis
import os

app = Flask(__name__)

# Connect to Redis container
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    # Increment visit count
    visits = cache.incr('visits')
    return f'Hello! This page has been visited {visits} times.\n'

@app.route('/health')
def health():
    try:
        cache.ping()
        return {'status': 'healthy', 'redis': 'connected'}, 200
    except:
        return {'status': 'unhealthy', 'redis': 'disconnected'}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
