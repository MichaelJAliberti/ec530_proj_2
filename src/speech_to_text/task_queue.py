# CREDIT: https://github.com/1xch/flask-celery-example/blob/master/app.py

from os import environ
from flask import Flask, jsonify, request
from celery import Celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://', # guest:guest@localhost:5672/myvhost
    CELERY_RESULT_BACKEND='rpc://',
)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task(name="tasks.add")
def add(x):
    return x * 2

@app.route("/test")
def hello_world(x=16):
    x = int(request.args.get("x", x))
    res = add.AsyncResult(x)

    result = f"convert({x})"
    goto = f"{res.task_id}"
    return jsonify(result=result, goto=goto)

@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=1.0)
    return repr(retval)


if __name__ == "__main__":
    port = int(environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)