from app import app, db
from flask import jsonify, request
from app.models import UserInfo, Project, Task, TaskCategory

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
            task_category_name = data.get('task_category_name')
            task_category_color = data.get('task_category_color')

            new_task = Task(
                title=task_title,
                description=task_description,
                project_id=project_id,
                task_category_name=task_category_name,
                task_category_color=task_category_color
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
    
@app.route('/task/<task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Task not found'})

@app.route('/task/<task_id>/edit', methods=['POST'])
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if task:
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        task_category_name = data.get('task_category_name')
        task_category_color = data.get('task_category_color')
        task.title = title
        task.description = description
        task.task_category_name = task_category_name
        task.task_category_color = task_category_color
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    else:
        return jsonify({'error': 'Task not found'})
    
@app.route('/taskcategories/project/<project_id>', methods=['GET', 'POST'])
def get_and_create_task_categories(project_id):
    if request.method == 'GET':
        task_categories = []
        categories = TaskCategory.query.filter_by(project_id=project_id).all()
        for category in categories:
            task_categories.append(TaskCategory.serialize(category))
        return jsonify(task_categories)
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        color = data.get('color')
        new_category = TaskCategory(
            name=name,
            color=color,
            project_id=project_id
        )
        try:
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'message': 'New category created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/taskcategories/<category_id>/delete', methods=['POST'])
def delete_task_category(category_id):
    task_category = TaskCategory.query.filter_by(id=category_id).first()
    project = Project.query.filter_by(id=task_category.project_id).first()
    if task_category:
        if project:
            for task in project.tasks:
                if task.task_category_name == task_category.name:
                    task.task_category_name = 'None'
                    task.task_category_color = '#bab5b5'
            try:
                db.session.delete(task_category)
                db.session.commit()
                return jsonify({'message': 'Task category deleted successfully'})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Project not found'})
    else:
        return jsonify({'error': 'Task category not found'})
    