let constrain = 2000;
let mouseOverContainer = document.getElementById("ex1");
let ex1Layer = document.getElementById("ex1-layer");
var finished = false;

//website UI graphics
function transforms(x, y, el) {
  let box = el.getBoundingClientRect();
  let calcX = -(y - box.y - (box.height / 2)) / constrain;
  let calcY = (x - box.x - (box.width / 2)) / constrain;
  
  return "perspective(100px) "
    + "   rotateX("+ calcX +"deg) "
    + "   rotateY("+ calcY +"deg) ";
};

 function transformElement(el, xyEl) {
  el.style.transform  = transforms.apply(null, xyEl);
}

mouseOverContainer.onmousemove = function(e) {
  let xy = [e.clientX, e.clientY];
  let position = xy.concat([ex1Layer]);

  window.requestAnimationFrame(function(){
    transformElement(ex1Layer, position);
  });
};

//preloader
var loader = document.getElementById("loader");
var loaderText = document.getElementById("loader-text");
var video = document.getElementById("video");
if (finished) {
  loader.style.display = "none";
  loaderText.style.display = "none";
  video.style.display = "block";
}

// When the user clicks the convert button, open video
/*
function openVideoPage() {
  window.location.href = "video.html";
}
  */


function openVideoPage() {
  document.getElementById("loading-text").style.display = "block";
}