import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'k8s_notification.settings')

app = Celery('resources')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# @app.task(bind=True, retry_limit=4, default_retry_delay=10)
# def k8s_notification():
#     """
#      This is a celery task. Just a normal function with task decorator.
#      Note that we use the decorator from a celery insance.
#     """
#     # print('Serving {} of {} beer!'.format(size, _type))
#     print("""
#           ------------------------------------------------
#                    .   *   ..  . *  *
#                  *  * @()Ooc()*   o  .
#                      (Q@*0CG*O()  ___
#                     |\_________/|/ _ \
#                     |  |  |  |  | / | |
#                     |  |  |  |  | | | |
#                     |  |  |  |  | | | |
#                     |  |  |  |  | | | |
#                     |  |  |  |  | | | |
#                     |  |  |  |  | \_| |
#                     |  |  |  |  |\___/
#                     |\_|__|__|_/|
#                      \_________/
#           ------------------------------------------------
#           """)


