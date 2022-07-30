(function () {
    // Variables
    var $curve = document.getElementById("curve");
    var last_known_scroll_position = 0;
    var defaultCurveValue = 350;
    var curveRate = 3;
    var ticking = false;
    var curveValue;
  
    // Handle the functionality
    function scrollEvent(scrollPos) {
      if (scrollPos >= 0 && scrollPos < defaultCurveValue) {
        curveValue = defaultCurveValue - parseFloat(scrollPos / curveRate);
        $curve.setAttribute(
          "d",
          "M 800 300 Q 400 " + curveValue + " 0 300 L 0 0 L 800 0 L 800 300 Z"
        );
        alert('here in scrollEvent')
      }
    }
  
    // Scroll Listener
    // https://developer.mozilla.org/en-US/docs/Web/Events/scroll
    window.addEventListener("scroll", function (e) {
      last_known_scroll_position = window.scrollY;
  
      if (!ticking) {
        window.requestAnimationFrame(function () {
          scrollEvent(last_known_scroll_position);
          ticking = false;
        });
      }
      
      ticking = true;
    });

    // page loading animation
    window.onbeforeunload = function () { $('#loading').show(); }  //현재 페이지에서 다른 페이지로 넘어갈 때 표시해주는 기능
    $(window).load(function () {          //페이지가 로드 되면 로딩 화면을 없애주는 것
        $('#loading').hide();
    });


    // logo
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

    timeline.from(chars, {opacity: 1, scale: 0, ease: "sine", delay: 0.25})
    .to(".text", {
        "--font-weight": 900,
        duration: .9,
        ease: "sine.inOut",
        stagger: {
            yoyo: true,
            each: 0.1,
            repeat: -1
        }
    }, 1);

})();
