import boto3
import json
import os
from dotenv import load_dotenv


load_dotenv()

AGENT_CORE_ARN = os.getenv("AGENT_CORE_ARN")
AGENT_CORE_SESSION_ID = os.getenv("AGENT_CORE_SESSION_ID")

client = boto3.client('bedrock-agentcore', region_name='us-west-2')
payload = json.dumps({
    "input": {"prompt": "Create a short Twitter post about a new coffee shop opening"}
})

response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_CORE_ARN,
    runtimeSessionId=AGENT_CORE_SESSION_ID,
    payload=payload,
    qualifier="DEFAULT"
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)