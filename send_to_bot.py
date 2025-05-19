import anthropic
import os
import google.generativeai as genai




def send_text(text, model, key, language):
    sys_prompt = "write a template for the following message, do not add any comments, commentary, or other text other than the code. Your response should be as simple as possible, using as few characters as possible. Assume you are writing " + language + " code. Messages before the code such as \"Sure, here is a X\", or \"Here's a X\" are considered unnecessary text"

    if model == "Claude":
        text = send_to_claude(text, key, language, sys_prompt)
    if model == "Gemini":
        text = send_to_gemini(text, key, language, sys_prompt)
    return (text)

def send_to_claude(text, key, language, sys_prompt):

    client = anthropic.Anthropic(api_key=key)
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        system=sys_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ]
    )
    return (message.content[0].text)

def send_to_gemini(text, gemini_key, language, sys_prompt):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(
        contents=(sys_prompt + text)
    )
    return(response.text)

