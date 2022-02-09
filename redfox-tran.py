from cgitb import text
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
        url = 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/query/{}/{}'.format(wf.args[1], query)
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
            result = r.json()["definitions"]["entryGroups"]
            for g in result:
                for e in g["entries"]:
                    try:
                        reg = re.search(r'\|[a-z]+', e["text"]).group(0)[1:]
                        sub = re.search(r'\(.*?\)', e["text"])
                        wf.add_item(title=reg,
                                    subtitle=e["text"].replace(sub.group(0),reg),
                                    arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/{}/{}".format(wf.args[1], query), valid=True,
                                    icon=ICON_WEB)
                    except:
                        wf.add_item(title=e["text"],
                                    subtitle=e["text"],
                                    arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/{}/{}".format(wf.args[1], query), valid=True,
                                    icon=ICON_WEB)
        else:
            for s in r.json()["suggestion"]:
                log.debug(s)
                wf.add_item(title=s,
                            arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/{}/{}".format(wf.args[1], s), valid=True,
                            icon=ICON_WEB)
        if r.json()["redfoxSecondaryTermbankTranslations"]["empty"] == False:
            result = r.json()["redfoxSecondaryTermbankTranslations"]["entryGroups"]
            for g in result:
                for e in g["entries"]:
                    wf.add_item(title=e["text"],
                                subtitle=e["context"] if "context" in e else "",
                                arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/{}/{}".format(wf.args[1], query), valid=True,
                                icon=ICON_WEB)
    else:
        query = None
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
