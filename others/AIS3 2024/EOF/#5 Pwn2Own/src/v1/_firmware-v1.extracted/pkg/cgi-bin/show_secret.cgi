#!/bin/bash

set -e
exec 2> /dev/null

done=
trap '{ if [[ -z $done ]]; then echo -e -n "Status: 500\r\n\r\n"; fi }' EXIT

function header(){
  cat << 'EOD'
<head>
    <title>Settings - Secret</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
    <script>
    function getCookie(cookieName) {
        const name = cookieName + "=";
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');

        for (let i = 0; i < cookieArray.length; i++) {
            let cookie = cookieArray[i].trim();
            if (cookie.indexOf(name) == 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }

        return null;
    }
    window.onload = function() {
        if (getCookie("auth.session-token") == null) {
            alert("Auth failed");
            location = "/cgi-bin/login.cgi";
        }
    };
    </script>
</head>
EOD
}

function bad_req(){
  msg="$1"
  echo -e -n 'Status: 400\r\n'
  echo -e -n 'Content-Type: text/html\r\n'
  echo -e -n '\r\n'
  header
  echo -e -n "<script language=\"javascript\">alert('$msg');window.location='$SCRIPT_NAME';</script>"
}

function gen_captcha(){
  code="$(cat /dev/urandom | tr -cd '1-9' | head -c 6)"
  web_home="$(realpath ../appweb/)"
  mkdir -p "$web_home/captcha/"
  mkdir -p "/tmp/captcha/"
  image="$(basename "$(mktemp -p "$web_home/captcha/" --suffix='.png')")"
  convert -background lightgrey -kerning -5 -attenuate 2 +noise Impulse -fill olive -pointsize 40 -size 120x -swirl 40 caption:"$code" "$web_home/captcha/$image"
  echo "$code" > "/tmp/captcha/$image.txt"
  setsid bash -c "sleep 120; rm -f '$web_home/captcha/$image' '/tmp/captcha/$image.txt';" &> /dev/null &
  echo "$image"
}

if [[ "$REQUEST_METHOD" == POST ]]; then
  cookie="$(python3 -c "from http.cookies import SimpleCookie; cookies='$HTTP_COOKIE'; cookie=SimpleCookie(); cookie.load(cookies); print(cookie['secret-captcha'].value) if 'secret-captcha' in cookie else None" 2> /dev/null)"
  if [[ -z "$cookie" || ! "$cookie" =~ ^tmp\.[0-9a-zA-Z]+\.png$ ]]; then
    echo -e -n 'Status: 302\r\n'
    echo -e -n "Location: $SCRIPT_NAME\r\n"
    echo -e -n '\r\n'
    done=1
    exit 0
  fi
  codefile="/tmp/captcha/$cookie.txt"
  if [[ ! -f "$codefile" ]]; then
    bad_req 'Session expired. Please try again.'
    done=1
    exit 0
  fi
  code="$(cat "$codefile")"
  payload="$(cat <&0)"
  input="$(echo "${payload:8}" | sed 's/^0\+//')"
  if [[ "$payload" =~ ^captcha= && "$input" -eq "$code" ]]; then
    rm -f "/tmp/captcha/$cookie.txt"
    echo -e -n 'Status: 200\r\n'
    echo -e -n 'Content-Type: text/html\r\n'
    echo -e -n '\r\n'
    secret="$(cat /etc/ais3eof-firmware/secret)"
    cat << EOD
$(header)
<body>
    <section class="section">
        <div class="container">
            <h1 class="title">Settings</h1>
            <div class="tabs">
                <ul>
                    <li><a href="/cgi-bin/control.cgi">Display</a></li>
                    <li><a href="/cgi-bin/manage.cgi">Manage</a></li>
                    <li><a href="/cgi-bin/firmware.cgi">Firmware</a></li>
                    <li class="is-active"><a href="/cgi-bin/show_secret.cgi">Show Secret</a></li>
                </ul>
            </div>

            <div class="box">
                <!-- Render secret -->
                <h2 class="subtitle">Secret</h2>
                <p><code>$secret</code></p>
            </div>

        </div>
    </section>
    <script language="javascript">setTimeout(()=>{window.location='$SCRIPT_NAME';},10000)</script>
</body>
EOD
    done=1
  else
    bad_req 'Incorrect verification code.'
    done=1
  fi
else
  image="$(gen_captcha)"
  echo -e -n 'Status: 200\r\n'
  echo -e -n 'Content-Type: text/html\r\n'
  echo -e -n "Set-Cookie: secret-captcha=$image; Max-Age=300\r\n"
  echo -e -n '\r\n'
  cat << EOD
$(header)
<body>
    <section class="section">
        <div class="container">
            <h1 class="title">Settings</h1>
            <div class="tabs">
                <ul>
                    <li><a href="/cgi-bin/control.cgi">Display</a></li>
                    <li><a href="/cgi-bin/manage.cgi">Manage</a></li>
                    <li><a href="/cgi-bin/firmware.cgi">Firmware</a></li>
                    <li class="is-active"><a href="/cgi-bin/show_secret.cgi">Show Secret</a></li>
                </ul>
            </div>

            <div class="box">
                <!-- Show captcha -->
                <div class="notification is-warning">
                    <h2 class="title">Warning!</h2>
                    <p>This page is about to display sensitive information.</p>
                    <p>Displaying secrets on a webpage is highly discouraged due to security risks.</p>
                    <p>Leaking the secret may cause your service to be compromised.</p>
                    <p>Please be sure that you want to proceed.</p>
                </div>
                <form method="POST">
                    <label class="label">Verification Code</label>
                    <div class="field has-addons">
                        <div class="control">
                            <input class="input" type="text" name="captcha" placeholder="captcha">
                        </div>
                        <div class="control">
                            <button class="button is-primary" type="submit">Submit</button>
                        </div>
                    </div>
                    <figure class="image">
                        <img src="/captcha/$image" style="width: 120; height: 52;">
                    </figure>
                </form>
            </div>

            <div class="box is-hidden">
                <!-- Render secret -->
                <h2 class="subtitle">Secret</h2>
                <p><code>JuyeNOSM5SlqD0SADeiNsSBldH0</code></p>
            </div>

        </div>
    </section>
</body>
</html>
EOD
  done=1
fi
