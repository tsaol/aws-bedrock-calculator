import boto3

def remove_bedrock_policies(identity):
    iam = boto3.client('iam')

    if identity:
        try:
            user_name = identity.split("/")[1]
            
            response = iam.list_attached_user_policies(UserName=user_name)
            attached_policies = response.get('AttachedPolicies', [])

            for policy in attached_policies:
                policy_name = policy['PolicyName']
                if "bedrockread" in policy_name.lower():
                    try:
                        iam.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])
                        print(f"Removed policy '{policy_name}' from user '{identity}'")
                    except Exception as e:
                        print(f"Error removing policy '{policy_name}': {e}")
        except Exception as e:
            print(f"Error listing attached user policies for '{identity}': {e}")