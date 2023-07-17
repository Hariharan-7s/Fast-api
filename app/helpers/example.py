import http.client
import json
import ssl

conn = http.client.HTTPSConnection(
    "apiemindsinternal.ddns.net",
    context = ssl._create_unverified_context()
)

payload = json.dumps({
  "bucket_name": "bearingdatadts3",
  "file_name": "W22.csv",
  "event_time": "2023-06-30"
})
headers = {
  'Content-Type': 'application/json'
}
conn.request("POST", "/bearing/dt-engine", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))