from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator, current_time
from prompts.InputPrompt import InputPrompt
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


# Define a custom tool for content analysis
@tool
def content_analyzer(text: str, analysis_type: str = "readability") -> str:
    """
    Analyze content for readability, engagement, or other metrics.

    Args:
        text (str): The content to analyze
        analysis_type (str): Type of analysis (readability, engagement, length)

    Returns:
        str: Analysis results
    """
    if analysis_type == "readability":
        word_count = len(text.split())
        char_count = len(text)
        return f"Content Analysis: {word_count} words, {char_count} characters"
    elif analysis_type == "engagement":
        # Simple engagement score based on question marks and exclamation points
        engagement_score = text.count('?') + text.count('!')
        return f"Engagement Score: {engagement_score} (based on questions and exclamations)"
    else:
        return f"Analysis type '{analysis_type}' not supported"


# Define a custom tool for hashtag generation
@tool
def generate_hashtags(topic: str, count: int = 5) -> str:
    """
    Generate relevant hashtags for a given topic.

    Args:
        topic (str): The topic to generate hashtags for
        count (int): Number of hashtags to generate

    Returns:
        str: Comma-separated list of hashtags
    """
    # Simple hashtag generation (in a real app, this would be more sophisticated)
    base_hashtags = [f"#{topic.replace(' ', '')}", f"#{topic.replace(' ', '').lower()}"]
    additional = [f"#{topic.replace(' ', '')}{i}" for i in range(1, count-1)]
    return ", ".join(base_hashtags + additional[:count-2])


class WriterAgent:
    def __init__(
        self,
        system_prompt: str = None,
        tools: List[callable] = None,
        openai_api_key: str = None,
        model_id: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ):
        self.system_prompt = (
            system_prompt
            if system_prompt
            else """
    You are a professional social media content writer specializing in creating engaging, viral-worthy posts across all platforms.
    
    You have access to tools to help you create high-quality marketing content:
    - Calculator: for any calculations needed
    - Current time: to reference timing in posts
    - Content analyzer: to analyze your content
    - Hashtag generator: to create relevant hashtags
    
    You will ALWAYS follow these guidelines when creating content:
    - Create content that is engaging, informative, and aligned with the brand voice
    - Research thoroughly before writing to ensure accuracy and relevance
    - Optimize content for the target audience and platform requirements
    - Always maintain a professional and creative tone
    - Focus on creating content that drives engagement and achieves marketing objectives
    - Ensure all content is original and plagiarism-free
    - Adapt content style and tone based on the target platform and audience
    """
        )

        # Get OpenAI API key from parameter or environment
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass openai_api_key parameter.")

        # Create OpenAI model
        self.openai_model = OpenAIModel(
            client_args={
                "api_key": api_key,
            },
            model_id=model_id,
            params={
                "max_tokens": 2000,
                "temperature": temperature,
            }
        )

        # Combine built-in tools with custom tools
        default_tools = [calculator, current_time, content_analyzer, generate_hashtags]
        self.tools = default_tools + (tools or [])

        # Create the Strands Agent with OpenAI model
        self.agent = Agent(
            model=self.openai_model,
            system_prompt=self.system_prompt,
            tools=self.tools,
        )

    def invoke(self, prompt_data: InputPrompt = None, query: str = None):
        """Invoke the agent with either an InputPrompt object or a direct query string."""
        try:
            if prompt_data:
                # Convert prompt data to a query string for the agent
                agent_query = self._format_prompt_data_as_query(prompt_data)
            elif query:
                agent_query = query
            else:
                agent_query = "Create engaging social media content"
            
            response = self.agent(agent_query)
            return str(response.message)
        except Exception as e:
            return f"Error invoking writer agent: {e}"

    async def stream(self, prompt_data: InputPrompt = None, query: str = None):
        """Stream the agent response with either an InputPrompt object or a direct query string."""
        try:
            if prompt_data:
                # Convert prompt data to a query string for the agent
                agent_query = self._format_prompt_data_as_query(prompt_data)
            elif query:
                agent_query = query
            else:
                agent_query = "Create engaging social media content"
            
            async for event in self.agent.stream_async(agent_query):
                if "data" in event:
                    # Only stream text chunks to the client
                    yield event["data"]

        except Exception as e:
            yield f"We are unable to process your writing request at the moment. Error: {e}"

    def _format_prompt_data_as_query(self, prompt_data: InputPrompt) -> str:
        """Format the InputPrompt data as a query string for the agent."""
        query_parts = []
        
        if prompt_data.product_name:
            query_parts.append(f"Product Name: {prompt_data.product_name}")
        
        if prompt_data.product_description:
            query_parts.append(f"Product Description: {prompt_data.product_description}")
        
        if prompt_data.product_main_features:
            query_parts.append(f"Main Features: {prompt_data.product_main_features}")
        
        if prompt_data.product_benefits:
            query_parts.append(f"Benefits: {prompt_data.product_benefits}")
        
        if prompt_data.product_use_cases:
            query_parts.append(f"Use Cases: {prompt_data.product_use_cases}")
        
        if prompt_data.product_pricing:
            query_parts.append(f"Pricing: {prompt_data.product_pricing}")
        
        if prompt_data.product_pricing_details:
            query_parts.append(f"Pricing Details: {prompt_data.product_pricing_details}")
        
        if prompt_data.product_pricing_features:
            query_parts.append(f"Pricing Features: {prompt_data.product_pricing_features}")
        
        if prompt_data.product_pricing_benefits:
            query_parts.append(f"Pricing Benefits: {prompt_data.product_pricing_benefits}")
        
        if query_parts:
            return "Create engaging social media content for this product:\n\n" + "\n".join(query_parts)
        else:
            return "Create engaging social media content for our product"
