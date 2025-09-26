from bedrock_agentcore import BedrockAgentCoreApp
from agents.writer.writer import WriterAgent
import os


app = BedrockAgentCoreApp()


# Default to Claude 3.7 Sonnet in us-west-2; allow env override
DEFAULT_MODEL_ID = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
DEFAULT_REGION = "us-west-2"


def _build_agent():
    model_id = os.getenv("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)
    region_name = os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", DEFAULT_REGION))

    # Instantiate WriterAgent using Bedrock provider
    return WriterAgent(
        provider="bedrock",
        bedrock_model_id=model_id,
        aws_region=region_name,
        temperature=float(os.getenv("WRITER_TEMPERATURE", "0.7")),
    )


writer_agent = _build_agent()


@app.entrypoint
def invoke(payload: dict):
    """AgentCore entrypoint for WriterAgent.

    Expected payload keys:
    - prompt: str (direct prompt string)
    - input_prompt: dict (fields matching prompts.InputPrompt)
    """
    try:
        from prompts.InputPrompt import InputPrompt

        prompt = payload.get("prompt")
        input_prompt_data = payload.get("input_prompt")

        if input_prompt_data:
            # Coerce dict to InputPrompt dataclass
            prompt_obj = InputPrompt(**input_prompt_data)
            result = writer_agent.invoke(prompt_data=prompt_obj)
        else:
            result = writer_agent.invoke(query=prompt)

        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    app.run()


