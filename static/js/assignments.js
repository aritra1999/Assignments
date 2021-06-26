let assignmentToggle = document.getElementById("assignmentToggle")
let studentToggle = document.getElementById("studentToggle")
let assignmentContainer = document.getElementById("assignmentContainer")
let studentContainer = document.getElementById("studentContainer")

assignmentToggle.addEventListener("click", openAssignment)

function openAssignment() {
    assignmentContainer.style.display = "block"
    studentContainer.style.display = "none"
    assignmentToggle.classList.add("activeTag")
    studentToggle.classList.remove("activeTag")
}

studentToggle.addEventListener("click", openStudent)

function openStudent() {
    assignmentContainer.style.display = "none"
    studentContainer.style.display = "block"
    assignmentToggle.classList.remove("activeTag")
    studentToggle.classList.add("activeTag")
}

function AddIO() {
    let IOField = $("#inputOutputFieldCont")
    if(testCaseNumber <= 5){
        IOField.append(`<div class="questionCreateFormElem" id="inputOutputField">
                            <h2 class="sampleText">Sample Test Case ${testCaseNumber}</h2>
                                <div class="sample">
                                    <label class="assignmentInfo sampleTest" for="questionName">Input ${testCaseNumber}:
                                        <textarea aria-required="true" name="input${testCaseNumber}" rows="10" cols="50" class="assignmentInfo" required></textarea>
                                    </label>
                                    <label class="assignmentInfo sampleTest" for="questionName">Output ${testCaseNumber}:
                                        <textarea aria-required="true" name="output${testCaseNumber}" rows="10" cols="50" class="assignmentInfo" required></textarea>
                                    </label>
                                </div>
                                <label class="score" for="score">Score ${testCaseNumber}(Out of 100):
                                    <input type="number" class="score" placeholder="Score" required name="score${testCaseNumber}">
                                </label>
                            </div>`)
    testCaseNumber++
    } else {
        document.getElementById("addTC").style.display="none"
    }
}
