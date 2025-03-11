from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as actions,
    aws_iam as iam,
    aws_logs as logs,
    aws_cloudwatch_actions  as actions
    
)
import aws_cdk as cdk
from constructs import Construct

class Ec2AlarmStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # 创建 VPC
        vpc = ec2.Vpc.from_lookup(
            self,
            f"TestAlarm",
            vpc_id="vpc-0fe29f1b2623eb8e2",
            vpc_name="VHPC-internet-access-vpc-vpc",
        )

        # 创建 EC2 实例
        instance = ec2.Instance(self, "TestAlarmInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
        )

        # 创建 CloudWatch 警报
        #在这个设置中，CloudWatch 将每 5 分钟收集一次 CPU 使用率数据，并在过去 100 分钟（10 个周期）内检查至少 2 个数据点是否低于 20%。确保这些参数符合您的监控需求。
        alarm = cloudwatch.Alarm(self, "CPUUtilizationAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/EC2",
                metric_name="CPUUtilization",
                dimensions_map={
                    "InstanceId": instance.instance_id,
                },
                statistic="Average",
                period=cdk.Duration.minutes(10),
            ),
            threshold=20,
            evaluation_periods=10,
            datapoints_to_alarm=2,
            comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
        )

        alarm.add_alarm_action(
            actions.Ec2Action(actions.Ec2InstanceAction.STOP))