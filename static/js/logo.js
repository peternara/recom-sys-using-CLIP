const timeline = gsap.timeline({repeat: -1});
const chars = document.querySelectorAll(".text");

gsap.set(".one", {color: "#3498DB"});
gsap.set(".two", {color: "#E74C3C"});
gsap.set(".three", {color: "#F1C40F"});
gsap.set(".four", {color: "#3498DB"});
gsap.set(".five", {color: "#27AE60"});
gsap.set(".six", {color: "#E74C3C"});
gsap.set(".seven", {color: "#3498DB"});
gsap.set(".eight", {color: "#E74C3C"});
gsap.set(".nine", {color: "#F1C40F"});
gsap.set(".ten", {color: "#3498DB"});
gsap.set(".eleven", {color: "#27AE60"});

timeline.from(chars, { opacity: 1, scale: 0, ease: "sine", delay: 0.25 }).
to(".text", {
  "--font-weight": 900,
  duration: .9,
  ease: "sine.inOut",
  stagger: {
    yoyo: true,
    each: 0.1,
    repeat: -1 } },
1);

/*
  Bounce down animation needs value ‘infinite’ on animation-iteration-count property of animation.

  animation-iteration-count: infinite

  Can have this in a shorthand too, like in the Codepen: 
  
  animation: bounce-down 2s ease infinite;
  
  And [sometimes it makes sense to postpone the execution of css-animations and transitions until the webpage has fully loaded](https://codepen.io/atelierbram/pen/GFyiC) …

*/
/* 
 * http://blog.simonwillison.net/post/57956760515/addloadevent
 * http://www.sitepoint.com/closures-and-executing-javascript-on-page-load/ 
*/ 
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      oldonload();
      func();
    }
  }
}

// addLoadEvent(nameOfSomeFunctionToRunOnPageLoad);
addLoadEvent(function() {
    /* more code to run on page load */
    /* put class on html-element wheh page is loaded */ 
    document.documentElement.className = "is-loaded"
    });