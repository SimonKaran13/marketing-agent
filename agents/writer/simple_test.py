#!/usr/bin/env python3
"""
Simple test to demonstrate WriterAgent functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.writer.writer import WriterAgent
from prompts.InputPrompt import InputPrompt


def main():
    """Test the WriterAgent with both simple query and Prompt object."""
    print("🧪 Testing WriterAgent")
    print("=" * 30)
    
    try:
        # Create the agent
        print("Creating WriterAgent...")
        writer = WriterAgent()
        print("✅ WriterAgent created successfully!")
        
        # Test 1: Simple query
        print("\n📝 Test 1: Simple query")
        print("-" * 40)
        prompt = "Create a short Twitter post about a new coffee shop opening"
        print(f"Query: {prompt}")
        print("Response:")
        result = writer.invoke(query=prompt)
        print(result)
        
        # Test 2: Using InputPrompt object
        print("\n📋 Test 2: Using InputPrompt object")
        print("-" * 40)
        prompt_data = InputPrompt(
            product_images=[],  # Empty list for now
            product_name="EcoClean Laundry Detergent",
            product_description="Eco-friendly laundry detergent made from natural ingredients",
            product_main_features="Plant-based, biodegradable, hypoallergenic",
            product_benefits="Gentle on skin, safe for environment, effective cleaning"
        )
        print("Product: EcoClean Laundry Detergent")
        print("Response:")
        result = writer.invoke(prompt_data=prompt_data)
        print(result)
        
        print("\n✅ Both tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. OPENAI_API_KEY set in your .env file")
        print("2. Valid OpenAI API key")
        print("3. Internet connection")


if __name__ == "__main__":
    main()
