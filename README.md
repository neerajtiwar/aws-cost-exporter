# aws-cost-exporter
Python Rest application that exports AWS costs for the given account and its services

## How it works
This application has two Rest API endpoints, both the endpoints
takes `account` as a query params in the request and outputs total
and services costs based on the current day(daily).

* total-cost

Example CURL:

```bash
curl http://localhost:8001/total-cost\?account\=00123456789`

{"2023-02-26":0.0}
```

* services-cost

```bash
curl http://localhost:8001/services-cost\?account\=00123456789`

{
  "2023-02-26":
  { 
    "ec2": 121.2,
    "Amazon DynamoDB": 38.45,
    "Amazon RDS": 232.12
  }
}
```
## Local setup
To run this application on local by doing the following steps:
* Create AWS role in your AWS as per this [cloudformation template](https://github.com/neerajtiwar/aws-cost-exporter/blob/main/cloud-formation.yaml)
* Login with AWS IAM user that you have given permission in the first step to assume this role and assume the IAM role we created in the first step, using following:
```bash
aws sts assume-role --role-arn "arn:aws:iam::1234567890:role/cost-explorer-iam-role" --role-session-name AWSCLI-Session
```
* Now, in the terminal run the python program:
```bash
# gunicorn --workers 1 --timeout 300 --bind 0.0.0.0:8001 --log-file=-  main:app main.py
[2023-02-28 22:04:59 +0100] [27676] [INFO] Starting gunicorn 20.1.0
[2023-02-28 22:04:59 +0100] [27676] [INFO] Listening at: http://0.0.0.0:8001 (27676)
[2023-02-28 22:04:59 +0100] [27676] [INFO] Using worker: sync
[2023-02-28 22:04:59 +0100] [27677] [INFO] Booting worker with pid: 27677
```
* You will now be able to run the [curl commands](https://github.com/neerajtiwar/aws-cost-exporter#how-it-works) given in the initial documentation to fetch the total-costs and services-costs

## How to contribute
If you see any mistakes or want to improve something, feel free to create a PR OR create issues if something is not working.
