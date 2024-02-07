import re
from urllib.parse import urlparse, parse_qs

URL_REGEX = re.compile(r"https?://[a-zA-Z0-9.]+(/[a-zA-Z0-9./?#]*)?")

path = "http://10.105.0.21:11698/?redir=http://10.105.0.21:11698/flag"
print(f"{path = }")

url_p = urlparse(path)
print(f"{url_p = }")

qs = parse_qs(url_p.query)
print(f"{qs = }")

redir = qs["redir"][0]

print(f"{redir = }")

a = True if URL_REGEX.match(redir) else False

print(f"{a = }")
