from flask import Blueprint, request, jsonify
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status')
        priority = request.args.get('priority')
        category_id = request.args.get('category_id')
        search = request.args.get('search')

        # Start with base query
        query = Task.query

        # Apply filters
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if category_id:
            query = query.filter_by(category_id=int(category_id))
        if search:
            query = query.filter(Task.title.contains(search))

        # Execute query and get all tasks
        tasks = query.order_by(Task.created_at.desc()).all()

        return jsonify({
            'success': True,
            'tasks': [task.to_dict() for task in tasks],
            'count': len(tasks)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Title is required'
            }), 400

        # Create new task
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            status=data.get('status', 'pending'),
            category_id=data.get('category_id')
        )

        # Handle due_date if provided
        if 'due_date' in data and data['due_date']:
            try:
                new_task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid due_date format. Use ISO format.'
                }), 400

        # Validate priority
        if new_task.priority not in ['high', 'medium', 'low']:
            return jsonify({
                'success': False,
                'error': 'Priority must be high, medium, or low'
            }), 400

        # Save to database
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'success': True,
            'task': new_task.to_dict(),
            'message': 'Task created successfully'
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a single task by ID"""
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'task': task.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404

        data = request.get_json()

        # Update fields if provided
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            if data['priority'] not in ['high', 'medium', 'low']:
                return jsonify({
                    'success': False,
                    'error': 'Priority must be high, medium, or low'
                }), 400
            task.priority = data['priority']
        if 'status' in data:
            if data['status'] not in ['pending', 'completed']:
                return jsonify({
                    'success': False,
                    'error': 'Status must be pending or completed'
                }), 400
            task.status = data['status']
        if 'category_id' in data:
            task.category_id = data['category_id']
        if 'due_date' in data:
            if data['due_date']:
                try:
                    task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid due_date format. Use ISO format.'
                    }), 400
            else:
                task.due_date = None

        db.session.commit()

        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': 'Task updated successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@tasks_bp.route('/tasks/<int:task_id>/toggle', methods=['PATCH'])
def toggle_task(task_id):
    """Toggle task completion status"""
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({
                'success': False,
                'error': 'Task not found'
            }), 404

        # Toggle status
        task.status = 'completed' if task.status == 'pending' else 'pending'
        db.session.commit()

        return jsonify({
            'success': True,
            'task': task.to_dict(),
            'message': f'Task marked as {task.status}'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
