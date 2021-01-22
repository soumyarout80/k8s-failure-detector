from utility.upload_config import GetConfigFile
from celery import shared_task
from .models import Account


@shared_task()
def upload_to_db():
    data = GetConfigFile()
    data.get_all_data_from_configfile()
    records = data.get_list_data()
    # db_records = Account.objects.all()
    for record in records:
        obj, created = Account.objects.update_or_create(
            aws_account=record['aws_account'], cluster_name=record['cluster_name'], defaults={
                'email_id': record['email_id'], 'slack_channel': record['slack_channel'], 'notification_state': 'Enable',
                'k8s_endpoint': record['cluster_endpoint'],
            },
        )

        # if Account.objects.filter(account=record['aws_account'], cluster_name=record['cluster_name']).exists():
        #     query_set = Account(account=record['aws_account'], cluster_name=record['cluster_name'],
        #                         email_id=record['email_id'], slack_channel=record['slack_channel'],
        #                         notification_state='Enable', k8s_endpoint=record['cluster_endpoint'],
        #                         )
        #     query_set.save()
