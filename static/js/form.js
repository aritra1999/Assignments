let part1 = document.querySelector(".part1")
let part2 = document.querySelector(".part2")
let nextBtn = document.getElementById("nextBtn")
let prevBtn = document.getElementById("prevBtn")
let userType = document.getElementById("userType")
let rollField = document.getElementById("roll")
part2.style.display = "none"
rollField.style.display = "none"

nextBtn.addEventListener("click", nextPart)
function nextPart(){
    if (validation()===true){
        if(userType.value === "student"){
            rollField.style.display = "block"
        }
        part1.style.display = "none"
        part2.style.display = "block"
    }
}
prevBtn.addEventListener("click", prevPart)
function prevPart(){
        part2.style.display = "none"
        part1.style.display = "block"
}
function validation(){
    let f_name = document.forms["userForm"]["f_name"]
    let l_name = document.forms["userForm"]["l_name"]
    let univ = document.forms["userForm"]["university"]
    if(f_name.value===""||l_name.value===""||univ.value===""||userType.value==="0"){
        console.log(f_name.value)
        console.log(l_name.value)
        console.log(univ.value)
        console.log(userType.value)
        nextBtn.style.backgroundColor="#ff6347"
        nextBtn.style.borderColor="#ff6347"
        alert("Please fill us all the fields")
        return false
    }
    else {
        return true
    }
}