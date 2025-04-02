import random
import bcrypt
from sqlalchemy.exc import IntegrityError
from models.db import Base, engine, SessionLocal
from models.auth import User
from models.activities import Activities
from models.location import Location, LocationActivities

# Initialize database and create tables
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
db = SessionLocal()

# Create default user 'tia' with password 'asdf'
try:
    hashed_pw = bcrypt.hashpw("asdf".encode(), bcrypt.gensalt()).decode()
    user = User(
        username="tia",
        password_hash=hashed_pw,
        email="tia@example.com",
        phone_number="0812345678"
    )
    db.add(user)
    db.commit()
    print("✅ Created default user 'tia'")
except IntegrityError:
    db.rollback()
    print("⚠️ User 'tia' already exists")

# Create activities
activity_names = [
    "Football", "Board Game", "Badminton", "Basketball", "Tennis",
    "Yoga", "Cycling", "Volleyball", "Running", "Swimming",
    "Table Tennis", "Golf", "Darts", "Futsal", "E-Sports",
    "Karaoke", "Bowling", "Chess", "Poker", "Muay Thai"
]

activity_objs = []
for name in activity_names:
    activity = Activities(name=name, description=f"{name} activity")
    db.add(activity)
    activity_objs.append(activity)
db.commit()
print(f"✅ Created {len(activity_objs)} activities")

# Real-world sports venues in Bangkok
venues = [
    {
        "name": "Rajamangala National Stadium",
        "address": "286 Hua Mak Rd, Hua Mak, Bang Kapi District, Bangkok 10240",
        "lat": "13.7629",
        "long": "100.6108"
    },
    {
        "name": "Lumpinee Boxing Stadium",
        "address": "6 Ram Inthra Rd, Anusawari, Bang Khen, Bangkok 10220",
        "lat": "13.8774",
        "long": "100.6042"
    },
    {
        "name": "The Racquet Club",
        "address": "8 Sukhumvit 49/9 Alley, Khlong Tan Nuea, Watthana, Bangkok 10110",
        "lat": "13.7350",
        "long": "100.5795"
    },
    {
        "name": "Rock Domain Climbing Gym",
        "address": "1780 Bangna-Trad Rd, Bang Na, Bangkok 10260",
        "lat": "13.6685",
        "long": "100.6348"
    },
    {
        "name": "The Rink Ice Arena",
        "address": "7th Floor, CentralWorld, 999/9 Rama I Rd, Pathum Wan, Bangkok 10330",
        "lat": "13.7465",
        "long": "100.5396"
    },
    {
        "name": "Bangkok Batting Center",
        "address": "4 Soi Sukhumvit 31, Khlong Toei Nuea, Watthana, Bangkok 10110",
        "lat": "13.7424",
        "long": "100.5670"
    },
    {
        "name": "Yokkao Training Center Bangkok",
        "address": "49 Sukhumvit Soi 16, Khlong Toei, Bangkok 10110",
        "lat": "13.7300",
        "long": "100.5600"
    },
    {
        "name": "D-Sports Stadium",
        "address": "123 Sukhumvit 71 Rd, Phra Khanong Nuea, Watthana, Bangkok 10110",
        "lat": "13.7222",
        "long": "100.5931"
    },
    {
        "name": "The Royal Bangkok Sports Club",
        "address": "1 Henri Dunant St, Pathum Wan, Bangkok 10330",
        "lat": "13.7392",
        "long": "100.5345"
    },
    {
        "name": "Rajadamnern Stadium",
        "address": "1 Ratchadamnoen Nok Rd, Pom Prap Sattru Phai, Bangkok 10100",
        "lat": "13.7691",
        "long": "100.5110"
    }
]

# Add venues to the database with associated activities
for venue in venues:
    location = Location(
        name=venue["name"],
        address=venue["address"],
        lat=venue["lat"],
        long=venue["long"]
    )
    db.add(location)
    db.flush()  # To get location_id

    # Randomly assign 2–4 activities with random prices
    selected_activities = random.sample(activity_objs, k=random.randint(2, 4))
    for activity in selected_activities:
        loc_act = LocationActivities(
            location_id=location.location_id,
            activity_id=activity.activity_id,
            price=random.randint(100, 500)
        )
        db.add(loc_act)

db.commit()
print(f"✅ Created {len(venues)} real-world locations with associated activities")

# Close session
db.close()
