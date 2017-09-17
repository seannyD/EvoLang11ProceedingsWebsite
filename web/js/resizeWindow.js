var mobileHeader = '<div class="container-fluid">\
    <ul class="nav navbar-nav">\
        <li class = "active"><a href="mobile/index.html">Mobile Site</a></li>\
    </ul>\
</div>';

var origHeader = "";


window.onresize = function(event) {
  switchHeaders();
};

document.body.onload = function(event){

  switchHeaders();
  fixGoogleSearchBox();

}

switchHeaders = function(){
  if(origHeader==""){
    origHeader =   document.getElementById("thenav").innerHTML;
  }
  mobileHeader = '<div class="container-fluid">\
      <ul class="nav navbar-nav">\
          <li class = "active"><a href="mobile/index.html">Mobile Site</a></li>\
      </ul>\
  </div>';
  if(window.innerWidth < 765){
    document.getElementById("thenav").innerHTML = mobileHeader;
  } else{
    document.getElementById("thenav").innerHTML = origHeader;
  }
}


fixGoogleSearchBox = function(){

  var cols = document.getElementsByClassName('gsc-input-box');
  for(i=0; i<cols.length; i++) {
    console.log("HERE");
    cols[i].style.height = '30px';
  }

  // gsc-input
  var csx = ["cse","gsc-control-cse","gsc-control-cse","gsc-search-box","gsc-input"];
  for(var x=0;x<csx.length;++x){
    cols = document.getElementsByClassName(csx[x]);
    for(i=0; i<cols.length; i++) {
      cols[i].style.padding = '0px';
      cols[i].style.paddingRight = '0px';
      cols[i].style.width = '100%';
    }
  }
  csx = ["gsc-clear-button",'gsc-search-button'];
  cols = document.getElementsByClassName('gsc-search-button');
  for(var x=0;x<csx.length;++x){
    cols = document.getElementsByClassName(csx[x]);
    for(i=0; i<cols.length; i++) {
      cols[i].style.display = 'none';
    }
  }

// remove google icon
//  cols = document.getElementById("gsc-i-id1");
//  if(cols){
    //cols.style.background = ""
  //}

}
