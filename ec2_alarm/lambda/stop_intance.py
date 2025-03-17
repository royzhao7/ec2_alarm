import os
import boto3

def handler(event, context):
    alarm_name = os.environ['ALARM_NAME']  
    # Update the alarm state to OK (this is via another method, not directly setting)
    cloudwatch = boto3.client('cloudwatch')
    cloudwatch.set_alarm_state(
        AlarmName=alarm_name,
        StateValue='OK',
        StateReason='NetworkIn reseted to acceptable range.'
    )