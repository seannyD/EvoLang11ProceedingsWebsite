
divContents = [];
divIds = [];
topics = [];

function getDivContents(){
	console.log(document.title + " " + document.title == "EvoLangXI Proceedings (Mobile)");
	var isMobilePage = document.title == "EvoLangXI Proceedings (Mobile)";

	var divs = document.getElementsByTagName("div");
	for(var i = 0; i < divs.length; i++){
		id = divs[i].id;

		if(isMobilePage){
			if(id.slice(0,4)=="ABS_"){
				// take the contents from the full abstract
				divContents.push(divs[i].innerHTML.toLowerCase());
				// but hide the toc div
				divIds.push(id.slice(4,id.length));
			}
		} else{
			if(id.slice(0, 5) == "paper"){
			   divContents.push(divs[i].innerHTML.toLowerCase());
			   divIds.push(id);
			}
		}
	}

}

function findMatches(search_string){
	search_string = search_string.toLowerCase();
	console.log("topics");
	for(var i = 0; i < divContents.length; i++){
		var dx = document.getElementById(divIds[i]);
		var hasSearchWord = search_string.length==0;
		if(search_string.length > 0){
			var searchWords = search_string.split(" ");
			hasSearchWord = true;
			// match ALL words (but not necessarily in sequence)
			for(var sx =0;sx <searchWords.length; ++ sx){
				if(divContents[i].indexOf(searchWords[sx])< 0){
					hasSearchWord = false;
					break;
				}
			}

		}
		var hasTopic = topics.length==0;
		for(var t =0;t<topics.length;++t){

			if(divContents[i].indexOf(topics[t]) >= 0){
				hasTopic = true;
				break;
			}
		}

	   if(hasSearchWord && hasTopic){
	   		dx.style.display = 'inline';
	   }  else{
	   	dx.style.display = 'none';
	   }

	}
}

function updateSearch(){
	console.log("CHANGE");
	if(divIds.length==0){
		getDivContents();
		whichCheckboxes();
	}

	var searchString = document.getElementById("searchPapers").value;
	if(searchString.length >0 || topics.length>0){
		findMatches(searchString);
	} else {
		for(var i = 0; i < divContents.length; i++){
		document.getElementById(divIds[i]).style.display = 'inline';
		}
	}
}

function whichCheckboxes(){
	if(document.getElementById("topics")!=null){
		var topicBoxes = document.getElementById("topics").getElementsByTagName("input");
		topics = [];
		console.log("which");
		for(var i=0;i<topicBoxes.length; ++ i){
			if(topicBoxes[i].checked){
				topics.push(topicBoxes[i].id);
			}
		}
		console.log(topics);
	}
}


function changeCheckbox(boxname){
	whichCheckboxes();
	updateSearch();
}
