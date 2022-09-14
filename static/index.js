let open = document.querySelector('.menu-icon-con')
let screen = document.querySelector('.mobile-screen-con')
let close = document.querySelector('.nav-menu-con')
const body = document.querySelector("body");
open.addEventListener('click', () => {
  screen.style.width = "100%"
  body.style.overflow = "hidden";
})
close.addEventListener('click', () => {
  screen.style.width = "0px";
  body.style.overflow = "auto";
})

