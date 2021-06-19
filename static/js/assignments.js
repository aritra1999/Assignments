let assignmentToggle = document.getElementById("assignmentToggle")
let studentToggle = document.getElementById("studentToggle")
let assignmentContainer = document.getElementById("assignmentContainer")
let studentContainer = document.getElementById("studentContainer")

assignmentToggle.addEventListener("click", openAssignment)
function openAssignment(){
    assignmentContainer.style.display="block"
    studentContainer.style.display="none"
    assignmentToggle.classList.add("activeTag")
    studentToggle.classList.remove("activeTag")
}

studentToggle.addEventListener("click", openStudent)
function openStudent(){
    assignmentContainer.style.display="none"
    studentContainer.style.display="block"
    assignmentToggle.classList.remove("activeTag")
    studentToggle.classList.add("activeTag")
}