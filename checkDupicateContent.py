import SimHashSample

def check_content(Content):
    """Check is there any similar content visited before
        
        Use SimHash compute a 128 bit hash number. Compute Hamming distance to decide whether they are similar
        """
    global numberOfSimilar
    hash = SimHashSample.simhash(Content.split())
    for x in hash_content:
        if hash.hamming_distance(x) < 1:
            print "Similar Page Found !!!"
            numberOfSimilar += 1
            print str(numberOfSimilar)
            return False
    hash_content.append(hash)
    return True;

def check_result(result_set):
    



hash_content = []
numberOfSimilar = 0