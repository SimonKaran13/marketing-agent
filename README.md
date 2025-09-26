# marketing-agent
Marketing Agent for AWS Agentic AI Hackathon 26.09.2025


## Deploy the Writer Agent on AgentCore
Make sure to install the dependencies:
`uv sync`

Then deploy with the following commands (make sure to have the AWS creds configured):
`agentcore configure -e agentcore_app.py --name marketing_writer_agent`

`agentcore launch`

`agentcore invoke '{"prompt": "Create a short Twitter post about a new coffee shop opening"}'`