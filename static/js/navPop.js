let popUp = document.getElementById("popUp")
let popToggle = document.getElementById("togglePop")
let arrow = document.querySelector(".arrowTogg")
let counter = 1
popToggle.addEventListener("click", pop)
function pop(){
    counter++
    if (counter%2 === 0){
        popUp.classList.add("popUpShow")
        arrow.style.transform="rotate(180deg)"
    }
    else{
        popUp.classList.remove("popUpShow")
        arrow.style.transform="rotate(0)"
    }
}