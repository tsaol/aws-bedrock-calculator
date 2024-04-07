import json
import boto3
import time
from pricing import ANTHROPIC_PRICING

def get_token_price(model_id, token_type, region):
    if region in ANTHROPIC_PRICING and model_id in ANTHROPIC_PRICING[region]:
        return ANTHROPIC_PRICING[region][model_id][token_type]
    elif model_id in ANTHROPIC_PRICING["default"]:
        return ANTHROPIC_PRICING["default"][model_id][token_type]
    else:
        return None

def lambda_handler(event, context):
    logs_client = boto3.client('logs')

    query = '''
    fields input.inputTokenCount, output.outputTokenCount, @timestamp, identity.arn, modelId
    | stats sum(input.inputTokenCount) as total_input_tokens, 
            sum(output.outputTokenCount) as total_output_tokens,
            count(*) as event_count
      by bin(86400s) as day, identity.arn, modelId
    | sort day desc, modelId
    '''

    start_time = int(time.time()) - 259200  # 查询最近24小时的数据
    end_time = int(time.time())

    response = logs_client.start_query(
        logGroupName='bedrock-log-test',
        startTime=start_time,
        endTime=end_time,
        queryString=query
    )
    query_id = response['queryId']

    response = logs_client.get_query_results(queryId=query_id)

    while response['status'] == 'Running':
        time.sleep(1)
        response = logs_client.get_query_results(queryId=query_id)
    
    print('------------------------')
    print(response)
    print('------------------------')
    
    
    for record in response['results']:
        model_id = record[1]['value']  # 访问 'modelId' 字段
        region = 'us-east-1'  # 替换为实际区域
        total_input_tokens = float(record[3]['value'])  # 访问 'total_input_tokens' 字段
        total_output_tokens = float(record[4]['value'])  # 访问 'total_output_tokens' 字段
        
        input_token_price = get_token_price(model_id, 'input', region)
        output_token_price = get_token_price(model_id, 'output', region)
        print('---record---')

        if input_token_price is not None and output_token_price is not None:
            input_token_cost = round(total_input_tokens / 1000 * input_token_price, 2)
            output_token_cost = round(total_output_tokens / 1000 * output_token_price, 2)
            total_cost = round(input_token_cost + output_token_cost, 2)
            
            record.append({'field': 'inputTokenCost', 'value': str(input_token_cost)})
            record.append({'field': 'outputTokenCost', 'value': str(output_token_cost)})
            record.append({'field': 'totalCost', 'value': str(total_cost)})
            print(record)

        else:
            record.append({'field': 'inputTokenCost', 'value': 'None'})
            record.append({'field': 'outputTokenCost', 'value': 'None'})  
            record.append({'field': 'totalCost', 'value': 'None'})
            print(record)
    
    return response['results']