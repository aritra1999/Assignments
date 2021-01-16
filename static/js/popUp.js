let popUpContainerWrap = document.getElementById("popUpContainerWrap")
let popUpContainer = document.getElementById("popUpContainerW")
let popUpOpen = document.getElementById("popUpOpenToggle")
let popUpClose = document.getElementById("popUpCloseToggle")

popUpOpen.addEventListener("click", popUpOpenFunc)
function popUpOpenFunc(){
    popUpContainerWrap.style.display="flex"
}
popUpClose.addEventListener("click", popUpCloseFunc)
function popUpCloseFunc(){
    popUpContainerWrap.style.display="none"
}