library(Hmisc)

setwd("~/Documents/Conferences/Evolang11/ProceedingsWebsite/schedule")
sc = read.table("schedule2.txt",header=F,stringsAsFactors = F,sep='\t', quote=c())

sc$session = rep(1:27,each=4)

sub = read.csv("../build/meta/submission.csv",stringsAsFactors = F)

sub$tweet = sapply(sub$form.fields, function(X){
  strsplit(X,"\\(Tweet\\) ")[[1]][2]
  })

sub$tweet[is.na(sub$tweet)] = ""
sub$tweet[nchar(sub$tweet)<3 | nchar(sub$tweet)>150] = ""

auth = read.csv("../build/meta/author.csv",stringsAsFactors = F)

capwords <- function(s, strict = FALSE) {
  cap <- function(s) paste(toupper(substring(s, 1, 1)),
                           {s <- substring(s, 2); if(strict) tolower(s) else s},
                           sep = "", collapse = " " )
  sapply(strsplit(s, split = " "), cap, USE.NAMES = !is.null(names(s)))
}

sub$title = capitalize(tolower(sub$title))
sub$title.lower = tolower(sub$title)

sub$authString = sapply(sub$X.,function(X){
  paste(auth[auth$submission..==X,]$last.name,collapse=', ')
})


sc$num = NA
for(t in sc$V1){
  t = strsplit(tolower(t),":")[[1]][2]
  
}

titles = sc$V1
names(titles) = sc$session


overlapping.authors = tapply(titles,names(titles), function(X){
  X = gsub(', '," and ",X)
  
  authorCount = table(unlist(sapply(X,function(Y){
    strsplit(strsplit(Y,":")[[1]][1]," and ")
  })))
  if(sum(authorCount>1)>0){
    print(paste("Session",names(X)[1]))
    print(authorCount[authorCount>1])
  }
  
})


sc$rawTitles = tolower(sapply(sc$V1,function(X){
  x = strsplit(X,": ")[[1]]
  paste(x[2:length(x)],collapse=' ')
  }))

match(sc$rawTitles,sub$title)

tdist = adist(sc$rawTitles,sub$title.lower)

sc$num = sub[apply(tdist,1,which.min),]$X.
sc$real.title = sub[match(sc$num,sub$X.),]$title
sc$dist = apply(tdist,1,min)
sc$auth = sub[match(sc$num,sub$X.),]$authString
sc$tweet = sub[match(sc$num,sub$X.),]$tweet
tx = table(sc$num)
bug = as.numeric(names(tx[tx>1]))
sc[sc$num %in% bug,]

write.csv(sc,'linkSchedule.csv')


table(sub[match(sc$num,sub$X.),]$decision)


times = read.csv("../schedule/times.txt",sep="\t",header = F)

sc$day = as.character(rep(times[,1],each=4))
sc$time = as.character(rep(times[,2],each=4))
sc$time.end = rep(times[,3],each=4)
sc$room = rep(c("A","B","C","D"),length.out=nrow(sc))
dates = c(Monday="20160321",Tuesday="20160322",Wednesday="20160323",Thursday="20160324")
sc$date = dates[sc$day]

cal.head = "BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:EvoLang 2016
X-WR-TIMEZONE:America/Chicago
X-WR-CALDESC:
BEGIN:VTIMEZONE
TZID:America/Chicago
X-LIC-LOCATION:America/Chicago
BEGIN:DAYLIGHT
TZOFFSETFROM:-0600
TZOFFSETTO:-0500
TZNAME:CDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0500
TZOFFSETTO:-0600
TZNAME:CST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE"

cal.foot = "END:VCALENDAR"

template = "BEGIN:VEVENT
DTSTART;TZID=America/Chicago:startx
DTEND;TZID=America/Chicago:endx
DESCRIPTION:descriptionx
LOCATION:
SUMMARY:titlex
END:VEVENT"

ics.cal = cal.head 

print(dim(sc))

for(i in 1:nrow(sc)){
  tmpx = template
  startTime = paste(sc[i,]$date,"T",sc[i,]$time,'Z',sep='')
  stimeshort = substr(sc[i,]$time,1,4)
  
  addTime = c("A"=0,"B"=1,"C"=2,"D"=3)[sc[i,]$room]
  endTimeX = sc[i,]$time.end + addTime
  endTime = paste(sc[i,]$date,"T",endTimeX,'Z',sep='')

  
  titlex = paste(sc[i,]$auth,": ",sc[i,]$real.title,sep="")
  description = paste("Room ",sc[i,]$room,": ",stimeshort," ",'<a href="http://evolang.org/neworleans/papers/',sc[i,]$num,'.html">Link to Paper</a><br />',sc[i,]$tweet,sep='')
  tmpx = gsub("startx",startTime,tmpx)
  tmpx = gsub("endx",endTime,tmpx)
  tmpx = gsub("titlex",titlex,tmpx)
  tmpx = gsub("descriptionx",description,tmpx)
  if(is.na(tmpx)){
    print(sc[i,])
  }
  ics.cal = paste(ics.cal,tmpx,sep="\n")
}


ics.cal = paste(ics.cal,cal.foot,sep="\n")

filex = file("../schedule/EvoLangICS.ics")
writeLines(ics.cal,filex)
close(filex)
