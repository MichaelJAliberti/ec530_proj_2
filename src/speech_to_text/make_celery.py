from ast import arg
from celery import Celery

def make_celery(*args):
    if args:
        app = args[0]

        celery = Celery(
            app.import_name,
            broker=app.config['CELERY_BROKER_URL'],
            backend=app.config['CELERY_RESULT_BACKEND']
        )
        class ContextTask(celery.Task):
            abstract = True
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        
        celery.Task = ContextTask
    else:
        celery = Celery(
            "tasks",
            broker='amqp://user:password@localhost/vhost',
            backend='amqp://'
        )

    return celery