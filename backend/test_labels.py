import json
import urllib.request

url = "https://huggingface.co/Hello-SimpleAI/chatgpt-detector-roberta/resolve/main/config.json"
try:
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    print(data.get("id2label"))
except Exception as e:
    print(e)
