import simHash
import urllib2

def get_content(url):
#    get latest the content of an url
    res = "none"

    if url.find("http://") == -1:
        url = "http://" + url

    try:
        # Open the URL
        pageToVisit = urllib2.urlopen(urllib2.Request(url, headers={
            # Change user agent.
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.17 (KHTML, like Gecko) "
                          "Chrome/24.0.1312.57 Safari/537.17",
            # Only html and xhtml are acceptable for the response.
            # If the server cannot send a response which is acceptable according to the combined Accept field value,
            # then the server SHOULD send a 406 (not acceptable) response.
            "Accept": "text/html,application/xhtml+xml"
        }), timeout=5)
        res = pageToVisit.read()
        pageToVisit.close()
    except Exception:
        pass
    
    return res
hash_content = []

def check_content(Content):
    """Check is there any similar content visited before
        
        Use SimHash compute a 128 bit hash number. Compute Hamming distance to decide whether they are similar
        """
    global hash_content
    return True
    hash = simHash.simhash(Content.split())
    for x in hash_content:
        if hash.hamming_distance(x) < 1:
            print "Similar Page Found !!!"
            return False
    hash_content.append(hash)
    return True;

def check_result(terms, result_set):
#    check the result set, if all page is open-able
#    also show a sample 140 char of result page
    global hash_content
    hash_content = []
    res = []
    for r in result_set:
        # did, url, score
        content = get_content(r[1])
        if not check_content(content) and content != "none":
            # res.append(r)

            # give a simple content
            res_sub_str = content[0: min(len(content), 140) ]
            res_sub_str_num = -1
            for term in terms:
                i = content.find(term)
                if i == -1:
                    continue
                sub_str = content[i: min(len(content), (i+140)) ]
                cc = 0
                for term2 in terms:
                    if sub_str.find(term2):
                        cc += 1
                if cc > res_sub_str_num:
                    res_sub_str = sub_str
                    res_sub_str_num = cc
#            print res_sub_str
            res.append( (r, res_sub_str) )
    return res











