from flask import Flask
# from OpenSSL import SSL


from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

import requests

app = Flask(__name__)

@app.route("/")
def hello():
    # return redirect(url_for('index1.html', filename='index1.html'), code=301)
    # return redirect(url_for('index1.html'), code=301)

    return render_template('index1.html')

@app.route("/test/a/b/c/proxy.html")
def proxy():

    resp =  requests.get("http://192.168.8.1")

    # help(resp)
    return resp.content



if __name__ == "__main__":


    context = ('cert.pem', 'key.pem')
    app.run(host="10.103.12.31", port=443, debug=1, ssl_context = context)

    # app.run(host="127.0.0.1", port=80, debug=1, )