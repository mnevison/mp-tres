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
