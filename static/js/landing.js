if (document.getElementById('cursor')) {
    let cursor = true
    let speed = 400

    setInterval(() => {
        if (cursor) {
            document.getElementById('cursor').style.opacity = "0"
            cursor = false
        } else {
            document.getElementById('cursor').style.opacity = "1"
            cursor = true
        }
    }, speed)
}


let ham = document.querySelector('.ham')
let navbarMob = document.querySelector('.navbarMob')
let triggerIndicator = 1
ham.addEventListener("click", openFunc)

function openFunc() {
    triggerIndicator++
    if (triggerIndicator % 2 === 0)
        navbarMob.classList.add("open")
    else
        navbarMob.classList.remove("open")
}