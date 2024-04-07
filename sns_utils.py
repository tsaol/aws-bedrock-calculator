# sns_utils.py
import boto3

sns = boto3.client('sns')

def send_cost_alert(total_cost, threshold, topic_arn):
    if total_cost > threshold:
        message = f"警告:A模型的总使用费用已达到 ${total_cost:.2f},超出了 ${threshold:.2f} 的阈值。"
        sns.publish(
            TopicArn=topic_arn,
            Subject='模型费用超出阈值',
            Message=message
        )