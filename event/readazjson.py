import json
import base64
import azure.functions.blob as func
import os
os.chdir(os.path.split(__file__)[0])

with open("azevent.json", "r") as f:
    event_data = json.load(f)
event_data["data"] = base64.standard_b64decode(event_data["data"].encode("UTF-8"))
event = func.InputStream(**event_data)

print(event.name, event.uri, event.length, len(event.read()))