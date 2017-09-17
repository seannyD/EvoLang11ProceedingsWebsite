#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv,os,string,shutil
from makeLatexBooklet_2016 import *
from addCopyrightToPDF import *
from makeMobilePages import *
from util import *

papersToAvoidAddingAbstract = []
#  Equal contributions: Dictionary with paper number, and index of authors that contributed equally
authorsContributedEqually = {"120":[0,1,2], "131":[0,1]}
avoidAddingSupplementary = ["49"]
avoidAddingCopyrightNotice = ["25"]

charReplacements = [("ı","ZZZ1","&#305;"), ("é","ZZZ2","&#233;"),("ö","ZZZ3","&#246;")]

webaddress = "http://evolang.org/neworleans/papers/"
#"http://evolang.org/proc/evolang11/papers/"

writeTopicsPage = False
nowAddCopyrightToPDF = True


specialReplacements = [("(tursiops Truncatus)","(<i>Tursiops Truncatus</i>)"),("Hmm","HMM"),("Mri","MRI"),('Fmri','fMRI')]

def addToDict(x,dict,key):
	try:
		dict[key].append(x)
	except:
		dict[key] = [x]


def u2html(x):

# 	x = x.replace("\n","<br />")
# 	for r in charReplacements:
# 		x = x.replace(r[0],r[1])
# 	try:
# 		x = x.encode('utf-8', 'xmlcharrefreplace')
# 	except:
# 		pass
# 	for r in charReplacements:
# 		x = x.replace(r[1],r[2])
# 	return x
	return x


def getMetaData():

	authors = {}
	for afile in ["../meta/author.csv","../plenaryPapers/authorPlenary.csv"]:
		f = open(afile, 'rt')
		reader = csv.DictReader(f)
		for row in reader:
			fname = u2html(row["first name"])
			lname = u2html(row["last name"])
			affil = u2html(row["organization"])
			#addToDict([fname + " " + lname,affil],authors,row["submission #"])
			addToDict([(lname,fname),affil],authors,row["submission #"])
		f.close()

	titles = {}
	keywords = {}
	abstracts = {}
	tweets = {}
	submissionIsFullPaper = {}

	for sfile in ["../meta/submission.csv","../plenaryPapers/submissionPlenary.csv"]:
		f = open(sfile, 'rt')
		reader = csv.DictReader(f)
		for row in reader:
			title = cleanTitles(row["title"])
			abs = u2html(row["abstract"])
			abs = abs.replace("\n","<br /><br />")
			abs = abs.replace("<br /><br /><br /><br />","<br /><br />")
			kw = u2html(row["keywords"])
			tweet = u2html(getTweet(row["form fields"]))
			fullpaper = row["form fields"].count("FullPaper")>0
			paperNumber = row["#"]



			if len(tweet) > 140:
				print "tweet is too long",paperNumber, 140 -len(tweet)
				#print tweet
			if len(tweet) > 300:
				print "tweet is way too long",paperNumber, 140 -len(tweet)
				tweet = ""
			if len(tweet)>2:
				tweet = '<b>Short description:</b> <span style="font-style: italic;">'+tweet+'</span>'

			addToDict(title,titles,paperNumber)
			addToDict(kw,keywords,paperNumber)
			addToDict(fullpaper,submissionIsFullPaper,paperNumber)
			if paperNumber in papersToAvoidAddingAbstract:
				addToDict("",abstracts,paperNumber)
				addToDict("",tweets,paperNumber)
			else:
				addToDict(abs,abstracts,paperNumber)
				addToDict(tweet,tweets,paperNumber)
		f.close()

	topics = {}
	for tfile in ["../meta/submission_topic.csv","../plenaryPapers/submission_topicPlenary.csv"]:
		f = open(tfile, 'rt')
		reader = csv.DictReader(f)
		for row in reader:
			n = u2html(row["submission #"])
			topic = u2html(row["topic"])
			addToDict(topic,topics,n)
		f.close()

	return titles,authors,abstracts,keywords,tweets, topics, submissionIsFullPaper

