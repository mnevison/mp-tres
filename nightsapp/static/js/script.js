document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    events: [
      {
        title: "John Doe's Holiday",
        start: "2024-10-10",
        end: "2024-10-15",
        color: "green",
      },
      {
        title: "Jane Smith's Holiday",
        start: "2024-11-05",
        end: "2024-11-10",
        color: "green",
      },
      {
        title: "Peter Parker's Holiday",
        start: "2024-10-10",
        end: "2024-10-15",
        color: "green",
      },
    ],
  });

  calendar.render();
});

const deleteButtons = document.querySelectorAll('[data-bs-toggle="modal"]');
const deleteForm = document.getElementById("deleteForm");
const taskIdInput = document.getElementById("task_id");

deleteButtons.forEach((button) => {
  button.addEventListener("click", function () {
    const taskId = this.getAttribute("data-task-id");
    taskIdInput.value = taskId;
    deleteForm.action = `/views/delete_task/${taskId}`;
  });
});
