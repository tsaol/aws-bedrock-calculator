ANTHROPIC_PRICING = {
    "us-east-1": {
        "claude-instant-v1": {"input": 0.00080,"output": 0.00240,},
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.00080,"output": 0.00240,},
        "claude-v2": {"input": 0.00080,"output": 0.00240,},
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.003, "output": 0.015},
        "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.003, "output": 0.015},
        "claude-v3-sonnet": {"input": 0.003, "output": 0.015},
    },
    "us-west-2": {
        "claude-instant-v1": {
            "input": 0.00080,
            "output": 0.00240,
        },
        "claude-v2": {
            "input": 0.00080,
            "output": 0.00240,
        },
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.003, "output": 0.015},
        "anthropic.claude-3-sonnet-20240229-v1:0": {"input": 0.003, "output": 0.015},
        "claude-v3-sonnet": {"input": 0.003, "output": 0.015},
    },
    "ap-northeast-1": {
        "claude-instant-v1": {
            "input": 0.00080,
            "output": 0.00240,
        },
        "claude-v2": {
            "input": 0.00080,
            "output": 0.00240,
        },
    },
    "default": {
        "claude-instant-v1": {
            "input": 0.00080,
            "output": 0.00240,
        },
        "claude-v2": {
            "input": 0.00080,
            "output": 0.00240,
        },
        "claude-v3-haiku": {"input": 0.00025, "output": 0.00125},
        "claude-v3-sonnet": {"input": 0.00300, "output": 0.01500},
    },
}