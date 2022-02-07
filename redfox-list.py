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
        log.debug(query)
        query = make_url(query)
        if len(query) > 0:
            url = 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/autocomplete/fin/{}'.format(query)
            log.debug(url)
            r = web.get(url)
            r.raise_for_status()
            result = r.json()
            for w in result:
                wf.add_item(title=w, arg=w, valid=True,)
    else:
        query = None
    wf.send_feedback()


if __name__ == u"__main__":
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
