let cursor = true
let speed = 400
// let colors = Array("#CA4246", "#E16541", "#F18F43", "#8B9862", "#A7489B", "#476098")

setInterval(() => {
    if(cursor) {
        document.getElementById('cursor').style.opacity = "0"
        // document.getElementById('cursor').style.color = colors[Math.floor(Math.random() * colors.length)]
        cursor = false
    }else {
        document.getElementById('cursor').style.opacity = "1"
        cursor = true
    }
}, speed)