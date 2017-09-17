#!/usr/bin/python
# -*- coding: UTF-8 -*-

# TODO: convert from UTF8 to latex

#import latexcodec  # see http://latexcodec.readthedocs.org/en/latest/quickstart.html
#import unicodedata
import codecs,sys
import csv,os,string,shutil
authorTemplate = "\\index{1_AUTHOR}"

paperTemplate = """
1_AUTHORS
\\phantomsection
\\label{paper2_PAPER_NUMBER}
\\addcontentsline{toc}{chapter}{3_PAPER_TITLE, \\newline \\textit{ 4_AUTHOR_NAMES}}

\\includepdf[height=271.76470588235293mm, pages=-,pagecommand=\\thispagestyle{plain}]{5_FILENAME}

\\cleardoublepage

"""

# the alternative template adjusts the margins of the pdf with 'offset'
alt_paperTemplate = """
1_AUTHORS

\\label{paper2_PAPER_NUMBER}
\\addcontentsline{toc}{chapter}{3_PAPER_TITLE \\newline \\textit{ 4_AUTHOR_NAMES}}

\\includepdf[height=271.76470588235293mm, pages=-,pagecommand=\\thispagestyle{plain}, offset={-0.3cm 1.1cm}]{5_FILENAME}

\\cleardoublepage

"""

reviewerTemplate = """\\noindent
X_REVIEWER \\newline"""

filebase = "pdf/"

latex_abstractList = []
latex_paperList = []


def addPaperToLatex(papertitle, authors, num, fullpaper):
	pt = paperTemplate
	ret = pt.replace("1_AUTHORS",utf8ToLatex(authorIndexString(authors)))

	ret = ret.replace("2_PAPER_NUMBER",num)
	ret = ret.replace("4_AUTHOR_NAMES",utf8ToLatex(authorList(authors)))
	ret = ret.replace("3_PAPER_TITLE",utf8ToLatex(papertitle))
	ret = ret.replace("5_FILENAME",filebase+"EVOLANG_11_paper_"+num+".pdf")


	if fullpaper:
		latex_paperList.append((authors[0],ret))
	else:
		latex_abstractList.append((authors[0],ret))

def authorIndexString(authors):
	global authorTemplate
	ret = ""
	for a in authors:
		ret += authorTemplate.replace('1_AUTHOR',a[0][0]+" "+a[0][1])+"\n"
	return ret

def authorList(authors):
	return ", ".join([x[0][1] + " " +x[0][0] for x in authors])


def makeTex():

	latex_abstractList.sort()
	latex_paperList.sort()


	tex = getTemplate("texTemplates/texBookletTemplate.tex")
	abst = "\n\n".join([x[1] for x in latex_abstractList])
	pap = "\n\n".join([x[1] for x in latex_paperList])

	tex = tex.replace("X_PAPER_LOC",pap)
	tex = tex.replace("X_ABSTRACT_LOC",abst)
	tex = tex.replace('‘','`')
	tex = tex.replace("’","'")
	return tex

def writeTex(tex):
	o = open("../../tex/evolang11.tex",'w')
	o.write(tex)
	o.close()


def copyTexPDFS(k):

	px = "EVOLANG_11_paper_"+k+".pdf"

	try:
		shutil.copyfile("../submissions_with_copyright/"+px,"../../tex/pdf/"+px)
	except:
		shutil.copyfile("../plenaryPapers/pdf/"+px,"../../tex/pdf/"+px)

def getTemplate(name):
	o = open("../templates/"+name)
	d = o.read()
	o.close()
	return d

##########


#def utf8ToLatex(text):
#	return text.encode("latex")


# http://stackoverflow.com/questions/10009753/python-dealing-with-mixed-encoding-files
import codecs

last_position = -1

def mixed_decoder(unicode_error):
    global last_position
    string = unicode_error[1]
    position = unicode_error.start
    if position <= last_position:
        position = last_position + 1
    last_position = position
    #if string[position] =="’":
    #	new_char = string[position].decode('latin1')
    #else:
    print ">>>",string
    new_char = string[position].decode("cp1252")
    #new_char = u"_"
    return new_char, position + 1

codecs.register_error("mixed", mixed_decoder)


