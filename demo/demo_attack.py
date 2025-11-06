import requests, time, json
ALERT = { "id":"demo-ransom-999", "source":"demo", "observables": {"hostname":"demo-finance-db","ip":"10.0.9.9","cmdline":"/usr/bin/encrypt --target /important --ransom","filehash":"feedfacedeadbeef"} }
def send_alert():
    r = requests.post('http://localhost:8000/ingest', json=ALERT, timeout=5)
    print('ingest response', r.status_code, r.text)
    time.sleep(1.5)
    r2 = requests.get('http://localhost:8000/audit')
    print('audit:', json.dumps(r2.json(), indent=2))
if __name__ == '__main__':
    send_alert()
