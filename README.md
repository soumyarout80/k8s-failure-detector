# k8s-failure-detector
**Notification feature(Features):**
1. Email/Slack Integration
2. Backend Admin Page for CRUD operations.
3. Screen to view all notifications (Admin page or Custom page[React js])
4. Rate limiting (Each metric for every day)
5. Toggle Notification(Enable/Disable) (Cluster and metrics level toggle)
6. Auto schedule for next Email/Slack notification
7. Cluster-wise Each Metrics wise toggle notification
8. Periodic tasks

**Why periodic task:**
* Generating periodic reports
* Clearing cache
* Sending batch email notifications
* Running nightly maintenance jobs
* Check for the config file for a new entry

**LLD:**
1. Bootstrap/config file to create all accounts and cluster details in our application Account
Model. (Periodic task)
2. To start hitting Kubernetes cluster API we will fetch records from Model(which we pushed
before (point 1).
3. After getting data from Kubernetes cluster API for some metrics we will store in
Resource Model. (Periodic task )
4. Once we get all metrics information our Async task for sending notifications starts
consuming these records from the Resource model.
5. Send notification will check for status true state. If it's in True state it will send a
notification to the cluster user and create/update a new record in Alert Model.

**Conditions:**
* Check for the specific cluster in Enable state
* Then check whether the metric is in Enable state.
* Check for records is available in Alert Model. If it’s available then check for the next scheduled time, Limit, Count

```Yml Config yaml file:
- account: 90933027639046
clusters:
- details:
email_id: XXX@gmail.com
k8s_cluster_endpoint: http://192.168.49.1:8008/
name: Phoenix
slack_channel: NA
- details:
email_id: XXXXX0@gmail.com
k8s_cluster_endpoint: http://192.168.49.1:8008/
name: TinyUrl
slack_channel: NA
```
**Some Kubernetes cluster API:**
1. Nodes: /api/v1/nodes
2. Pods: /api/v1/pods
3. Services: /api/v1/services
4. ETCD: /healthz/etcd
a. /livez/etcd
b. /readyz/etcd
5. Volume: /api/v1/persistentvolumeclaims
