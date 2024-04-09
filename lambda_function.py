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
    fields requestId, input.inputTokenCount, output.outputTokenCount, region, timestamp, identity.arn, modelId
    | sort timestamp desc
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
        time.sleep(2)
        response = logs_client.get_query_results(queryId=query_id)
    
    print('hello')
    print("Results:", response['results'])
    record = ''
    for record in response['results']:
        model_id = None
        region = None
        total_input_tokens = None
        total_output_tokens = None

        for field in record:
            if field['field'] == 'modelId':
                model_id = field['value']
            elif field['field'] == 'region':
                region = field['value']
            elif field['field'] == 'input.inputTokenCount':
                total_input_tokens = float(field['value'])
            elif field['field'] == 'output.outputTokenCount':
                total_output_tokens = float(field['value'])
        
        
        if model_id and region and total_input_tokens is not None and total_output_tokens is not None:
            input_token_price = get_token_price(model_id, 'input', region)
            output_token_price = get_token_price(model_id, 'output', region)

            if input_token_price is not None and output_token_price is not None:
                input_token_cost = total_input_tokens / 1000 * input_token_price
                output_token_cost = total_output_tokens / 1000 * output_token_price
                total_cost = input_token_cost + output_token_cost
                record.append({'field': 'inputTokenCost', 'value': str(input_token_cost)})
                record.append({'field': 'outputTokenCost', 'value': str(output_token_cost)})
                record.append({'field': 'totalCost', 'value': str(total_cost)})

            else:
                record.append({'field': 'inputTokenCost', 'value': 'None'})
                record.append({'field': 'outputTokenCost', 'value': 'None'})  
                record.append({'field': 'totalCost', 'value': 'None'})
                


    
    return response['results']