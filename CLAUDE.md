# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack Todo List/Task Management application with the following technology stack:

- **Frontend**: Angular (TypeScript-based SPA)
- **Backend**: Flask (Python)
- **Database**: SQLite (development/personal use; PostgreSQL recommended for production multi-user scenarios)

## Architecture

### Frontend Structure (Angular)

**Components**:
- `AppComponent` - Main container
- `TaskListComponent` - Task list display
- `TaskItemComponent` - Individual task rendering
- `TaskFormComponent` - Create/edit form
- `FilterBarComponent` - Filters and search UI
- `CategoryManagerComponent` - Category management

**Services**:
- `TaskService` - API communication for tasks
- `CategoryService` - Category operations
- `AuthService` - Authentication (Phase 2)

**Routing**:
- `/tasks` - Complete task list
- `/tasks/new` - Create new task
- `/tasks/:id/edit` - Edit task
- `/categories` - Category management

**State Management**: Use Angular services with RxJS Observables (or NgRx for complex scenarios)

### Backend Structure (Flask)

```
backend/
├── app.py              # Entry point
├── config.py           # Configuration
├── models.py           # SQLite table definitions
├── routes/
│   ├── tasks.py        # Task endpoints
│   ├── categories.py   # Category endpoints
│   └── auth.py         # Authentication (Phase 2)
├── database.db         # SQLite database file
└── requirements.txt    # Python dependencies
```

### Database Schema

**tasks**:
- `id` (INTEGER PRIMARY KEY)
- `title` (TEXT NOT NULL)
- `description` (TEXT)
- `created_at` (DATETIME)
- `due_date` (DATETIME)
- `priority` (TEXT) - 'high'/'medium'/'low'
- `status` (TEXT) - 'pending'/'completed'
- `category_id` (INTEGER FOREIGN KEY)

**categories**:
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `color` (TEXT) - hex color code
- `created_at` (DATETIME)

**users** (Phase 2):
- `id` (INTEGER PRIMARY KEY)
- `email` (TEXT UNIQUE)
- `password_hash` (TEXT)
- `name` (TEXT)

## API Endpoints

### Tasks
- `GET /api/tasks` - List all tasks (supports query params)
- `GET /api/tasks/:id` - Get single task
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/:id` - Update task
- `DELETE /api/tasks/:id` - Delete task
- `PATCH /api/tasks/:id/toggle` - Toggle completion status

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category
- `PUT /api/categories/:id` - Update category
- `DELETE /api/categories/:id` - Delete category

### Query Parameters (Filtering)
- `?status=completed|pending`
- `?priority=high|medium|low`
- `?category_id=X`
- `?search=text`

## Development Commands

### Frontend (Angular)
```bash
# Development server (runs on port 4200)
ng serve

# Build for production
ng build

# Run tests
ng test

# Run linting
ng lint
```

### Backend (Flask)
```bash
# Run development server (port 5000)
python app.py
# or
flask run

# Install dependencies
pip install -r requirements.txt
```

### Setup Notes
- Flask must be configured with **Flask-CORS** to accept requests from `localhost:4200`
- SQLite database auto-creates on first run
- Use SQLAlchemy ORM (not raw SQL queries) for better maintainability

## Key Dependencies

### Python (Backend)
- Flask
- Flask-CORS
- SQLAlchemy - ORM for database operations
- Flask-Migrate - Database migrations

### Angular (Frontend)
- HttpClient (built-in)
- Angular Material or PrimeNG - UI components
- RxJS - Async operations and state management

## Development Plan (Sprints)

**Sprint 1 (MVP)**:
- Setup Angular and Flask projects
- SQLite database with tasks table
- Complete CRUD operations for tasks
- Basic UI (list and form)

**Sprint 2**:
- Implement categories
- Add filters and search
- Improve UI/UX

**Sprint 3**:
- Authentication system
- User-specific tasks
- Complete error handling

**Sprint 4**:
- Advanced validation
- Date picker and reminders
- Data export/import functionality

## Technical Considerations

- **ORM Usage**: Always use SQLAlchemy ORM instead of raw SQL for maintainability
- **Validation**: Implement on both Angular (client-side) and Flask (server-side)
- **Timezone Handling**: Handle timezones correctly for due dates and created_at fields
- **Pagination**: Implement if expecting large numbers of tasks
- **Database**: SQLite is single-user; consider PostgreSQL for production multi-user deployments

## Typical Workflow Example

**Creating a Task**:
1. User fills form in Angular (`TaskFormComponent`)
2. Component collects data
3. `TaskService` sends POST to Flask `/api/tasks`
4. Flask validates and inserts into SQLite using SQLAlchemy
5. Flask returns created task (JSON)
6. Angular updates displayed task list via Observable

**Filtering Tasks**:
1. User selects filter (e.g., "High priority")
2. `FilterBarComponent` emits event
3. `TaskListComponent` calls `TaskService.getTasks({priority: 'high'})`
4. Flask executes SQLite query with WHERE clause
5. Returns filtered results
6. Angular renders filtered list
