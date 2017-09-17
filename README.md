# EvoLang2016Proceedings

This project takes data from an EasyChair.org conference and produces a website, electronic schedule and latex booklet.  It was used to produce the website for EvoLang 11 (http://evolang.org/neworleans).

The main program is the python script build/python/makeAuthorPages.py.

The following files are required:

build/meta/:
----------------
    (files from EasyChair - administrator can download 'conference data' csv files)
    
    author.csv
    
    submission-topics.csv
    
    submission.csv
    
    subreviewers_final.txt: a list of reviewers (for the latex booklet)

build/plenaryPapers/:
----------------------------
	If plenary speakers want their papers included in the proceedings, then you can add the details here - it requires versions of the files in build/meta/

build/paperDecisions/:
----------------------------
    Decisions Tracker: a google spreadsheet was used to keep track of decisions about acceptance or rejection.  There are four categories: ACCEPT, Reject, Poster and 'Poster waiting' (on the shortlist to be upgraded to a talk).
    
    EvoLang publishing license (part 2) (Responses) - Form responses 1.csv:  
    	A google form was sent to participants to answer questions on how they would like to license the work.  Several options were available e.g. :
    	- Creative Commons CC BY license (preferred)
    	- Creative Commons CC BY-NC-ND license
    	- CC BY-NC-SA
    	All authors maintained copyright of their papers - this is independent from the license they give EvoLang to publish their paper.
	Authors could indicate that they wanted to wait before their paper was included in the column "Do you wish your paper to appear in the proceedings?" (Enter anything except 'Yes').  A page is produced, but not papers are added until this is changed to 'Yes'.

build/submissions/:
-------------------------
	paper pdfs from EasyChair

build/Templates:
----------------------
	(This has a set of templates used to create the web pages)
	
	toc.html: DuckDuckGo search site location
	
	Citation template web location


The script makeAuthorPages.py does the following things:

- Produces web pages for each paper, including a bibtex citation
	
- Adds a copyright notice and meta data to the pdfs
	
- Adds pdfs and supplementary materials to the web pages
	
- Produces a table of contents for the website
	
- Produces a mobile version of the website
	
- Produces a latex booklet

Note that makeAuthorPages.py copies index.html to index.php (the EvoLang server promotes php pages before html).  There are also various options at the start of the script for adding equal contributions, avoiding adding certain papers etc.

The python script for producing the latex has some custom rules for converting text into latex code.  The latex booklet needs to be complied (Latex), then an index needs to be made (MakeIndex), then compiled again.

The schedule folder uses an R script to combine a list of talks with a list of times and produces an ics calendar format, which can be imported to google calendar.

Workshop web pages were edited by hand from the templates.


-----------

For publishing a physical copy through lulu, we need to crop the paper size, see:
tex/lulu/make_pdfCrop_command.R

Which makes this command:
pdfcrop --margins '-81.70936275 -97.15831425 -81.70936275 -97.15831425' --clip --bbox '0 0 595.2807 842.180457' EvoLang11.pdf EvoLang11_crop.pdf

Then we need to re-embed the fonts:
pdf2ps EvoLang11_crop.pdf EvoLang11_crop.ps
ps2pdf -dSAFER -dNOPLATFONTS -dEmbedAllFonts=true -dPDFSETTINGS=/prepress EvoLang11_crop.ps EvoLang11_crop_embedded.pdf