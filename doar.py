import sys
import json
import re
import urllib.request

URL = "http://www.israelpost.co.il/itemtrace.nsf/trackandtraceNDJSON?openagent&lang=EN&itemcode=%s"
HTTP_USER_AGENT = "Mozilla/5.0 (X11; U; Slackware Linux x86_64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61 Safari/537.36"

def http_get_request(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', HTTP_USER_AGENT), ("Accept", "*/*")]
    try:
        return opener.open(url).read().decode()
    except Exception as e:
        return None

def parse(data):
    data = json.loads(data)['itemcodeinfo']
    tags = re.findall(r'<tr>(.*?)</tr>', data)
    try:
        # remove header
        header = tags.pop(0)
    except Exception as e:
        sys.stdout.write("error: invalid tracking number.\n")
        sys.exit(0)

    for tag in tags[::-1]:
        col = re.findall(r'<td>(.*?)</td>', tag)
        for item in col:
            if col[-1] == item:
                sys.stdout.write("%s." % (item))
                break
            if item:
                sys.stdout.write("%s -> " % (item))
        sys.stdout.write("\n")

def track(tracking_number=None):
    url = "%s" % (URL % (tracking_number))
    data = http_get_request(url)
    parse(data)

def main():
    if len(sys.argv) < 2:
        sys.stdout.write("Usage: %s [tracking number] ...\n" % (sys.argv[0]))
        sys.exit(1)
    track(sys.argv[1])

if __name__ == '__main__':
    main()
