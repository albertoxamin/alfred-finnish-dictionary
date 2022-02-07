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
        log.debug(query)
        query = make_url(query)
        if len(query) > 2:
            url = 'https://api.redfoxsanakirja.fi/redfox-api/api/basic/autocomplete/fin/{}'.format(query)
            log.debug(url)
            # params = dict(auth_token=API_KEY, count=20, format='json')
            r = web.get(url)

            # # throw an error if request failed
            # # Workflow will catch this and show it to the user
            r.raise_for_status()

            # # Parse the JSON returned by pinboard and extract the posts
            result = r.json()

            # # Loop through the returned posts and add an item for each to
            # # the list of results for Alfred
            for w in result:
                w1 = make_url(w)
                log.debug(w)
                new_url = "https://api.redfoxsanakirja.fi/redfox-api/api/basic/query/fin/eng/{}".format(w1)
                # encode url for finnish characters
                # new_url = new_url.decode('iso-8859-1')
                log.debug(new_url)

                # try:
                # res = web.get(new_url).json()
                # if "word2" in res["subtitleResult"]["query"]:
                wf.add_item(title=w,
                            arg=w, valid=True,
                                # arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/fin/eng/"+w,
                                # subtitle=str(res["subtitleResult"]["query"]["word2"]),
                                icon=ICON_WEB)
                # elif "definitionsInDestLanguage" in res:
                    # wf.add_item(title=w,
                                # arg="https://redfoxsanakirja.fi/fi/sanakirja/-/s/fin/eng/"+w,
                    #             subtitle=res["definitionsInDestLanguage"]["entryGroups"]["entries"][0]["text"],
                    #             icon=ICON_WEB)
                    # pass
                # except:
                #     pass
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