from app import app, db
from flask import jsonify, request
from app.models import UserInfo, Project, Task, TaskCategory, Collaborator
from datetime import datetime
from datetime import timedelta
from sqlalchemy import desc
from sqlalchemy.sql import func

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
    
@app.route('/users/search/<search>', methods=['GET'])
def search_by_username(search):
    search_term = f"%{search}%"
    results = UserInfo.query.filter(func.lower(UserInfo.username).like(func.lower(search_term))).all()
    return jsonify([UserInfo.serialize(user) for user in results])
    
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
            task_created_by_uid = data.get('created_by_user_uid')
            print(task_created_by_uid)
            userInfo = None
            if task_created_by_uid:
                print('here')
                userInfo = UserInfo.query.filter_by(userUID=task_created_by_uid).first()

            new_task = Task(
                title=task_title,
                description=task_description,
                project_id=project_id,
                task_category_name=task_category_name,
                task_category_color=task_category_color,
                created_by=userInfo.firstName + ' ' + userInfo.lastname if userInfo else None
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
        tasks = Task.query.filter_by(project_id=project_id).order_by(desc(Task.date_added)).all()
        for task in tasks:
            task_list.append(Task.serialize(task))
        return jsonify(task_list)
    
@app.route('/task/<task_id>/complete', methods=['POST'])
def mark_task_as_completed(task_id):
    data = request.get_json()
    task = Task.query.filter_by(id=task_id).first()
    if(task.status == 'completed'):
        return jsonify({'error': 'Task already completed'})
    else:
        task.status = 'completed'
        task.completed_at_time = datetime.now().isoformat()
        task.completed_by = data.get('completed_by')
        db.session.commit()
        return jsonify({'message': 'Task marked as completed'})


@app.route('/task/<task_id>/pending', methods=['POST'])
def mark_task_as_pending(task_id):
    task = Task.query.filter_by(id=task_id).first()
    if(task.status == 'pending'):
        return jsonify({'error': 'Task already pending'})
    else:
        task.status = 'pending'
        task.completed_at_time = None
        task.completed_by = None
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

@app.route('/stats/tasks/weekly/<user_uid>', methods=['GET'])
def get_weekly_task_stats(user_uid):
    if request.method == 'GET':
        task_counts = {}
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)

        current_date = start_date
        while current_date <= end_date:
            task_counts[current_date.date()] = 0
            current_date += timedelta(days=1)

        projects = Project.query.filter_by(userUID=user_uid).all()
        for project in projects:
            for task in project.tasks:
                if task.completed_at_time and start_date <= datetime.fromisoformat(task.completed_at_time) <= end_date:
                    completion_date = datetime.fromisoformat(task.completed_at_time).date()
                    if completion_date not in task_counts:
                        task_counts[completion_date] = 1
                    else:
                        task_counts[completion_date] += 1
        response_data = [{'date': str(date), 'completed_tasks': count} for date, count in task_counts.items()]
        return jsonify(response_data)
    
@app.route('/stats/basic/<user_uid>', methods=['GET'])
def get_basic_stats(user_uid):
    projects = Project.query.filter_by(userUID=user_uid).all()
    total_tasks = 0
    completed_tasks = 0
    for project in projects:
        for task in project.tasks:
            total_tasks += 1
            if task.status == 'completed':
                completed_tasks += 1
    return jsonify({'total_tasks': total_tasks, 'completed_tasks': completed_tasks, 'total_projects': len(projects)})

@app.route('/stats/projects/tasks/<user_uid>', methods=['GET'])
def get_recent_projects_bar_graph(user_uid):
    recent_projects = Project.query.filter_by(userUID=user_uid).order_by(desc(Project.date_added)).limit(5).all()
    response_data = []
    for project in recent_projects:
        completed_tasks = 0
        total_tasks = len(project.tasks)
        for task in project.tasks:
            if task.status == 'completed':
                completed_tasks += 1
        response_data.append({'title': project.title, 'completed_tasks': completed_tasks, 'total_tasks': total_tasks})  
    return jsonify(response_data)

@app.route('/users/exist/<username>', methods=['GET'])
def does_username_exist(username):
    user = UserInfo.query.filter_by(username=username).first()
    if user:
        return jsonify({'exists': True})
    else:
        return jsonify({'exists': False})
    
@app.route('/collab/project/<project_id>', methods=['GET', 'POST'])
def add_or_get_collab_to_project(project_id):
    if request.method == 'GET':
        project = Project.query.filter_by(id=project_id).first()
        if project:
            collabs = Collaborator.query.filter_by(project_id=project_id).all()
            return jsonify([Collaborator.serialize(collab) for collab in collabs])
        else:
            return jsonify({'error': 'Project not found'})
    elif request.method == 'POST':
        data = request.get_json()
        project = Project.query.filter_by(id=project_id).first()
        if project:
            if Collaborator.query.filter_by(project_id=project_id, userUID=data.get('userUID')).first():
                return jsonify({'error': 'Collaborator already exists'})
            new_collab = Collaborator(
                project_id=project_id,
                userUID=data.get('userUID'),
            )
            try:
                db.session.add(new_collab)
                db.session.commit()
                return jsonify({'message': 'New collaborator added successfully'})
            except Exception as e:
                return jsonify({'error': str(e)})
        else:
            return jsonify({'error': 'Project not found'})

@app.route('/collabs/projects/<user_uid>', methods=['GET'])
def get_collab_projects_for_user(user_uid):
    projects = []
    collabs = Collaborator.query.filter_by(userUID=user_uid).all()
    for collab in collabs:
        project = Project.query.filter_by(id=collab.project_id).first()
        if project:
            projects.append(Project.serialize(project))
    return jsonify(projects)

@app.route('/collabs/verify/<project_id>', methods=['POST'])
def check_if_user_is_a_collaborator(project_id):
    data = request.get_json()
    user_uid = data.get('userUID')
    collab = Collaborator.query.filter_by(project_id=project_id, userUID=user_uid).first()
    if collab:
        return jsonify({'is_collab': True})
    else:
        return jsonify({'is_collab': False})
   