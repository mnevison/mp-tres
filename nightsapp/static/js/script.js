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
