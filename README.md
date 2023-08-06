# task.it Backend

This is a REST API for the [task.it](https://github.com/saarthak2002/taskit-app) application written in Python using the Flask framework. A PostgreSQL database is used for persisting user data, and Firebase is used for authentication. The SQLAlchemy ORM is used for handling interactions with the database. The REST API and Postgres Database instance are hosted on Heroku. Postman was used for testing the REST API.

## Database Models
The following models are defined in the ORM:

### UserInfo
Fields: id (primary key), userUID (from Firebase), username, firstname, lastname

### Project
Fields: id (primary key), date_added, userUID (from Firebase), title, description, tasks (Task[]), task_categories (TaskCategory[])

### Task
Fields: id (primary key), date_added, title, description, project_id (Foreign key to id column of Projects table), status, task_category_name, task_category_color, created_by (UID from Firebase), completed_at_time, completed_by (UID from Firebase)

### TaskCategory
Fields: id (primary key), name, color, project_id (Foreign key to id column of Projects table)

### Collaborator
Fields: id (primary key), project_id (Foreign key to id column of Projects table), userUID (from Firebase)

## Endpoints
The significant API endpoints are:

### .../users
GET or POST requests to get UserInfo or create new UserInfo entry on sign-up.

### .../users/<user_uid>
GET UserInfo from the unique user_id of a user provided by Firebase during login or sign-up.

### .../users/search/<search_string>
Search for a user's info by their username. Full-text search based on the query in the search string using TS Vectors.

### .../users/change/<user_uid>
Update the username in the UserInfo of the user with unique id user_uid.

### .../projects
GET or POST requests to get all projects or create a new project using data included in the request body.

### .../projects/<user_uid>
GET all projects for a particular user with unique id user_uid.

### .../projects/id/<project_id>
GET a particular project based on its id.

### .../projects/<project_id>/tasks
GET a JSON Array of all the tasks added to a project. Send a POST request to add a new Task to a project given by project_id based on data sent in the request body.

### .../task/<task_id>/complete
Change the status of a particular task to Complete.

### .../task/<task_id>/pending
Change the status of a particular task to Pending.

### .../task/<task_id>/delete
Delete a particular task from a project.

### .../task/<task_id>/edit
Edit the information of a task like name, description, category, etc.

### .../taskcategories/project/<project_id>
GET all the Task Categories associated with a project or POST to add a new Task Category to a project based on the request body.

### .../taskcategories/<category_id>/delete
Delete a particular task category from a project.

### .../stats/tasks/weekly/<user_uid>
Get the number of tasks completed by a particular user on each day in the last 7 days.

### .../stats/basic/<user_uid>
Get the total tasks, completed tasks, and total projects for a particular user.

### .../stats/projects/tasks/<user_uid>
Get the total tasks and completed tasks for each of the five most recent projects a user has created.

### .../users/exist/<user_name>
Check if a user with a particular username already exists or not.

### .../collab/project/<project_id>
GET all collaborators on a project, POST to add a new collaborator to a project, or DELETE a collaborator from a project.

### .../collabs/projects/<user_uid>
GET all projects a particular user is collaborating on.

### .../collabs/verify/<project_id>
Check if a user is a collaborator on a particular project or not.

### .../collabs/getcollabsbyuid/<user_uid>
GET all the other users a particular user has collaborated with.

## Frontend
This REST web service serves data to a frontend web application made with React. See the frontend source code [here](https://github.com/saarthak2002/taskit-app) or visit the [deployed version](https://taskit-frontend-a7880b47804a.herokuapp.com/).

The essential features of the platform can be accessed on the go using the [task.it mobile app](https://github.com/saarthak2002/taskit-mobile) built with Flutter.

## Copyright
This application is developed by Saarthak Gupta © 2023.
