from random import randint, choice
from string import ascii_letters

from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException

# ref
# https://stackoverflow.com/questions/21498694/flask-get-current-route

# ---------- init ---------- #

app = Flask(__name__)

gusp_dict = {}
gusp_set = set()

# ---------- Flask ---------- #


@app.route('/', methods=['POST'])
def fn_root():
    try:
        # print('headers', request.headers)
        # print('data', request.data)
        # print()

        if request.headers.get('Content-Type') == 'application/gusp':

            _str = request.data
            _str = _str.decode()[6:-7].split('|')

            _len, _url = 0, ""
            if len(_str) == 3:
                _, _len, _url = _str
            elif len(_str) == 4:
                _, _len, _url, _ = _str
            else:
                print('Regular expression mismatch')

            if int(_len) != len(_url):
                print(f"Length mismatch: {_len} vs {len(_url)}")

            # --- GUSP --- #

            status = ""
            length = 0
            content = ""

            if _url in gusp_set:
                status = 'ERROR'
            else:
                status = 'SUCCESS'
                length = randint(11, 15)
                content = ''.join(choice(ascii_letters) for _ in range(length))

                gusp_dict[content] = _url
                gusp_set.add(_url)

            # --- Response --- #

            res = Response(
                response=f"[gusp]{status}|{length}|{content}[/gusp]",
                status='200')
            res.headers['Content-Type'] = 'application/gusp'

            return res

    except Exception as e:
        print('ERROR | fn_root', e)

    return ''


@app.route('/<shorten_str>', methods=['GET'])
def fn_redirect(shorten_str):
    try:
        # print('shorten_str', shorten_str)
        # print()

        _url = gusp_dict.get(shorten_str)

        if _url is not None:
            res = Response(response="", status='302')
            res.headers['Content-Type'] = 'application/gusp'
            res.headers['Location'] = _url

            return res
        else:
            res = Response(response="", status='404')
            res.headers['Content-Type'] = 'application/gusp'

            return res

    except Exception as e:
        print('ERROR | fn_redirect', e)

    return ''


@app.route('/alias', methods=['GET'])
def fn_alias():
    try:
        # print('shorten_str', shorten_str)
        # print()

        res = Response(response="", status='302')

        return res

    except Exception as e:
        print('ERROR | fn_alias', e)

    return ''


@app.route('/flag', methods=['GET'])
def fn_flag():

    flag = request.args.get("flag")
    print('flag', flag)

    return ''


# ---------- errorhandler ---------- #


@app.errorhandler(Exception)
def handle_error(e):
    code = ''

    if isinstance(e, HTTPException):

        print('handle_error', e, request)
        print(request.headers)

        code = e.code

    return str(code), code


# ---------- main ---------- #


def main():
    print('server init; host: 0.0.0.0 port: 3000')
    app.run(debug=False, host='0.0.0.0', port=3000)
    return


if __name__ == '__main__':
    main()
