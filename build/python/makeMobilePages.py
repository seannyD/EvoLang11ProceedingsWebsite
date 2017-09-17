from util import *

def makeMobilePages(pages,toc):
    pids = pages.keys()
    pids.sort()
    out = ""
    detailsOut = ''
    for p in pids:
        page = pages[p]
        idx = "ABS_paper"+str(p[1])
        page = page.replace("__TOPID__",idx)
        tx = toc[p]
        detailsOut += page + "\n"
        out += tx + "\n"

    mout = getTemplate("mobileTemplate.html")
    mout = mout.replace("__TOC__",out)
    mout = mout.replace("__DETAILS__",detailsOut)
    for f in ["../../web/mobile/index.php","../../web/mobile/index.html"]:
        o = open(f,'w')
        o.write(mout)
        o.close()


#titles[k][0], authors[k],k, topics[k]
def mobileTocEntry(title,authors,k,topics):
    tx = tocEntry(title,authors,k,topics)
    tx = tx.split("\n")
    #<div id="paper178">
    
    pid = tx[0][tx[0].index('"')+1:-2]
    tx[0] = '<div id="'+pid + '" onclick="openDetails(\''+pid+'\')">'
    tx[2] = "<a>"
    return("\n".join(tx))
