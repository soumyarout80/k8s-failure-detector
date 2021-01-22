import yaml
import os


class GetConfigFile(object):
    def __init__(self):
        self.all_data = list()

    def read_data(self):
        with open("utility/data.yaml", 'r') as stream:
            try:
                data = yaml.safe_load(stream)
                return data
            except yaml.YAMLError as exc:
                print(exc)

    def get_list_data(self):
        return self.all_data

    def create_list(self, dictionary_data):
        self.all_data.append(dictionary_data)

    def get_all_data_from_configfile(self):
        data = self.read_data()
        config_data = {}
        for accounts in data:
            config_data['aws_account'] = accounts['account']
            for j in accounts['clusters']:
                config_data['cluster_name'] = j['details']['name']
                config_data['email_id'] = j['details']['email_id']
                config_data['slack_channel'] = j['details']['slack_channel']
                config_data['cluster_endpoint'] = j['details']['k8s_cluster_endpoint']
                out_dict = config_data.copy()
                self.create_list(out_dict)
