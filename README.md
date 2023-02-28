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
* Create a AWS role in your AWS as per this [cloudformation template](https://github.com/neerajtiwar/aws-cost-exporter/blob/main/cloud-formation.yaml)
* Login with a AWS IAM user and assume the IAM role we created in the first step, using following:
```bash
aws sts assume-role --role-arn "arn:aws:iam::002474742307:role/cost-explorer-iam-role" --role-session-name AWSCLI-Session
```
