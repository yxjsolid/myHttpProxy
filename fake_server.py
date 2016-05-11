from flask import Flask, request, make_response
from werkzeug.routing import BaseConverter
import requests

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__, static_folder="download",static_url_path='')
app.url_map.converters['regex'] = RegexConverter

target = "10.103.12.251"

@app.route('/<regex(".*"):url>', methods=['GET','POST'])
def test(url):
    # print request.headers
    # print request.data

    # print request.method
    # print request.host
    # print request.path
    # print request.environ["SERVER_PROTOCOL"]

    newHeaders = {}
    for key, val in request.headers:
        if val:
            if key.lower() == "host":
                val = target

            if key.lower() == "referer":
                val = val.replace('10.103.12.31', target)
                # print val


            newHeaders[key] = str(val)

    data = request.data

    backendURL = r"http://%s/"%target + url
    if request.method == "GET":
        print newHeaders
        r = requests.get(backendURL, headers=newHeaders, data=data, allow_redirects=False)
    elif request.method == "POST":
        # print newHeaders
        r = requests.post(backendURL, headers=newHeaders, data=data, allow_redirects=False)
        # help(r)
        # print r.status_code
        # print r.headers
        #
        # print r.raw.data
        # print r.text
        # print r.content


    resp = make_response()
    # resp.headers = r.headers
    resp.status_code = r.status_code


    for key, v in r.headers.iteritems():
        # print key, v
        if key.lower() == "location":
            v = v.replace(target, '10.103.12.31')

        if key.lower() == "Content-Encoding".lower():
            print key
            continue

        resp.headers[key] = v

    # help(resp)
    resp.data = r.content

    resp.set_data(r.content)

    # help(resp)
    return resp



if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    # app.run(host="10.103.12.31", port=443, debug=1, ssl_context = context)
    app.run(host="10.103.12.31", port=80, debug=0, threaded=True)