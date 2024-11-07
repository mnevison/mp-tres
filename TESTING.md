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

- [BUGS](#bugs)

  ***

  ## Automated Testing

  ### W3C Validator

  [W3C](https://validator.w3.org/) was used to validate the HTML on all pages of the website. Due to my app not working in the regular way, I've had to do it via direct input.

  - [Login Page](/docs/testing/w3c%20-%20html/w3c-login.png) - 1 error. The error is related to a bootstrap class added on for styling purposes. I'm happy to let this error sit.
  - [Register](/docs/testing/w3c%20-%20html/w3c-register.png) - No errors.
  - [Dashboard](/docs/testing/w3c%20-%20html/w3c-dashboard.png) - No errors. Warnings are from elements that are dynamically rendered, so may sometimes appear empty.
  - [Create Task](/docs/testing/w3c%20-%20html/w3c-createtask.png) - Corrected the initial errors I was getting regarding the `<options>` tag. I needed to add a placeholder before my own custom ones. No errors now.
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

---

## Manual Testing

### Testing User Stories

**_First Time User Goals_**

| Goal                                             |                 Test                 | Outcome                                           |
| :----------------------------------------------- | :----------------------------------: | :------------------------------------------------ |
| To be able to register for an account            |       Register for an account        | Successfully make a new account for the app       |
| To be able to navigate around the site with ease | Click the navigation links & buttons | Routed to desired area of site                    |
| Log out when I'm done                            |  Press "Logout" button on Dashboard  | I was logged out and returned to the login screen |

**_Returning Visitor Goals_**

| Goal                                                    |                  Test                  | Outcome                                                                                                                       |
| :------------------------------------------------------ | :------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------- |
| To view/add tasks for myself                            |              Added a task              | The task was added then displayed on the Dashboard view                                                                       |
| To request/update/check the status of my holiday        |          Requested a holiday           | Holiday rendered within the calendar across chosen dates                                                                      |
| Complete/update any tasks I've finished or need to move | Edited a task - Once edited, completed | The task updated - date ranges changed. Calendar view updated. Once completed, task was removed from the task view & calendar |

### Full Testing

**_Heading above each file represents the feature that is being tested. Text above would be the expected outcome. GIF will show the test performed and the outcome of the test_**

#### Navbar Authentication

**_Unauthenticated users only see registration link - Once validated, the other links appear_**

![auth-nav](/docs/testing/full-testing/auth-nav.gif)

#### Login

**_User is logged in and sent to the dashboard_**

![login-test](/docs/testing/full-testing/login-test.gif)

#### Logout

**_User is logged out and redirected to the login screen_**

![logout-test](/docs/testing/full-testing/logout-test.gif)

#### Register Nav Link

**_Opens registration page_**

![register-link](/docs/testing/full-testing/register-nav.gif)

#### Register (Account Creation)

**_Upon registering the new user will be given access and redirected to the dashboard_**

![register-new-account](/docs/testing/full-testing/register-account-creation.gif)

#### Register (Email Validation)

**_If an email is already in use on the database, an error will be flashed to advise the user_**

![register-email](/docs/testing/full-testing/register-email-validation.gif)

#### Registration Form Auto Fill

**_If any validation checks fail upon submission, the form data will be re-input automatically_**

![register-auto-fill](/docs/testing/full-testing/register-form-complete.gif)

#### New Task Link/Button

**_Directs user to the New Task form_**

![new-task-link](/docs/testing/full-testing/new-task-link.gif)

#### Create New Task

**_When all fields are filled out correctly, the task is created and rendered on the dashboard & the calendar_**

![create-new-task](/docs/testing/full-testing/create-new-task.gif)

#### Edit Task Link

**_Will direct user to the desired task they want to edit with all fields populated with the original task information_**

![edit-task-link](/docs/testing/full-testing/edit-task-link.gif)

#### Edit Task

**_The user can alter the task details and update the task being rendered on the dashboard & stored in the database_**

![edit-task](/docs/testing/full-testing/edit-task.gif)

#### Complete/Delete Task

**_Upon confirmation that they want to complete/delete the task, the data is removed from the site & database_**

![task-delete](/docs/testing/full-testing/task-delete.gif)

#### Task Edit (Modal)

**_User can interact with a task on the calendar and navigate to the edit page via the pop-up modal_**

![task-modal-edit](/docs/testing/full-testing/task-modal-edit.gif)

#### Task Delete/Complete (Modal)

**_User can interact with a task on the calendar and choose to complete/delete it via the pop-up modal_**

![task-modal-delete](/docs/testing/full-testing/task-modal-delete.gif)

#### Request Holiday Nav

**_Users are able to navigate to the holiday request page_**

![request-holiday-link](/docs/testing/full-testing/request-holiday-link.gif)

#### Request Holiday

**_Users are able to request a holiday for there desired time period_**

![request-holiday](/docs/testing/full-testing/request-holiday.gif)

#### Holiday Edit/Update Link

**_Users are able to interact with the holiday object on the calendar and navigate to the edit page_**

![holiday-edit-link](/docs/testing/full-testing/holiday-edit-link.gif)

#### Holiday Update

**_Users are able to update the dates requested_**

![holiday-edit-update](/docs/testing/full-testing/holiday-edit-update.gif)

#### Holiday Delete

**_Users are able to delete there existing holiday requests_**

![delete-holiday](/docs/testing/full-testing/delete-holiday.gif)

#### Holiday Authentication

**_Users are unable to interact with a holiday object that isn't related to them_**

![holiday-auth](/docs/testing/full-testing/holiday-auth.gif)

#### Holiday Status Update

**_When editing a holiday that is already approved or denied, the holiday needs to be checked over again by an admin - flash message to confirm_**

![holiday-status-update](/docs/testing/full-testing/holiday-status-update.gif)

#### Admin Holiday Approval

**_Admins are able to access the Approve Holiday route and approve/deny any pending requests_**

![admin-approval](/docs/testing/full-testing/admin-holiday-approve.gif)

---

## Bugs

As of right now, the site has no known bugs.

I didn't really experience any "bugs" during development - I experienced more "user error", which was typically solved using the flask default debugging tool.

My main initial "headache" was related to the Database side of the project. Getting it off of the ground was a chore, but this was an error of my own making as I was trying to use 2 different projects that were very different as helpers - Credited in the README.md
