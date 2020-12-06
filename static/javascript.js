function checkBox() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var checkedOne = Array.prototype.slice.call(checkboxes).some(x => x.checked);
    
    if (checkedOne === false) {
        alert("You must schedule at least 1 day.");
        event.preventDefault();
        event.stopPropagation();
    }
}

function checkTime() {    
    var startTime = document.querySelector('#start').value;
    var endTime = document.querySelector('#end').value;
    
    if (startTime >= endTime) {
        alert("Start time must be before end time.");
        event.preventDefault();
        event.stopPropagation();
    }
}

function editTime(index) {
    
    startID = '#start' + index;
    endID = '#end' + index;
    var startTime = document.querySelector(startID).value;
    var endTime = document.querySelector(endID).value;
    
    if (startTime >= endTime) {
        alert("Start time must be before end time.");
        event.preventDefault();
        event.stopPropagation();
    }
}

function delAllSchedule() {
    var del = confirm("Are you sure you want to delete all schedules?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function delRowSchedule() {
    var del = confirm("Are you sure you want to delete this row from your schedule?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function delAllEvents() {
    var del = confirm("Are you sure you want to delete all special events?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function delRowEvent() {
    var del = confirm("Are you sure you want to delete this row from your special events?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function delAllTodos() {
    var del = confirm("Are you sure you want to delete all tasks from your To-Do list?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}

function delRowTodo() {
    var del = confirm("Are you sure you want to delete this row from your To-Do list?");
    
    if (!del) {
        event.preventDefault();
        event.stopPropagation();
    }
}