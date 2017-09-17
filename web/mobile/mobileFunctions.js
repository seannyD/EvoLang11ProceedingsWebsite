var currentlyOpen = "";

function loadMobile(){

  var divs = document.getElementsByTagName("div");
  for(var i = 0; i < divs.length; i++){
    id = divs[i].id;
    if(id.slice(0, 3) == "ABS"){
       hideMe(id);
    }
  }


  updateSearchMobile();
  tocHeight();

}

function tocHeight(){
  var topDivHeight = document.getElementById("tocx").offsetTop;
  var totalHeight = document.body.offsetHeight;
  $('#tocx').height(totalHeight  - topDivHeight );
}

function updateSearchMobile(){
  exitDetails();
  updateSearch();

}

function exitDetails(){
  hideMe("exitButton");
  if(currentlyOpen!=''){
    hideMe(currentlyOpen);
    currentlyOpen='';
  }
  showMe("tocx");
  showMe("topSearch")
  //document.getElementById("tocx").style.display = 'inline';
}

function openDetails(idx){
  idx = "ABS_" + idx;
  console.log("Open "+idx);
  showMe(idx);
  hideMe("tocx");
  hideMe("topSearch")
  showMe("exitButton");
  currentlyOpen = idx;
}

function showMe(x){
  console.log("SHOW "+x);
  //document.getElementById(x).style.display = 'inline';
  $("#"+x).show();
}

function hideMe(x){
  //document.getElementById(x).style.display = 'none';
  $("#"+x).hide();
}

// hide address bar
window.addEventListener("load",function() {
	// Set a timeout...
	setTimeout(function(){
		// Hide the address bar!
		window.scrollTo(0, 1);
	}, 0);
});

window.addEventListener("resize",function(){
  tocHeight();
})
