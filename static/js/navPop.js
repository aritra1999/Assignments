let popUp = document.getElementById("profilePop")
let popToggle = document.getElementById("popToggle")
let counter = 1
popToggle.addEventListener("click", pop)
function pop(){
    counter++
    if (counter%2 === 0){
        popUp.style.display="block"
    }
    else{
        popUp.style.display="none"
    }
}
// let classToggleClose = document.getElementById("closeBtn")
// let classToggleOpen = document.getElementById("createClass")
// let classBody = document.getElementById("classBody")
// classBody.style.display = "none"
// classToggleOpen.addEventListener("click", classShow)
// function classShow(){
//     classBody.style.display = "block"
// }
// classToggleClose.addEventListener("click", classHide)
// function classHide() {
//     classBody.style.display = "none"
// }