def utf8ToLatex(text):
	return text
	print text
	#text = text.replace(u"’",'')
 	for utf,lat in latexAccents:


 		global last_position
 		last_position = -1
 		#text = text.decode('utf-8','mixed')
# 		print '---'
 		text = text.replace(utf,lat)
# 		print text
# 		print "===="
	return text
#     out = ""
#     txt = tuple(text)
#     i = 0
#     while i < len(txt):
#         char = text[i]
#         code = ord(char)
#
#         # combining marks
#         if unicodedata.category(char) in ("Mn", "Mc") and code in accents:
#             out += "\\%s{%s}" %(accents[code], txt[i+1])
#             i += 1
#         # precomposed characters
#         elif unicodedata.decomposition(char):
#             base, acc = unicodedata.decomposition(char).split()
#             acc = int(acc, 16)
#             base = int(base, 16)
#             if acc in accents:
#                 out += "\\%s{%s}" %(accents[acc], unichr(base))
#             else:
#                 out += char
#         else:
#             out += char
#
#         i += 1
#
#     return out


def fixLatex():
	fixLatex2("../../tex/evolang11.tex","../../tex/evolang11.tex")


def fixBibTex():
	bfiles = os.listdir("../../web/bib/")
	for b in bfiles:
		fixLatex2("../../web/bib/"+b)


def fixLatex2(filename,outFilename=""):
	if outFilename=="":
		outFilename = filename
	o = codecs.open(filename,'r',encoding='utf8')
	d = o.read()
	o.close()
	d = d.replace("pdf/EVOLANG_","XXYYXXYYGGHH")

	#print d[(d.index("Roland")-30):(d.index("Roland")+30)]

	#swaps = [("Ã©","\\'{e}"),("ÃŽ","\\^{o}"),("Ä±l","\\i"),("ÃŒ",'\\"{o}'),("Ã¡","\\'{a}"),("Ãš","\\`{e}"),("Ã",'\\"{u}')]
	# swaps += [("Ã¶" , "\\:{o}" )]
	# swaps += [("ÃŒ",'\\"{u}')]
	#
	# swaps += [("Ã³","\\'{o}")]
	# swaps += [("Ã«",'\\"{e}')]
	#


	# swaps = [(u"<i>",u"\\emph{"),(u"</i>",u"}")]#,(u' "',u"``")]
	# swaps += [("Slawomir","S\\l{}awomir"),("Przemyslaw","Przemys\\l{}aw"), ("Zywiczynski","\.{Z}ywiczy\'{n}ski"),("Jasinski","Jasi\'{n}ski")]
	# swaps += [("Eryilmaz","Ery{\\i}lmaz")]
	# for s in latexAccents:
	# 	d = d.replace(s[0],s[1])
	# for s in swaps:
	# 	d = d.replace(s[0],s[1])

	d = fixLatexCharacters(d)

	d = d.replace("XXYYXXYYGGHH","pdf/EVOLANG_")
	o = codecs.open(outFilename,'w',encoding='utf8')
	o.write(d)
	o.close()

def fixLatexCharacters(text):
	swaps = [(u"<i>",u"\\emph{"),(u"</i>",u"}")]#,(u' "',u"``")]
	swaps += [("Slawomir","S\\l{}awomir"),("Przemyslaw","Przemys\\l{}aw"), ("Zywiczynski","\\.{Z}ywiczy\\'{n}ski"),("Jasinski","Jasi\\'{n}ski")]
	swaps += [("Eryilmaz","Ery{\\i}lmaz")]
	for s in latexAccents:
		text = text.replace(s[0],s[1])
	for s in swaps:
		text = text.replace(s[0],s[1])
	return text