def getAcceptedPapers():
	acceptedPaperNumbers = []
	f = open("../paperDecisions/DecisionsTracker - Sheet1.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		num = row["#"]

		dec = row["Final Decision"]
		cancel = row["Cancellations"]

		#if dec!="REJECT" and len(cancel)<2:
		if dec!="REJECT" and dec!='Cancel' and dec!='Preject':
			acceptedPaperNumbers.append(num)

	f.close()
	return acceptedPaperNumbers

def getLicensedPapers():
	lpapers = {}
	f = open("../paperDecisions/EvoLang publishing license (part 2) (Responses) - Form responses 1.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		num = row["Paper Number"]

		include = row["Do you wish your paper to appear in the proceedings?"]
		# todo: check that the last column really is the right one
		dec = row["If you do want your paper included (at some point):"]
		if num in lpapers.keys() and lpapers[num][1] != dec:
			print "Warning: conflicting license agreement for paper ",num
		lpapers[num] = (include,dec)
		if num=='12':
			print include,dec
	f.close()

	return lpapers



def makeAuthor(name,affiliation, equalContrib=False):

	tm = getTemplate("AuthorDivTemplate.txt")
	# name is (lastName, firstName)

	aname = name[1]+" "+name[0]
	if equalContrib:
		aname += "*"

	tm = tm.replace("__AUTHORNAME__",aname)
	tm = tm.replace("__AFFILIATION__",affiliation)
	return tm

def makeAuthorBlock(authors,equalContrib):

	affils = []
	for name,affil in authors:
		if not affil in affils:
			affils.append(affil)

	out = ""
	for i, author in enumerate(authors):
		affil = str(affils.index(author[1])+1)
		if len(affils)==1:
			affil = ""
		out += makeAuthor(author[0],affil,i in equalContrib)

		if i < (len(authors)-2):
			out += ", "
		if i == (len(authors)-2):
			out += " and "

#	out = ", ".join([makeAuthor(authors[i][0],authors[i][1]) for i in range(len(authors))])
	if len(equalContrib)>0:
		out += "<br /> * These authors contributed equally to the work\n"
	if len(affils) > 1:
		for i,affil in enumerate(affils):
			out += '<br /><span class="affiliation">'+str(i+1)+ " " + affil + "</span>\n"
	else:
		out +=     '<br /><span class="affiliation">' +               affils[0] + "</span>\n"

	return out

def makeFileLinks(links,openInNewTab=False):
	links = ["../pdf/"+x for x in links]
	tm = '<p><a href="XX">Download Paper (pdf)</a></p>'
	if openInNewTab:
		tm = '<p><a target="_blank" href="XX">Download Paper (pdf)</a></p>'
	tm = tm.replace("XX",links[0])
	if len(links)>1:
		supx = '\n<p><a href="XX">Supplementary Materials (zip)</a></p>'
		if openInNewTab:
			supx = '\n<p><a target="_blank" href="XX">Supplementary Materials (zip)</a></p>'
		supx = supx.replace("XX",links[1])
		tm += supx
	return tm


def formatKeywords(k):
	k = k[0].replace("\n",", ")
	if k.endswith(", "):
		k = k[:-2]
	return k

def getTweet(x):
	tx = x.split("(Tweet)")[1]
	return tx

def cleanTitles(x):
	sx = string.capwords(x)
	for t,r in specialReplacements:
		sx = sx.replace(t,r)
	return sx

def makePage(paperNumber, papertitle, authors,keywords,abstract,links, tweet,toc, equalContrib, license, includeTOC=True, xtemplate="papertemplate.html"):

	p = getTemplate(xtemplate)

	#header = getTemplate("HeaderTemplate.txt")
	#p = p.replace("XXHEADER",header)

	p = p.replace("XXPAPERTITLE",papertitle)
	if(includeTOC):
		p = p.replace("__TOC__",toc)
	else:
		p = p.replace("__TOC__","")


	authorBlock = makeAuthorBlock(authors,equalContrib)
	p = p.replace("XXAUTHORS",authorBlock)
	p = p.replace("XXKEYWORDS",formatKeywords(keywords))
	p = p.replace("XXABSTRACT",abstract)
	p = p.replace("XXLINKS",links)

	citation = makeCitation(papertitle,authors, paperNumber)
	bibcitation = makeBibtexCitation(papertitle,authors,paperNumber)
	writeBibCitation(bibcitation,paperNumber)
	p = p.replace("XXCITATION",citation)
	p = p.replace("XXBIBCITATION",'<a href="../bib/'+paperNumber+'.bib">Bibtex file</a>')

	p = p.replace("XXTWEET",tweet)


	licenseT = makeLicense(license[1], authors)
	p = p.replace("XXLICENSE",licenseT)
	p = p.replace("__SCROLLID__","paper"+str(paperNumber))

	paperPdfLoc = "../submissions/EVOLANG_11_paper_"+paperNumber+".pdf"
	if paperNumber.startswith("p"):
		paperPdfLoc = "../plenaryPapers/pdf/EVOLANG_11_paper_"+paperNumber+".pdf"
	paperPdfDest = "../submissions_with_copyright/EVOLANG_11_paper_"+paperNumber+".pdf"
	paperPdfCopyright = makeLicenseText(license[1], authors)

	addC = not paperNumber in avoidAddingCopyrightNotice
	simpleAuthorString = ", ".join([a[0][1]+" "+a[0][0] for a in authors])

	if nowAddCopyrightToPDF:
		addCopyrightToPDF(paperPdfLoc,paperPdfDest,paperPdfCopyright,addC,papertitle,simpleAuthorString)

	#p = p.replace("XXBACKTOTOC",'<a href="../index.html">Back to Table of Contents</a>')

	return p

def makeCitation(title,authors,paperNumber):
	authorString = ""
	for i, author in enumerate(authors):
		authorString += author[0][0] + " " + " ".join([x[0]+"." for x in author[0][1].split(" ")])
		if i < (len(authors)-2):
			authorString += ", "
		if i == (len(authors)-2):
			authorString += " and "


	tm = getTemplate("TexCitationTemplate.txt")
	tm = tm.replace("__TITLE__",title)
	tm = tm.replace("__AUTHORS__", authorString)
	tm = tm.replace("__HANDLE__", "Available online: "+webaddress +paperNumber+".html")
	return tm

def makeBibtexCitation(title,authors,paperNumber):
	tm = getTemplate("bibTexTemplate.txt")

	astring = 	" and ".join([x[0][0]+", "+x[0][1] for x in authors])

	tm = tm.replace("__CITEKEY__",'evolang11_'+str(paperNumber))
	tm = tm.replace("__AUTHORS__", astring)
	tm = tm.replace("__TITLE__",title)
	tm = tm.replace("__ADDRESS__",webaddress +paperNumber+".html")
	return tm


def writeBibCitation(bibcitation,paperNumber):
	o = open("../../web/bib/"+str(paperNumber)+".bib",'w')
	o.write(bibcitation)
	o.close()


def makeLicense(licenseType,authors):
	out = ""
	if licenseType == "Creative Commons CC BY license (preferred)":
		out = getTemplate("ccLicenseTemplate.txt")
	if licenseType == "Creative Commons CC BY-NC-ND license":
		out = getTemplate("cc-by-nc-nd-LicenseTemplate.txt")
	if licenseType == "CC BY-NC-SA":
		out = getTemplate("byncsaLicense.txt")
	# surnames
	name = ", ".join([x[0][0] for x in authors])
	out += "<br />&copy; " + name + " 2016"
	return out
def makeLicenseText(licenseType,authors):
	out = ""
	if licenseType == "Creative Commons CC BY license (preferred)":
		out = "This work is licensed under a Creative Commons Attribution 4.0 International License."
	if licenseType == "Creative Commons CC BY-NC-ND license":
		out = "This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License."
	if licenseType == "CC BY-NC-SA":
		out = "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."
	# surnames
	name = ", ".join([x[0][0] for x in authors])

	out += "\n© " + name + " 2016"
	return out

def makeTopicCheckbox(t):
	tp = """<input type="checkbox" id="__NAME__" onchange="changeCheckbox('__NAME__')">__NAME__</input>"""
	tp = tp.replace("__NAME__",t.lower())
	return tp

def listToTable(lx):
	  cols = ["",""] # hard coded 2 columns
	  out = "<table>\n<tr>\n"
	  for i,l in enumerate(lx):

	  	out += "<td>"+l+"</td>\n"
	  	if (i % 2) == 1:
	  		out += "</tr>\n<tr>\n"
	  out = out[:-5] + "\n</table>"
	  return out


def makeTopicCheckboxes(topicBody):
	tx = sorted([makeTopicCheckbox(x) for x in topicBody.keys()])
	return listToTable(tx)
	#return "<br />".join(sorted([makeTopicCheckbox(x) for x in topicBody.keys()]))


def writePage(page,paperNumber):
	o = open("../../web/papers/"+paperNumber+".html",'w')
	o.write(page)
	o.close()

def tocEntry(title,authors,number, pTopics):
	authors = ", ".join([x[0][1]+" "+x[0][0] for x in authors])
	link = "../papers/"+number+".html"
	tm = getTemplate("TOCTemplate.txt")
	tm = tm.replace("__TITLE__",title)
	tm = tm.replace("__AUTHORS__",authors)
	tm = tm.replace("__LINK__",link)
	tm = tm.replace("__PAPERID__","paper"+str(number))
	pTopics = ", ".join(pTopics)
	tm = tm.replace("__TOPICS__",pTopics)
	return tm

def makePages():

	titles,authors,abstracts,keywords,tweets, topics, submissionIsFullPaper = getMetaData()

	toc = ""
	tocarray = []
	topicBody = {}
	authorsBody = {}

	acceptedPapers =getAcceptedPapers()
	licensedPapers = getLicensedPapers()

	files = os.listdir("../submissions/")

	print "Missing licences:"
	missingL = []
	for k in acceptedPapers:
		if not (k in licensedPapers.keys()):
			missingL.append(int(k))
	missingL.sort()

	for l in missingL:
		print l

	mobileTocs = {}

	# Make toc (which needs to go in each page)
	for k in licensedPapers.keys():
		# if the paper was accepted and authors have agreeed to license it
		if k in acceptedPapers and licensedPapers[k][0]!="No":
			tocx = tocEntry(titles[k][0], authors[k],k, topics[k])
			mobileKey= (authors[k][0][0],k)
			mobileTocs[mobileKey] = mobileTocEntry(titles[k][0], authors[k],k, topics[k])
			toc += tocx
#			surname = authors[k][0][0].split(" ")[-1]
#			surname = authors[k][0][0]
			# authors[k][0] is (lastName, firstName)
			tocarray.append([authors[k][0],tocx])
	# sort toc by author surname
	tocarray.sort()
	toc = "\n".join([x[1] for x in tocarray])


	# not using search yet
	#searchpage=getTemplate("search.html")
	#searchpage=searchpage.replace("__TOC__",toc)
	#o = open("../../web/search.html",'w')
	#o.write(searchpage)
	#o.close()

	mobilePages = {}



	# make individual paper pages
	for k in licensedPapers.keys():
		if k in acceptedPapers:
			links = ""
			if (not k in papersToAvoidAddingAbstract):
				if licensedPapers[k][0]=="Yes":
					links = ["EVOLANG_11_paper_"+k+".pdf"]
					if not links[0] in files:
						print "No paper file for "+k
					supp = "EVOLANG_11_SupplementaryMaterials_"+k+".zip"
					if supp in files and (not k in avoidAddingSupplementary):
						links.append(supp)
					supp = "EVOLANG_11_SupplementaryMaterials_"+k+".tgz"
					if supp in files and (not k in avoidAddingSupplementary):
						links.append(supp)
					links = makeFileLinks(links,True)
					#copyPDFS(k)  # done later, after we've made a pdf with an added copyright notice

					addPaperToLatex(titles[k][0],authors[k],k,submissionIsFullPaper[k][0])




			abstractx = abstracts[k][0]
			tweetx = tweets[k][0]
			if licensedPapers[k][0]!="Yes":
				abstractx = ""
				tweetx = ""

			equalContrib = []
			if k in authorsContributedEqually.keys():
				equalContrib = authorsContributedEqually[k]
			page = makePage(k,titles[k][0], authors[k], keywords[k],abstractx, links, tweetx,toc, equalContrib, licensedPapers[k])
			writePage(page,k)
			mobileKey= (authors[k][0][0],k)
			mobilePages[mobileKey] = makePage(k,titles[k][0], authors[k], keywords[k],abstractx, links, tweetx,toc, equalContrib, licensedPapers[k], False, "mobilePageTemplate.html")



			if k in acceptedPapers:
				if (not k in papersToAvoidAddingAbstract):
					if licensedPapers[k][0]=="Yes":
						copyTexPDFS(k)
						copyPDFS(k)



			# add toc entry to topics sections
			if k in topics.keys():
				for topic in topics[k]:
					try:
						topicBody[topic] += tocx
					except:
						topicBody[topic] = tocx


			for author in authors[k]:
				try:
					authorsBody[author[0]] += tocx
				except:
					authorsBody[author[0]] = [tocx]

	makeMobilePages(mobilePages,mobileTocs)

	topicbody = ""
	topiclinks = ""

	for topic in sorted(topicBody.keys()):

		top = getTemplate("TopicEntryTemplate.txt")
		top = top.replace("__TOPICTITLE__",topic)
		top = top.replace("__TOPICCONTENTS__",topicBody[topic])
		topicbody += top + "\n"
		topiclinks += '<a href="#'+topic+'">'+topic+'</a><br />'

	topicpage = getTemplate("TopicPageTemplate.txt")
	topicpage = topicpage.replace("__TOPICBODY__",topicbody)
	topicpage = topicpage.replace("__TOPICLIST__",topiclinks)

	header = getTemplate("HeaderTemplate.txt")
	topicpage = topicpage.replace("__HEADER__",header)


	if writeTopicsPage:
		o = open("../../web/topics.html",'w')
		o.write(topicpage)
		o.close()

	topicCheckboxes = makeTopicCheckboxes(topicBody)

	# Now that we have the topics, we can write the toc page
	tocpage = getTemplate("toc.html")
	tocpage = tocpage.replace("__TOC__",toc)
	tocpage = tocpage.replace("__TOPICCHECKBOXES__",topicCheckboxes)
	o = open("../../web/toc/toc.html",'w')
	o.write(tocpage)
	o.close()

	authorItems = ""
	# TODO: make author entries with authorsBody
#	for author in akeys:



def removePDFS():
	for x in os.listdir("../../web/pdf/"):
		if x.endswith(".pdf") or x.endswith(".zip") or x.endswith(".tgz"):
			os.remove("../../web/pdf/"+x)

def removePaperPages():
	for x in os.listdir("../../web/papers/"):
		if x.endswith(".html"):
			os.remove("../../web/papers/"+x)

def copyPDFS(k):

	px = "EVOLANG_11_paper_"+k+".pdf"
	sx = "EVOLANG_11_SupplementaryMaterials_"+k+".zip"
	sx2 = "EVOLANG_11_SupplementaryMaterials_"+k+".tgz"
	shutil.copyfile("../submissions_with_copyright/"+px,"../../web/pdf/"+px)
	try:
			shutil.copyfile("../submissions/"+sx,"../../web/pdf/"+sx)
	except:
		pass
	try:
		shutil.copyfile("../submissions/"+sx2,"../../web/pdf/"+sx2)
	except:
		pass

def copyHTMLtoPHP():
	shutil.copyfile("../../web/index.html","../../web/index.php")


removePDFS()
removePaperPages()
makePages()
copyHTMLtoPHP()

makeReviewerList()

tex = makeTex()
writeTex(tex)
fixLatex()
fixBibTex()
