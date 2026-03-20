# Student Management System

A complete beginner-friendly student management system built with FastAPI, SQLAlchemy, MySQL, and Bootstrap 5.

## Features

- **Student Management**: Add, edit, delete, and view students
- **Subject Management**: Manage school subjects
- **Marks Management**: Enter and view student marks for different subjects
- **Web Interface**: User-friendly web interface using Bootstrap 5
- **REST API**: Full REST API for all operations

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy ORM, Pydantic
- **Database**: SQLite (file-based, no server required)
- **Frontend**: HTML, Bootstrap 5, Jinja2 Templates
- **Server**: Uvicorn

## Project Structure

```
student_management_fastapi/
│
├── app/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database configuration
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── crud.py                 # CRUD operations
│   ├── routers/
│   │   ├── student_routes.py   # Student API routes
│   │   └── subject_routes.py   # Subject API routes
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── students.html
│   │   ├── add_student.html
│   │   ├── edit_student.html
│   │   └── student_marks.html
│   └── static/                 # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # This file
```

## Database Schema

The application uses SQLite database with the following tables:

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd student_management_fastapi
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Open in browser**
   - Web Interface: http://127.0.0.1:8000
   - API Documentation: http://127.0.0.1:8000/docs

## API Endpoints

### Students
- `GET /api/students` - Get all students
- `GET /api/students/{id}` - Get student by ID
- `POST /api/students` - Create new student
- `PUT /api/students/{id}` - Update student
- `DELETE /api/students/{id}` - Delete student

### Subjects
- `GET /api/subjects` - Get all subjects
- `POST /api/subjects` - Create new subject

### Marks
- `GET /api/marks/{student_id}` - Get marks for a student
- `POST /api/marks` - Create marks entry
- `PUT /api/marks/{id}` - Update marks
- `DELETE /api/marks/{id}` - Delete marks

## Usage

1. **Dashboard**: Visit the home page to see an overview
2. **Students**: View all students, add new students, edit or delete existing ones
3. **Subjects**: View all subjects and add new subjects
4. **Marks**: Click "View Marks" for any student to see and add their marks
5. **API**: Use the `/docs` endpoint for interactive API documentation

## Default Subjects

The system comes with these default subjects:
- Maths
- Science
- English
- History
- Geography

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.