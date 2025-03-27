from groq import Groq
from ..config import Config

def call_llm(sys_msg, user_msg):
    
    client = Groq(api_key=Config.GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content": sys_msg
            },
            {
                "role": "user",
                "content": user_msg
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
    )

    return chat_completion.choices[0].message.content