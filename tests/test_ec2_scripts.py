import pytest
import sys
import os

import boto
import boto3
import botocore
from moto import mock_ec2_deprecated, mock_ec2

from EC2_UpdateTags import EC2_UpdateTags

@mock_ec2_deprecated
def test_ec2_found():
    print('-----------------------TEST_UPDATE_EC2_Tags_Found--------------------------')
    conn = boto.ec2.connect_to_region("us-east-1")
    reservation = conn.run_instances('i-01d4d95bd13ac9dbe')
    print(reservation.instances[0].id)

    csv_line = reservation.instances[0].id + ',Stop,prod,anusha_redshift_jumpbox,Linux,Ubuntu 18.04,Anusha,-,,-'

    # Create a test csv with the id of the created instance above
    f = open('tests/testFiles/test.csv', 'r+')
    f.truncate(0)
    f.write(csv_line)
    f.close()

    val = EC2_UpdateTags.lambda_handler('test', 'tests/testFiles/test.csv')
    assert val['statusCode'] == 200

@mock_ec2_deprecated
def test_ec2_not_found():
    print('-----------------------TEST_UPDATE_EC2_Tags_Not_Found--------------------------')
    # Create a test csv with the id of the created instance above
    f = open('tests/testFiles/test.csv', 'r+')
    f.truncate(0)
    csv_line = 'i-1111111111111,Stop,prod,anusha_redshift_jumpbox,Linux,Ubuntu 18.04,Anusha,-,,-'
    f.write(csv_line)
    f.close()

    val = EC2_UpdateTags.lambda_handler('test', 'tests/testFiles/test.csv')
    assert val['statusCode'] == 200
