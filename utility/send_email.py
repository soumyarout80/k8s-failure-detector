from django.conf import settings
from django.core.mail import send_mail


class EmailNotification(object):
    def __init__(self, email_id, metrics, message):
        self.subject = '!!Alert Kubernetes {metrics}'.format(metrics=metrics)
        self.user_name = email_id.split("@")[0]
        self.message = message
        self.email_from = settings.EMAIL_HOST_USER
        self.recipient_list = [email_id]

    def send(self):
        print("**************", self.user_name)
        return send_mail(self.subject, self.template(), self.email_from, self.recipient_list)

    def template(self):
        return "Hello {name}, \n\n{site_name}".format(name=self.user_name, site_name=self.message)
