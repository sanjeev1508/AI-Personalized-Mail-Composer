import requests

API_URL = "Api URL"
API_KEY = "Your API Key"
MODEL = "Model Name"

def generate_email(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stream": False
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error from NVIDIA API: {e}\n{res.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")

    try:
        response_json = res.json()
        return response_json["choices"][0]["message"]["content"]
    except (ValueError, KeyError) as e:
        raise Exception(f"Invalid response format from NVIDIA API: {e}\nRaw: {res.text}")
