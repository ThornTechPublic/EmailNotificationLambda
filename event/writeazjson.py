import json
import base64
import sys
import os
os.chdir(os.path.split(__file__)[0])

try:
    filename = sys.argv[1]
    print(f"Using file {filename}")
except IndexError:
    filename = input("Which file (relative to this program file)? ")
with open(filename, "rb") as f:
    data = f.read()
b64data = base64.standard_b64encode(data).decode("UTF-8")
with open("azevent.json", "w") as f:
    json.dump({"data": b64data, "length": len(data),
               "uri": f"https://joshpgpstorage.blob.core.windows.net/pgptest1/{filename}", "name": filename},
              f, indent=1)
