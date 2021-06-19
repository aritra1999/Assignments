let popUpWrap = document.getElementById("popUpContainerWrap")
let popUpCont = document.getElementById("popUpContainerW")
let openToggle = document.getElementById("createCta")
let closeToggle = document.querySelector(".closeClassPop")
let closeToggleBtn = document.querySelector(".closeClassPopBtn")
let popUpForm = document.getElementById("creationForm")

openToggle.addEventListener("click", openCta)
function openCta(){
    popUpWrap.style.display="flex"
}

closeToggle.addEventListener("click", closeCta)
closeToggleBtn.addEventListener("click", closeCta)
function closeCta(){
    popUpWrap.style.display="none"
    popUpForm.reset()
}