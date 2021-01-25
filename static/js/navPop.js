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