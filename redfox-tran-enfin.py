import sys
from time import sleep
from workflow import Workflow, ICON_WEB, web
import re

import urllib2 
import codecs

def make_url(word):
    word = codecs.encode(word,'utf-8')
    # print type(word)
    url_Word = urllib2.quote(word)
    return url_Word
    # print "\ntype = %s \n" %type(word)
    # print "url_word = %s \n" %url_Word

#  API_KEY = 'your-pinboard-api-key'
log = None
def main(wf):
    if len(wf.args):
        query = wf.args[0]
        query = make_url(query)
        url = 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/query/eng/fin/{}'.format(query)
        log.debug(url)
        # params = dict(auth_token=API_KEY, count=20, format='json')
        r = web.get(url)

        # # throw an error if request failed
        # # Workflow will catch this and show it to the user
        r.raise_for_status()

        # # Parse the JSON returned by pinboard and extract the posts
        result = r.json()["translations"]
        if result["empty"] == False:
            for g in result["entryGroups"]:
                for e in g["entries"]:
                    wf.add_item(title=e["text"].replace("[","").replace("]",""),
                                subtitle=e["context"] if "context" in e else "",
                                arg=e["text"], valid=True,
                                icon=ICON_WEB)
        else:
            result = r.json()["definitions"]["entryGroups"]
            for g in result:
                for e in g["entries"]:
                    reg = re.search(r'\|[a-z]+', e["text"]).group(0)[1:]
                    sub = re.search(r'\[.*\]', e["text"])
                    wf.add_item(title=reg,
                                subtitle=e["text"].replace(sub.group(0),reg),
                                arg=e["text"], valid=True,
                                icon=ICON_WEB)
    else:
        query = None
    # Send the results to Alfred as XML
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))


# curl 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/query/fin/eng/apuva' \
#   -H 'authority: api.redfoxsanakirja.fi' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'dnt: 1' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36' \
#   -H 'sec-gpc: 1' \
#   -H 'origin: https://redfoxsanakirja.fi' \
#   -H 'sec-fetch-site: same-site' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'referer: https://redfoxsanakirja.fi/' \
#   -H 'accept-language: en-US,en;q=0.9' \
#   --compressed