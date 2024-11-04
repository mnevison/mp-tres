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

document.addEventListener("DOMContentLoaded", function () {
  // Target the delete button in the modal
  const deleteButton = document.getElementById("deleteHolidayButton");
  const deleteForm = document.getElementById("deleteHolidayForm");

  deleteButton.addEventListener("click", function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // SweetAlert2 confirmation dialog
    Swal.fire({
      title: "Are you sure?",
      text: "This action cannot be undone!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        // Submit the form if confirmed
        deleteForm.submit();
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  // Target the task completion button
  const deleteTaskButton = document.getElementById("deleteTaskButton");
  const deleteTaskForm = document.getElementById("deleteTaskForm");

  deleteTaskButton.addEventListener("click", function (event) {
    // Prevent the default form submission
    event.preventDefault();

    // SweetAlert2 confirmation dialog for task completion
    Swal.fire({
      title: "Mark Task as Complete?",
      text: "This action will mark the task as complete and remove it from the list.",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: "#28a745",
      cancelButtonColor: "#6c757d",
      confirmButtonText: "Yes, complete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        // Submit the form if confirmed, which routes to delete the task
        deleteTaskForm.submit();
      }
    });
  });
});
