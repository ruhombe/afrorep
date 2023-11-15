
var Tabbuttons = document.querySelectorAll('.tab-btn')
var TabWindows = document.querySelectorAll('.tab')
let centLide = 1;

var talNav = function(nual){
    TabWindows.forEach((slide) => {
        slide.classList.remove('active-tab');
            Tabbuttons.forEach((btn)=>{
                btn.classList.remove('active-btn');
            });
        });
        TabWindows[nual].classList.add('active-tab');
        Tabbuttons[nual].classList.add('active-btn');
    }
    Tabbuttons.forEach((btn, i) => {
        btn.addEventListener("click", () => {
            talNav(i);
            centSlide  = i;
        });
    });