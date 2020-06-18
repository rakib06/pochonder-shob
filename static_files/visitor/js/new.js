window.onscroll = function () { myFunction() };

var sticky_nav = document.getElementById("sticky_nav");
var sticky = sticky_nav.offsetTop;

function myFunction() {
    if (window.pageYOffset >= sticky) {
        sticky_nav.classList.add("sticky")
    } else {
        sticky_nav.classList.remove("sticky");
    }
}

window.onscroll = function () { myFunction1() };

var sticky_nav1 = document.getElementById("sticky_nav1");
var sticky = sticky_nav1.offsetTop;

function myFunction1() {
    if (window.pageYOffset >= sticky) {
        sticky_nav1.classList.add("sticky1")
    } else {
        sticky_nav1.classList.remove("sticky1");
    }
}