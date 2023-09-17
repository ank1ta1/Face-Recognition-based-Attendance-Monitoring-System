import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facerecattendance-1a20c-default-rtdb.firebaseio.com/"
})

# creates students directory
ref = db.reference('Students')

data = {
    "852741":
        {
            "name": "Emily blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 10,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2022,
            "total_attendance": 2,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
    "464635":
        {
            "name": "Gigi Hadid",
            "major": "Engineering",
            "starting_year": 2020,
            "total_attendance": 20,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
    "525267":
        {
            "name": "Rishi Sunak",
            "major": "Political Science",
            "starting_year": 2021,
            "total_attendance": 14,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
    "698830":
        {
            "name": "Barack Obama",
            "major": "History",
            "starting_year": 2021,
            "total_attendance": 13,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-07-11 00:54:34"
        },
}

for key, value in data.items():
    ref.child(key).set(value)