# Omnify_Assignment
Python Developer Assignment (1+ Years Experience)
# 🧘 Fitness Studio Booking API

Simple Django-based API for booking fitness classes (Yoga, Zumba, HIIT).

## 🔧 Setup Instructions

```bash
git clone (https://github.com/Usaib21/Omnify_Assignment.git)
cd fitness_booking

python -m venv .venv
# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


| Method | Endpoint               | Description                         |
| ------ | ---------------------- | ----------------------------------- |
| GET    | `/api/classes`         | List all available fitness classes  |
| POST   | `/api/book`            | Book a fitness class                |
| GET    | `/api/bookings?email=` | Retrieve bookings for a given email |


📦 API Usage Examples
🧾 1. GET /api/classes
Request:

GET http://localhost:8000/api/classes
Response:

[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-06-17T10:00:00Z",
    "instructor": "Aman",
    "available_slots": 5
  },
  {
    "id": 2,
    "name": "HIIT",
    "datetime": "2025-06-18T17:00:00Z",
    "instructor": "Priya",
    "available_slots": 2
  }
]
📝 2. POST /api/book
Request:

POST http://localhost:8000/api/book
Content-Type: application/json

Body:

{
  "class_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com"
}
Response:

{
  "id": 5,
  "fitness_class": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "created_at": "2025-06-16T15:45:00Z"
}
📨 3. GET /api/bookings?email=
Request:

GET http://localhost:8000/api/bookings?email=john@example.com
Response:

[
  {
    "id": 5,
    "fitness_class": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "created_at": "2025-06-16T15:45:00Z"
  }
]
