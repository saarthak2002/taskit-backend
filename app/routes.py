from app import app, db
from flask import jsonify, request
from app.models import UserInfo, Project, Task

@app.route('/', methods=['GET'])
def index():
    return "Hello, world!"

@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        user_list = []
        users = UserInfo.query.all()
        for user in users:
            user_list.append(UserInfo.serialize(user))
        return jsonify(user_list)
    
    elif request.method == 'POST':
        data = request.get_json()
        user_uid = data.get('userUID')
        username = data.get('username')
        first_name = data.get('firstName')
        last_name = data.get('lastName')

        existing_user = UserInfo.query.filter_by(userUID=user_uid).first()
        if existing_user:
            return jsonify({'error': 'User with the same userUID already exists'})
        
        existing_user = UserInfo.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'User with the same username already exists'})

        new_user = UserInfo(
            userUID=user_uid,
            username=username,
            firstName=first_name,
            lastname=last_name
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'New user created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/users/<user_uid>', methods=['GET'])
def get_user_info_by_uid(user_uid):
    user = UserInfo.query.filter_by(userUID=user_uid).first()
    if user:
        return jsonify(UserInfo.serialize(user))
    else:
        return jsonify({'error': 'User not found'})
    
@app.route('/projects', methods=['GET', 'POST'])
def get_and_create_project():
    if request.method == 'GET':
        project_list = []
        projects = Project.query.all()
        for project in projects:
            project_list.append(Project.serialize(project))
        return jsonify(project_list)
    
    elif request.method == 'POST':
        data = request.get_json()
        user_uid = data.get('userUID')
        title = data.get('title')
        description = data.get('description')

        new_project = Project(
            userUID=user_uid,
            title=title,
            description=description,
        )

        try:
            db.session.add(new_project)
            db.session.commit()
            return jsonify({'message': 'New project created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/projects/<user_uid>', methods=['GET'])
def get_projects_by_user_uid(user_uid):
    if request.method == 'GET':
        project_list = []
        projects = Project.query.filter_by(userUID=user_uid).all()
        for project in projects:
            project_list.append(Project.serialize(project))
        return jsonify(project_list)
    
@app.route('/projects/id/<project_id>', methods=['GET'])
def get_project_by_id(project_id):
    if request.method == 'GET':
        project = Project.query.filter_by(id=project_id).first()
        if project:
            return jsonify(Project.serialize(project))
        else:
            return jsonify({'error': 'Project not found'})
        
@app.route('/projects/<project_id>/tasks', methods=['POST'])
def add_task_to_project(project_id):
    if request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=project_id).first()
        if project:
            task_title = data.get('title')
            task_description = data.get('description')

            new_task = Task(
                title=task_title,
                description=task_description,
                project_id=project_id
            )

            try:
                db.session.add(new_task)
                db.session.commit()
                return jsonify({'message': 'New task created successfully'})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Project not found'})


@app.route('/projects/<project_id>/tasks', methods=['GET'])
def get_all_tasks_for_project(project_id):
    if request.method == 'GET':
        task_list = []
        tasks = Task.query.filter_by(project_id=project_id).all()
        for task in tasks:
            task_list.append(Task.serialize(task))
        return jsonify(task_list)
    
@app.route('/task/<task_id>/complete', methods=['POST'])
def mark_task_as_completed(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if(task.status == 'completed'):
        return jsonify({'error': 'Task already completed'})
    else:
        task.status = 'completed'
        db.session.commit()
        return jsonify({'message': 'Task marked as completed'})


@app.route('/task/<task_id>/pending', methods=['POST'])
def mark_task_as_pending(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if(task.status == 'pending'):
        return jsonify({'error': 'Task already pending'})
    else:
        task.status = 'pending'
        db.session.commit()
        return jsonify({'message': 'Task marked as pending'})
