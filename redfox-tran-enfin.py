import sys
from time import sleep
from workflow import Workflow, ICON_WEB, web
import re

import urllib2 
import codecs

def make_url(word):
    word = codecs.encode(word,'utf-8')
    url_Word = urllib2.quote(word)
    return url_Word

log = None
def main(wf):
    if len(wf.args):
        query = wf.args[0]
        query = make_url(query)
        url = 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/query/eng/fin/{}'.format(query)
        log.debug(url)
        r = web.get(url)

        r.raise_for_status()

        result = r.json()["translations"]
        if result["empty"] == False:
            for g in result["entryGroups"]:
                for e in g["entries"]:
                    wf.add_item(title=e["text"].replace("[","").replace("]",""),
                                subtitle=e["context"] if "context" in e else "",
                                arg=e["text"], valid=True,
                                icon=ICON_WEB)
        elif r.json()["definitions"]["empty"] == False:
            log.debug(r.json()["definitions"]["empty"])
            result = r.json()["definitions"]["entryGroups"]
            for g in result:
                for e in g["entries"]:
                    reg = re.search(r'\|[a-z]+', e["text"]).group(0)[1:]
                    sub = re.search(r'\[.*\]', e["text"])
                    wf.add_item(title=reg,
                                subtitle=e["text"].replace(sub.group(0),reg),
                                arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/eng/fin/{}".format(query), valid=True,
                                icon=ICON_WEB)
    else:
        query = None
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
