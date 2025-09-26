# marketing-agent
Marketing Agent for AWS Agentic AI Hackathon 26.09.2025

## Environment Setup

Create a `.env` file in the project root with the following API keys:

```bash
# OpenAI API key for the WriterAgent
OPENAI_API_KEY=your_openai_api_key_here

# Gemini API key for the PhotographerAgent  
GEMINI_API_KEY=your_gemini_api_key_here
```

## Deploy the Writer Agent on AgentCore
Make sure to install the dependencies:
`uv sync`

Then deploy with the following commands (make sure to have the AWS creds configured):
`agentcore configure -e agentcore_app.py --name marketing_writer_agent`

`agentcore launch`

`agentcore invoke '{"prompt": "Create a short Twitter post about a new coffee shop opening"}'`