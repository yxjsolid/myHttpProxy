from flask import Flask, request, make_response
from werkzeug.routing import BaseConverter
import requests
from requests import Session

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

app = Flask(__name__, static_folder="download",static_url_path='')
app.url_map.converters['regex'] = RegexConverter


ourIp = "10.103.12.150"
target = "192.168.8.1"
rawproxy = "10.103.12.31"




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
                val = val.replace(ourIp, target)
                # print val


            newHeaders[key] = str(val)

    #data = request.data
    request.environ['CONTENT_TYPE'] = 'application/something_Flask_ignores'
    data = request.get_data()

    backendURL = r"http://%s/"%rawproxy + url
    isHome = 0
    if "home.html" in url:
        isHome = 1
        #return


    if request.method == "GET":
        #print newHeaders
        r = requests.get(backendURL, headers=newHeaders, data=data, allow_redirects=False)
    elif request.method == "POST":
        s = Session()


        r = requests.post(backendURL, headers=newHeaders, data=data, allow_redirects=False)
        # help(r)

        #print r.status_code
        #print r.headers
        #print data
        #
        #print r.raw.data
        #print r.text
        #print r.content


    resp = make_response()
    # resp.headers = r.headers
    resp.status_code = r.status_code


    for key, v in r.headers.iteritems():
        # print key, v
        if key.lower() == "location":
            v = v.replace(target, ourIp)

        if key.lower() == "Content-Encoding".lower():
            #print key
            continue

        resp.headers[key] = v

    # help(resp)
    #resp.data = r.content[3:-1]
    #print r.content[3:-1]

    if isHome:
        resp.set_data(r.content[3:-1])
    else:
        resp.set_data(r.content)

    # help(resp)
    return resp



if __name__ == "__main__":
    context = ('cert.pem', 'key.pem')
    # app.run(host="10.103.12.31", port=443, debug=1, ssl_context = context)
    app.run(host=ourIp, port=80, debug=0, threaded=True)