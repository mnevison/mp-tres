# Nights Team Planner - Milestone Project 3 - Backend Development.

![amiresponsive](docs/readme/amiresponsive.png)

This team planner/productivity app was created as my 3rd milestone project for my Level 5 Diploma in Web Development.

Link to deployed site: [Team Planner](https://nightsapp-mp3-95b6adbcde7b.herokuapp.com/)

## Contents

- [AUTOMATED TESTING](#automated-testing)

  - [W3C Validator](#w3c-validator)
  - [CSS Jigsaw](#css-jigsaw)
  - [JavaScript Validator](#javascript-validator)
  - [Python Validator](#python-validator)
  - [Lighthouse](#lighthouse)

- [MANUAL TESTING](#manual-testing)

  - [Testing User Stories](#testing-user-stories)
  - [Full Testing](#full-testing)

  ***

  ## Automated Testing

  ### W3C Validator

  [W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the website. Due to my app not working in the regular way, I've had to do it via direct input.

  - [Login Page](/docs/testing/w3c%20-%20html/w3c-login.png) - 1 error. The error is related to a bootstrap class added on for styling purposes. I'm happy to let this error sit.
  - [Register](/docs/testing/w3c%20-%20html/w3c-register.png) - No errors.
  - [Dashboard](/docs/testing/w3c%20-%20html/w3c-dashboard.png) - No errors.
  - [Create Task](/docs/testing/w3c%20-%20html/w3c-createtask.png) - Corrected the initial errors I was getting regarding the <options> tag. I needed to add a placeholder before my own custom ones. No errors now.
  - [Edit Task](/docs/testing/w3c%20-%20html/w3c-edittask.png) - Corrected the initial errors I was getting regarding the <options> tag. I needed to add a placeholder before my own custom ones. No errors now.
  - [Holiday Request](docs/testing/w3c%20-%20html/w3c-holidayrequest.png) - No errors.
  - [Edit Holiday](/docs/testing/w3c%20-%20html/w3c-editholiday.png) - No errors.
  - [Admin Approval](/docs/testing/w3c%20-%20html/w3c-adminapprove.png) - No errors.

  ### CSS Jigsaw

  [CSS Validator](https://jigsaw.w3.org/css-validator/) Jigsaw was used to validate my styles.css file.

  - [CSS Jigsaw](/docs/testing/w3jigsaw/w3-jigsaw.png) - No errors.

  ### JavaScript Validator

  [JSHint](https://jshint.com/) was used to validate the JavaScript across the site.

  - [script.js](/docs/testing/jshint/jshint-script.png) - No issues. Unused variables are from Sweetalert2.
  - [dashboard](/docs/testing/jshint/jshint-dashboard.png) - No issues. Unused variables refer to FullCalendar & Bootstrap.

  **_I had to inline a good portion of my JavaScript due to using Jinja to loop through my tasks and holidays. To get the validator to provide some results that weren't just full of errors caused by Jinja, I removed that section totally and just essentially added the code related to the calendar & modal functionality - Below you will see the "taskEvents" and "holidayEvents" variables missing from the above file_**

  ```
  document.addEventListener('DOMContentLoaded', function() {
      let taskEvents = [
          {% for task in tasks %}
          {
              title: "{{ task.title|escape }}",
              start: "{{ task.start_date.strftime('%Y-%m-%dT%H:%M:%S') }}",
              end: "{{ task.due_date.strftime('%Y-%m-%dT%H:%M:%S') }}",

              extendedProps: {
                  type: 'task',
                  description: "{{ task.description|escape }}",
                  editUrl: "{{ url_for('views.edit_task', task_id=task.id) }}",
                  deleteUrl: "{{ url_for('views.delete_task', task_id=task.id) }}"
              }
          }{% if not loop.last %},{% endif %}
          {% endfor %}
      ];

      let holidayEvents = [
          {% for holiday in holidays %}
          {
              title: "{{ holiday.owner.fname if holiday.owner else 'Unknown' }} {{ holiday.owner.lname if holiday.owner else '' }}'s Holiday",
              start: "{{ holiday.start_date.strftime('%Y-%m-%dT%H:%M:%S') if holiday.start_date else '' }}",
              end: "{{ holiday.end_date.strftime('%Y-%m-%dT%H:%M:%S') if holiday.end_date else '' }}",
              type : 'holiday',
              extendedProps: {
                  description: "Holiday: {{ holiday.description|escape if holiday.description else '' }}{% if not holiday.is_approved %} (Pending Approval){% endif %}",
                  isDeclined: {% if holiday.is_declined %} true {% else %} false {% endif %},
                  isApproved: {% if holiday.is_approved %} true {% else %} false {% endif %},
                  editUrl: "{{ url_for('views.edit_holiday', holiday_id=holiday.id) }}",
                  deleteUrl: "{{ url_for('views.delete_holiday', holiday_id=holiday.id) }}"
              },
              backgroundColor:
                {% if holiday.is_approved %}
                  "#28a745"
                {% elif holiday.is_declined %}
                  "#dc3545"
                {% else %}
                  "#ffc107"
                {% endif %}
            }{% if not loop.last %},{% endif %}
            {% endfor %}
      ];
  ```

  ### Python Validator

  [CI Python Linter](https://pep8ci.herokuapp.com/) was used to validate the Python code for pep8 compliance. All but 1 error I was able to correct during initial testing, and have now fully cleared all errors.

  - [run.py](/docs/testing/pep8/run-pep8.png) - No errors.
  - [init.py](/docs/testing/pep8/init-pep8.png) - No errors.
  - [views.py](/docs/testing/pep8/views-pep8.png) - 1 error, mentioned above. Correction below.
  - [auth.py](/docs/testing/pep8/auth-pep8.png) - No errors.
  - [models.py](/docs/testing/pep8/models-pep8.png) - No errors.
  - [database.py](/docs/testing/pep8/db-pep8.png) - No errors.
  - [errors.py](/docs/testing/pep8/errors-pep8.png)

  **_Below is the line of code causing the issue in views.py with in it's corrected format_**

  ![corrected-views](/docs/testing/pep8/views-error-fix.png)

  ### Lighthouse

  I used Lighthouse within the Chrome Developer Tools to test the performance, accessibility, best practices and SEO of the website.

  **_As the majority of the website is just various forms, I was noticing the majority of results were the same. Rather than posting the tests from everything, I'm just going to show the results I got from my "Dashboard" - The hub of the site that contains the most information that may have the biggest impact on things like performance_**

  #### Dashboard Desktop

  ![dashboard-desktop](/docs/testing/lighthouse/desktop/dashboard-desktop.png)

  #### Dashboard Mobile

  ![dashboard-mobile](/docs/testing/lighthouse/mobile/dashboard-mobile.png)
