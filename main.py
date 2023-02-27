import boto3
from datetime import *
from flask import Flask, request
from flask import jsonify
import structlog
app = Flask(__name__)
LOGGER = structlog.get_logger()


def get_arn(account_id, role_name):
    return f"arn:aws:iam::{account_id}:role/{role_name}"


def assume_aws_role(role_name, account_id):
    current_account_id = boto3.client("sts").get_caller_identity().get("Account")
    if current_account_id == account_id:
        LOGGER.debug("No need to assume already assumed role")
        return boto3.Session()
    LOGGER.debug("Assuming AWS Billing role in zalando aws account")
    session_name = f"pinfra-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}"
    assumed_credentials = boto3.client("sts").assume_role(
        RoleArn=get_arn(account_id, role_name), RoleSessionName=session_name
    )["Credentials"]
    return boto3.Session(
        aws_access_key_id=assumed_credentials["AccessKeyId"],
        aws_secret_access_key=assumed_credentials["SecretAccessKey"],
        aws_session_token=assumed_credentials["SessionToken"],
    )

@app.route('/total-cost')
def gettotalcosts():
    start = date.today() - timedelta(days=2)
    end = date.today() - timedelta(days=1)
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')

    # get the value of account from query string (i.e. ?account=some-value)
    account = request.args.get('account')

    aws_session = assume_aws_role(role_name='cost-explorer-iam-role', account_id=account)
    cd = aws_session.client('ce', 'us-east-1')
    totalcostdata = cd.get_cost_and_usage(
    TimePeriod={
        'Start': start,
        'End': end
    },
    Granularity='DAILY',
    Filter={
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "Values": [account]
            }
    },
    Metrics=["UnblendedCost"],
     )

    for item in totalcostdata['ResultsByTime']:
        timestamp = item['TimePeriod']['Start']
        cost = item['Total']['UnblendedCost']['Amount']
        cost = float(cost)
        return jsonify({timestamp: round(cost, 2)}), 200


@app.route('/services-cost')
def getcostsbyservice():
    start = date.today() - timedelta(days=2)
    end = date.today() - timedelta(days=1)
    end = end.strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    result = {}

    # get the value of account from query string (i.e. ?account=some-value)
    account = request.args.get('account')

    aws_session = assume_aws_role(role_name='cost-explorer-iam-role', account_id=account)
    cd = aws_session.client('ce', 'us-east-1')

    servicewisedata = cd.get_cost_and_usage(
        TimePeriod={
            'Start': start,
            'End': end
        },
        Granularity='DAILY',
        Filter={
            "Dimensions": {
                "Key": "LINKED_ACCOUNT",
                "Values": [account]
            }
        },
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            },
        ]
    )

    for item in servicewisedata['ResultsByTime']:
        timestamp = item['TimePeriod']['Start']
        for k in item['Groups']:
            service = k['Keys'][0]
            cost = k['Metrics']['UnblendedCost']['Amount']
            cost = round(float(cost),2)
            result[service] = cost
    return jsonify({timestamp: result}), 200