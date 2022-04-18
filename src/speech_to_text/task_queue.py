# CREDIT: https://github.com/1xch/flask-celery-example/blob/master/app.py

from os import environ
# from flask import Flask, jsonify, request

from src.speech_to_text.make_celery import make_celery

# flask_app = Flask(__name__)
# flask_app.config.update(
#     CELERY_BROKER_URL='amqp://localhost', # guest:guest@localhost:5672/myvhost
#     CELERY_RESULT_BACKEND='rpc://localhost',
# )

# app = make_celery(flask_app)

app = make_celery()

@app.task
def process(x):
    return x + 2

# @flask_app.route("/test")
# def hello_world(x=16):
#     x = int(request.args.get("x", x))
#     res = add.delay(x)

#     result = f"convert({x})"
#     goto = f"{res.task_id}"
#     return jsonify(result=result, goto=goto)

# @flask_app.route("/test/<task_id>")
# def show_result(task_id):
#     retval = add.AsyncResult(task_id).get(timeout=1.0)
#     return repr(retval)


# if __name__ == "__main__":
    # port = int(environ.get("PORT", 5000))
    # flask_app.run(host='0.0.0.0', port=port, debug=True)