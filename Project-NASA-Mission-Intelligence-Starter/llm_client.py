from typing import Dict, List
from openai import OpenAI
import os

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""
    client = OpenAI(api_key=openai_key)


    try:
        user_message_prompt = _get_user_message_prompt(context, user_message)


        conversation_history.append({
            "role": "user",
            "content": user_message_prompt
        })
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,
            temperature=0.7,
            max_tokens=300
        )

        assistant_message = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message
    except Exception as e:
        error_msg = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."
        print(f"Error generating response: {e}")
        return error_msg
    
def _get_user_message_prompt(self, context_text, query:str):
    return f"""You are a helpful NASA expert for NASA.

Your role is to assist astronauts, researchers, or even a curious historian with:
- questions about NASA's most historic space missions. Based on the following context documents, please answer the user's question. If the context doesn't contain enough information to answer the question completely, please say so and provide what information you can.

Guidelines:
- Be professional, friendly and empathetic
- Provide clear, concise answers
- Ask clarifying questions when the customer's intent is unclear
- If you don't have specific information, ask for it
- Always prioritize customer satisfaction

Context Documents:
{context_text}

User Question: {query}

Please provide a comprehensive answer based on the context provided.
If a request is outside your capabilities, politely explain and offer to escalate to a human agent"""