latexAccents = [
  [ u"à", "\\`a" ], # Grave accent
  [ u"è", "\\`e" ],
  [ u"ì", "\\`\\i" ],
  [ u"ò", "\\`o" ],
  [ u"ù", "\\`u" ],
  [ u"ỳ", "\\`y" ],
  [ u"À", "\\`A" ],
  [ u"È", "\\`E" ],
  [ u"Ì", "\\`\\I" ],
  [ u"Ò", "\\`O" ],
  [ u"Ù", "\\`U" ],
  [ u"Ỳ", "\\`Y" ],
  [ u"á", "\\'a" ], # Acute accent
  [ u"é", "\\'e" ],
  [ u"í", "\\'{i}" ],
  [ u"ó", "\\'o" ],
  [ u"ú", "\\'u" ],
  [ u"ý", "\\'y" ],
  [ u"Á", "\\'A" ],
  [ u"É", "\\'E" ],
  [ u"Í", "\\'\\I" ],
  [ u"Ó", "\\'O" ],
  [ u"Ú", "\\'U" ],
  [ u"Ý", "\\'Y" ],
  [ u"â", "\\^a" ], # Circumflex
  [ u"ê", "\\^e" ],
  [ u"î", "\\^\\i" ],
  [ u"ô", "\\^o" ],
  [ u"û", "\\^u" ],
  [ u"ŷ", "\\^y" ],
  [ u"Â", "\\^A" ],
  [ u"Ê", "\\^E" ],
  [ u"Î", "\\^\\I" ],
  [ u"Ô", "\\^O" ],
  [ u"Û", "\\^U" ],
  [ u"Ŷ", "\\^Y" ],
  [ u"ä", "\\\"a" ],    # Umlaut or dieresis
  [ u"ë", "\\\"e" ],
  [ u"ï", "\\\"\\i" ],
  [ u"ö", "\\\"o" ],
  [ u"ü", "\\\"u" ],
  [ u"ÿ", "\\\"y" ],
  [ u"Ä", "\\\"A" ],
  [ u"Ë", "\\\"E" ],
  [ u"Ï", "\\\"\\I" ],
  [ u"Ö", "\\\"O" ],
  [ u"Ü", "\\\"U" ],
  [ u"Ÿ", "\\\"Y" ],
  [ u"ç", "\\c{c}" ],   # Cedilla
  [ u"Ç", "\\c{C}" ],
  [ u"œ", "{\\oe}" ],   # Ligatures
  [ u"Œ", "{\\OE}" ],
  [ u"æ", "{\\ae}" ],
  [ u"Æ", "{\\AE}" ],
  [ u"å", "{\\aa}" ],
  [ u"Å", "{\\AA}" ],
 # [ u"–", "--" ],   # Dashes
#  [ u"—", "---" ],
  [ u"ø", "{\\o}" ],    # Misc latin-1 letters
  [ u"Ø", "{\\O}" ],
  [ u"ß", "{\\ss}" ],
  [ u"¡", "{!`}" ],
  [ u"¿", "{?`}" ],
#  [ u"\\", "\\\\" ],    # Characters that should be quoted
 # [ u"~", "\\~" ],
  [ u"&", "\\&" ],
  [ u"$", "\\$" ],
 # [ u"{", "\\{" ],
 # [ u"}", "\\}" ],
  #[ u"%", "\\%" ],
#  [ u"#", "\\#" ],
  #[ u"_", "\\_" ],
  [ u"≥", "$\\ge$" ],   # Math operators
  [ u"≤", "$\\le$" ],
  [ u"≠", "$\\neq$" ],
  [ u"©", "\copyright" ], # Misc
  [ u"ı", "{\\i}" ],
  [ u"µ", "$\\mu$" ],
  #[ u"°", "$\\deg$" ],
  #[ u"‘", "`" ],    #Quotes
  #[ u"’", "'" ],
  #[ u"“", "``" ],
  #[ u"”", "''" ],
  #[ u"‚", "," ],
  #[ u"„", ",," ],
]


def makeReviewerList():
	o = codecs.open("../meta/subreviewers_final.txt",'r','utf-8')
	d = o.read()
	o.close()
	d = fixLatexCharacters(d)
	r_names = [x.split("\t")[2] for x in d.split("\n")]
	r_names2 = []
	for n in r_names:
		if n.count("<")>0:
			n = n[:n.index("<")]
		n = n.strip()
		r_names2.append(n)

	r_names2 = list(set(r_names2))
	r_names2.sort()
	out = "\\begin{multicols}{3}\n\\begin{itemize}[label={},leftmargin=*]\n"
	for n in r_names2:
		out += "\\item "+n +"\n"
	out += "\n\\end{itemize}\n\\end{multicols}\n"
	out = out[:-1]
	o = open("../../tex/reviewers.tex",'w')
	o.write(out)
	o.close()
