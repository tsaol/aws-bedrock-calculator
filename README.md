# bedrock-calculator
本方案旨在助您高效构建Bedrock监控体系,实现对Bedrock多IAM用户场景的无感知、低成本追踪与精细管控。
* 无服务器架构
* 对每一个IAM用户进行监控
* 根据企业需求灵活调整监控频率与窗口期
* 消息通知与报警
* 自动化触发用户权限管控



## 架构图
![](/images/image-1.jpg)

## 代码
### pricing.py 定价信息

存储不同区域和模型的定价信息。

包含一个名为 ANTHROPIC_PRICING 的字典，该字典按 Region 和 Model 组织价格信息。每个模型都有输入和输出 Token 的价格。


### sns_utils.py 告警信息
提供了一个函数 send_cost_alert，用于在费用超出阈值时发送 SNS 告警消息。定义了 send_cost_alert 函数，该函数接受总费用、阈值和 SNS 主题的 ARN 作为参数。在函数内部，它检查总费用是否超过阈值，如果超过，则构建一条警告消息并使用 sns.publish 方法将其发布到指定的 SNS 主题。
```
def send_cost_alert(total_cost, threshold, topic_arn):
    if total_cost > threshold:
        message = f"警告:Bedrock模型的总使用费用已达到 ${total_cost:.2f},超出了 ${threshold:.2f} 的阈值。"
        sns.publish(
            TopicArn=topic_arn,
            Subject='模型费用超出阈值',
            Message=message
        )
```

### Lambda 主函数文件
您可以直接使用以下语句查询每一条记录：
```
  query = '''
    fields requestId, input.inputTokenCount, output.outputTokenCount, region, timestamp, identity.arn, modelId
    | sort timestamp desc
    '''
```

如果您的请求量较大，建议您更改为以下 query 语句以做聚合处理，本文示例为从 CloudWatch Logs 中聚合过去 1 小时内的模型使用数据。
```
    query = '''
    fields input.inputTokenCount, output.outputTokenCount, @timestamp, identity.arn, modelId
    | stats sum(input.inputTokenCount) as total_input_tokens, 
            sum(output.outputTokenCount) as total_output_tokens,
            count(*) as event_count
      by bin(3600s) as day, identity.arn, modelId
    | sort day desc, modelId
    '''
```