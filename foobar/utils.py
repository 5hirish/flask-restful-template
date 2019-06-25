import boto3


def get_aws_client(aws_resource, aws_access_key, aws_secret_key):
    client = boto3.client(
        aws_resource,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    return client
