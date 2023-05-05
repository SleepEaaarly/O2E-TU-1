import json
import requests


def get_chatgpt_response(prompt: str):
    url = f"https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer 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"}
    sent_data = {}
    sent_data['model'] = "gpt-3.5-turbo"
    sent_data['messages'] = [{"role": "user", "content": prompt}]
    sent_data['temperature'] = 0.7
    jsonfy = json.dumps(sent_data)
    response = requests.post(url, headers=headers, data=jsonfy)
    ret_json = json.loads(response.content.decode('utf-8'))
    return ret_json['choices'][0]['message']['content']
