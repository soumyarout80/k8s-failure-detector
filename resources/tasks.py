from celery import shared_task
from .models import Resource
from .models import Account
from .models import Alert
from utility.upload_config import GetConfigFile
from utility.send_email import EmailNotification
from django.utils import timezone
import requests
import time
import concurrent.futures
from billiard.pool import Pool


def get_node_info_from_k8s(data):
    aws_account = data['aws_account']
    cluster_name = data['cluster_name']
    cluster_end_point = data['k8s_endpoint'] + "api/v1/nodes"
    raw_data = requests.get(cluster_end_point)
    raw_data = raw_data.json()
    for i in raw_data['items']:
        for j in i['status']['conditions']:
            uid = i['metadata']['uid']
            metrics = j['type']
            resource_type = 'Node'
            resource_status = j['status']
            alert_message = j['message']
            resource_name = i['metadata']['name']

            if metrics != 'Ready':
                obj, created = Resource.objects.update_or_create(aws_account=aws_account,
                                                                 cluster_name=cluster_name,
                                                                 uid=uid, account_id=data['id'],
                                                                 metrics=metrics, resource_type=resource_type,
                                                                 resource_name=resource_name,
                                                                 defaults={'status': resource_status,
                                                                           'status_message': alert_message,
                                                                           'last_updated': timezone.now(),
                                                                           },
                                                                 )

    cluster_end_point = data['k8s_endpoint'] + "api/v1/pods"
    raw_data = requests.get(cluster_end_point)
    raw_data = raw_data.json()
    for i in raw_data['items']:
        for j in i['status']['containerStatuses']:
            if not j['ready']:
                uid = i['metadata']['uid']
                metrics = 'ContainerStatuses'
                resource_status = "False"
                resource_name = i['metadata']['name']
                resource_type = "Pod"
                alert_message = "PodName: {pod_name}, Image: {image}, RestartCount: {restartCount} Reason: {reason} " \
                                "and FailureMessage: {message}".format(
                    pod_name=resource_name, message=j['state']['waiting']['message'],
                    reason=j['state']['waiting']['reason'], image=j['image'], restartCount=j['restartCount'])

                pod_obj, created = Resource.objects.update_or_create(aws_account=aws_account,
                                                                     cluster_name=cluster_name,
                                                                     uid=uid, account_id=data['id'],
                                                                     metrics=metrics, resource_type=resource_type,
                                                                     resource_name=resource_name,
                                                                     defaults={'status': resource_status,
                                                                               'status_message': alert_message,
                                                                               'last_updated': timezone.now(),
                                                                               },
                                                                     )

                print("aws_account: {aws_account}, cluster_name: {cluster_name}, resource_type: {resource_type},"
                      "resource_name: {resource_name}, status: {status}, status_message: {status_message} ".format(
                    aws_account=aws_account, cluster_name=cluster_name, resource_type=resource_type,
                    resource_name=resource_name,
                    status=resource_status, status_message=alert_message
                )
                )


def notification(data):
    aws_account = data['aws_account']
    cluster_name = data['cluster_name']
    alert_status = data['status']
    metrics = data['metrics']
    resource_type = data['resource_type']
    resource_name = data['resource_name']
    message = data['status_message']
    limit = "5"
    count = 0
    email_id = ''
    resource_id = data['account_id']
    account_object = Account.objects.filter(aws_account=aws_account, cluster_name=cluster_name).values('email_id')
    for i in account_object:
        email_id = i['email_id']

    c = Alert.objects.filter(aws_account=aws_account, cluster_name=cluster_name, metrics=metrics).values('count')
    for i in c:
        count = i['count']
    if alert_status == 'True':
        count = count + 1
        print("########################")
        email_notification = EmailNotification(email_id, metrics, message)
        email_notification.send()
        alert, created = Alert.objects.update_or_create(
            account_id=resource_id,
            resource_id=data['id'],
            aws_account=aws_account,
            cluster_name=cluster_name, metrics=metrics,
            resource_type=resource_type,
            resource_name=resource_name,
            defaults={
                'last_sent': timezone.now(),
                'count': count,
                'limit': limit,
            },
        )


@shared_task()
def send_notification():
    start = time.perf_counter()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    with Pool() as executor:
        db_records = list(Resource.objects.all().values())
        executor.map(notification, db_records)

    finish = time.perf_counter()
    print(f'Finish  in {round(finish - start, 2)} second(s)')
    print(len(list(Account.objects.all().values())))


@shared_task()
def get_resource_info_from_k8s_task():
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        db_records = list(Account.objects.all().values())
        executor.map(get_node_info_from_k8s, db_records)

    finish = time.perf_counter()
    print(f'Finish  in {round(finish - start, 2)} second(s)')
    print(len(list(Account.objects.all().values())))


def save_to_db(record):
    # for record in records:
    obj, created = Account.objects.update_or_create(
        aws_account=record['aws_account'], cluster_name=record['cluster_name'], defaults={
            'email_id': record['email_id'], 'slack_channel': record['slack_channel'],
            'k8s_endpoint': record['cluster_endpoint'],
        },
    )


@shared_task()
def upload_to_db():
    start = time.perf_counter()
    data = GetConfigFile()
    data.get_all_data_from_configfile()
    records = data.get_list_data()
    with Pool() as executor:
        db_records = list(Account.objects.all().values())
        results = executor.map(save_to_db, records)

    finish = time.perf_counter()
    print(f'Finish  in {round(finish - start, 2)} second(s)')
    print(len(list(Account.objects.all().values())))
    # for record in records:
    #     obj, created = Account.objects.update_or_create(
    #         aws_account=record['aws_account'], cluster_name=record['cluster_name'], defaults={
    #             'email_id': record['email_id'], 'slack_channel': record['slack_channel'],
    #             'k8s_endpoint': record['cluster_endpoint'],
    #         },
    #     )

# @shared_task()
# def send_notification():
#     resources = ResourceType.objects.all()
#     for resource in resources:
#         alerts = Alert.objects.filter(alert__alert_status="")
#         if resource.status == "True":
#             alert, created = Alert.objects.update_or_create(alert=resources,
#                                                             defaults={'alert_status': 'True',
#                                                                       'count': alerts[resource].count + 1,
#                                                                       'last_sent': datetime.now()}
#                                                             )
#             # queryset = Alert(alert=resource, email_id="soumyarout80@gmail.com", alert_status="True",
#             #                  last_sent=datetime.now())
#             # queryset.save()
#             print("##### There is a failure $$$$$$")
