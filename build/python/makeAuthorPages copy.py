#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv,os,string,shutil

charReplacements = [("ı","ZZZ1","&#305;"), ("é","ZZZ2","&#233;"),("ö","ZZZ3","&#246;")]

def addToDict(x,dict,key):
	try:
		dict[key].append(x)
	except:
		dict[key] = [x]

# TODO: convert strange characters properly
def u2html(x):

	x = x.replace("\n","<br />")
	for r in charReplacements:
		x = x.replace(r[0],r[1])
	try:
		x = x.encode('utf-8', 'xmlcharrefreplace')
	except:
		pass
	for r in charReplacements:
		x = x.replace(r[1],r[2])
	return x


def getMetaData():

	authors = {}
	f = open("../meta/author.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		fname = u2html(row["first name"])
		lname = u2html(row["last name"])
		affil = u2html(row["organization"])
		addToDict([fname + " " + lname,affil],authors,row["submission #"])
	f.close()

	titles = {}
	keywords = {}
	abstracts = {}
	tweets = {}

	f = open("../meta/submission.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		title = cleanTitles(row["title"])
		abs = u2html(row["abstract"])
		kw = u2html(row["keywords"])
		tweet = u2html(getTweet(row["form fields"]))

		addToDict(title,titles,row["#"])
		addToDict(kw,keywords,row["#"])
		addToDict(abs,abstracts,row["#"])
		addToDict(tweet,tweets,row["#"])
	f.close()

	topics = {}
	f = open("../meta/submission_topic.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		n = u2html(row["submission #"])
		topic = u2html(row["topic"])
		addToDict(topic,topics,n)
	f.close()

	return titles,authors,abstracts,keywords,tweets, topics

def getAcceptedPapers():
	acceptedPaperNumbers = []
	f = open("../paperDecisions/DecisionsTracker - Sheet1.csv", 'rt')
	reader = csv.DictReader(f)
	for row in reader:
		num = row["#"]
		dec = row["Original Decision"]
		cancel = row["Cancellations"]

		if dec!="REJECT" and len(cancel)<2:
			acceptedPaperNumbers.append(num)

	f.close()
	return acceptedPaperNumbers

def getTemplate(name):
	o = open("../templates/"+name)
	d = o.read()
	o.close()
	return d

def makeAuthor(name,affiliation):
	tm = getTemplate("AuthorDivTemplate.txt")
	tm = tm.replace("__AUTHORNAME__",name)
	tm = tm.replace("__AFFILIATION__",affiliation)
	return tm

def makeAuthorBlock(authors):
	return "\n".join([makeAuthor(authors[i][0],authors[i][1]) for i in range(len(authors))])

def makeFileLinks(links):
	links = ["../pdf/"+x for x in links]
	tm = '<p><a href="XX">Download Paper</a></p>'
	tm = tm.replace("XX",links[0])
	if len(links)>1:
		tm += '\n<p><a href="XX">Supplementary Materials</a></p>'.replace("XX",links[1])
	return tm


def formatKeywords(k):
	k = k[0].replace("<br />",", ")
	if k.endswith(", "):
		k = k[:-2]
	return k

def getTweet(x):
	return x.split("(Tweet)")[1]

def cleanTitles(x):
	return string.capwords(x)

def makePage(papertitle, authors,keywords,abstract,links, tweet):

	p = getTemplate("PaperPageTemplate.html")

	header = getTemplate("HeaderTemplate.txt")
	p = p.replace("XXHEADER",header)

	p = p.replace("XXPAPERTITLE",papertitle)

	authorBlock = makeAuthorBlock(authors)
	p = p.replace("XXAUTHORS",authorBlock)
	p = p.replace("XXKEYWORDS",formatKeywords(keywords))
	p = p.replace("XXABSTRACT",abstract)
	p = p.replace("XXLINKS",links)

	citation = makeCitation(papertitle,authors)
	p = p.replace("XXCITATION",citation)

	p = p.replace("XXTWEET",tweet)

	p = p.replace("XXBACKTOTOC",'<a href="../index.html">Back to Table of Contents</a>')

	return p

def makeCitation(title,authors):
	authors = [x[0] for x in authors]
	tm = getTemplate("TexCitationTemplate.txt")
	tm = tm.replace("__TITLE__",title)
	tm = tm.replace("__AUTHORS__", " and ".join(authors))
	tm = tm.replace("__HANDLE__", "")


	return tm

def writePage(page,paperNumber):
	o = open("../../web/papers/"+paperNumber+".html",'w')
	o.write(page)
	o.close()

def tocEntry(title,authors,number):
	authors = ", ".join([x[0] for x in authors])
	link = "papers/"+number+".html"
	tm = getTemplate("TOCTemplate.txt")
	tm = tm.replace("__TITLE__",title)
	tm = tm.replace("__AUTHORS__",authors)
	tm = tm.replace("__LINK__",link)
	return tm

def makeTopicCheckbox(t):
	tp = """<input type="checkbox" id="__NAME__" onchange="changeCheckbox('__NAME__')">__NAME__</input>"""
	tp = tp.replace("__NAME__",t)
	return tp


def makePages():

	titles,authors,abstracts,keywords,tweets, topics = getMetaData()

	toc = ""
	tocarray = []
	topicBody = {}
	authorsBody = {}

	acceptedPapers =getAcceptedPapers()
	files = os.listdir("../submissions/")
	for k in acceptedPapers:
		links = ["EVOLANG_11_paper_"+k+".pdf"]
		if not links[0] in files:
			print "No paper file for "+k
		supp = "EVOLANG_11_SupplementaryMaterials_"+k+".zip"
		if supp in files:
			links.append(supp)
		links = makeFileLinks(links)
		page = makePage(titles[k][0], authors[k], keywords[k], abstracts[k][0], links, tweets[k][0])
		writePage(page,k)
		tocx = tocEntry(titles[k][0], authors[k],k)
		toc += tocx

		surname = authors[k][0][0].split(" ")[-1]
		tocarray.append([surname,tocx])
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
				authorsBody[author[0]] += tocx


	tocarray.sort()

	toc = "\n".join([x[1] for x in tocarray])

	topicCheckboxes = "<br />".join([makeTopicCheckbox(x) for x in topicBody.keys()])


	tocpage = getTemplate("TOCPageTemplate.txt")
	tocpage = tocpage.replace("__TOC__",toc)
	tocpage = tocpage.replace("__TOPICCHECKBOXES__",topicCheckboxes)
	o = open("../../web/toc.html",'w')
	o.write(tocpage)
	o.close()

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

	o = open("../../web/topics.html",'w')
	o.write(topicpage)
	o.close()

	authorItems = ""
	# sort keys by last name
	akeys = [(x.split(" ",x)[-1]) for x in authorsBody.keys()]
	akeys.sort()
	# TODO: make author entries
#	for author in akeys:



def removePDFS():
	for x in os.listdir("../../web/pdf/"):
		if x.endswith(".pdf") or x.endswith(".zip"):
			os.remove("../../web/pdf/"+x)

def copyPDFS(k):

	px = "EVOLANG_11_paper_"+k+".pdf"
	sx = "EVOLANG_11_SupplementaryMaterials_"+k+".zip"

	shutil.copyfile("../submissions/"+px,"../../web/pdf/"+px)
	try:
			shutil.copyfile("../submissions/"+sx,"../../web/pdf/"+sx)
	except:
		pass

removePDFS()
makePages()
