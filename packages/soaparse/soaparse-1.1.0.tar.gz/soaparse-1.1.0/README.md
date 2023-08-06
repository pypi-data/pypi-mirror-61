# soaparse
Sane, modular DNS [SOA record](https://en.wikipedia.org/wiki/SOA_record) parsing

Fields are based on https://www.ripe.net/publications/docs/ripe-203

The best-guess email address is parsed from the `rname` field

Trailing periods are stripped

#### Usage
```python
import json
import soaparse

soa_record_str = "ns.example.com. email.example.com. 20200101 60 3 2 1"
soa = soaparse.soa_parse(soa_record_str)

json.dumps(soa.__dict__)
```
