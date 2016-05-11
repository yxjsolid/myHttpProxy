import requests




if __name__ == "__main__":
    resp = requests.get("http://192.168.8.1")

    # help(resp)
    print resp.content