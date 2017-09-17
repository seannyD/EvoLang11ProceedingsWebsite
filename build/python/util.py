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


def getTemplate(name):
	o = open("../templates/"+name)
	d = o.read()
	o.close()
	return d
