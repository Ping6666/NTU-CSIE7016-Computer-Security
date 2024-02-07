#!/usr/bin/python3

import os
import subprocess

def show_login_form():
    print('Status: 200')
    print('Content-type: text/html')
    print()
    print('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Set Passowrd</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
        <script>
            function deleteAndRedirect() {
                fetch(window.location.href, {
                    method: 'POST',
                }).then(() => {
                    window.location.href = "/cgi-bin/login.cgi";
                })
            }
            
            var result = confirm("Want to set password?");
            if (!result) {
                deleteAndRedirect();
            }
        </script>
    </head>
    <body>
        <section class="section">
            <div class="container" style="max-width: 400px;">
                <h1 class="title">Set Password</h1>
                <form action="/cgi-bin/set_password.cgi" method="post">
                    <div class="field">
                        <label class="label" for="password">Password:</label>
                        <div class="control">
                            <input class="input" type="password" id="password" name="password" required>
                        </div>
                    </div>
                    <div class="field">
                        <div class="control">
                            <button class="button is-primary">Set</button>
                        </div>
                    </div>
                </form>
            </div>
        </section>
    </body>
    </html>

    ''')

def set_success():
    print('Status: 200')
    print('Content-type: text/html')
    print()
    print('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Password Change Success</title>
        <script>
            alert("Password change success");
            window.location = "/cgi-bin/login.cgi";
        </script>
    </head>
    <body>
        <p>Password change successful. Redirecting...</p>
    </body>
    </html>
    ''')

def redirect_login():
    print('Status: 302')
    print('Location: /cgi-bin/login.cgi')
    print()

try:
    changeFile = os.path.expanduser("~/.local/ais3eof-firmware/change")
    if os.path.exists(changeFile) == False:
        redirect_login()

    elif os.environ['REQUEST_METHOD'] == 'POST':
        os.remove(changeFile)
        password = os.environ["PASSWORD"]
        if password != None:
            if subprocess.run(['/usr/sbin/chpass', password]).returncode == 0:
                set_success()
        else:
            redirect_login()
    else:
        show_login_form()
except:
    print('Status: 500\r\n\r\n', end='')
