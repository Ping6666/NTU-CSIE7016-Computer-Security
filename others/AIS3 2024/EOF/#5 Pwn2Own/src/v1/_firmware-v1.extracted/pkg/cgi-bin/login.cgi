#!/usr/bin/python3

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
import cgi
import os
import jwt
import time

def show_login_form():
    print('Status: 200')
    print('Content-type: text/html')
    print()
    print('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    </head>
    <body>
        <section class="section">
            <div class="container" style="max-width: 400px;">
                <h1 class="title">Login Page</h1>
                <form action="/cgi-bin/login.cgi" method="post">
                    <div class="field">
                        <label class="label" for="username">Username:</label>
                        <div class="control">
                            <input class="input" type="text" id="username" name="username" required>
                        </div>
                    </div>
                    <div class="field">
                        <label class="label" for="password">Password:</label>
                        <div class="control">
                            <input class="input" type="password" id="password" name="password" required>
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <button class="button is-primary">Login</button>
                        </div>
                    </div>
                </form>
            </div>
        </section>
    </body>
    </html>

    ''')

def show_auth_fail():
    print('Status: 403')
    print('Content-type: text/plain')
    print()
    print('Incorrect username or password.')

def login_success(username):
    with open('/etc/ais3eof-firmware/secret','r') as f:
        secret = f.read().strip()
    payload = {'user': username, 'exp': int(time.time()) + 3600}
    token = jwt.encode(payload, secret)
    print('Status: 302')
    print('Location: /')
    print(f'Set-Cookie: auth.session-token={token}; Max-Age=3600')
    print()

try:
    if os.environ['REQUEST_METHOD'] == 'POST':
        username = os.environ.get("USERNAME")
        password = os.environ.get("PASSWORD")
        if username == None or password == None:
            show_auth_fail()
        else:
            # if subprocess.run(['/usr/sbin/auth', username, password]).returncode != 0:
            if os.system(f'/usr/sbin/auth {username} {password}') != 0:
                show_auth_fail()
            else:
                login_success(username)
    else:
        show_login_form()
except:
    print('Status: 500\r\n\r\n', end='')
