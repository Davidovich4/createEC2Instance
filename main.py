import boto3
from botocore.exceptions import ClientError

region = 'eu-west-1'
#provide credentials
access_key = ''
access_key_id = ''

def main():
    ec2 = boto3.client('ec2', region_name=region,
                       aws_secret_access_key=access_key,
                       aws_access_key_id=access_key_id)

    #set instance parameters
    instanceresponse = ec2.run_instances(
        ImageId='',
        KeyName='',
        MinCount=1,
        MaxCount=1,
        SecurityGroups=[
            ''
        ],
        InstanceType='t2.micro',
        UserData=user_data_script)

    for i in instanceresponse['Instances']:
        instanceId = i['InstanceId']

    print instanceId + ' instance created.'

    ec2resource = boto3.resource('ec2', region_name=region,
                       aws_secret_access_key=access_key,
                       aws_access_key_id=access_key_id)
    instance = ec2resource.Instance(instanceId)
    instance.wait_until_running()

    try:
        #set elastic ip id
        response = ec2.associate_address(AllocationId='', InstanceId=instanceId)
        print instanceId + 'is associated with elastic IP'
    except ClientError as e:
        print(e)

#add the proper init script for the instance creation
user_data_script = """#!/bin/bash
echo "Hello World" >> /tmp/data.txt
"""

if __name__ == "__main__":
    main()