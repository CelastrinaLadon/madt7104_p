# create_tables.py
import random
import bcrypt
from sqlalchemy.exc import IntegrityError

from models.db import Base, engine, SessionLocal
from models.auth import User
from models.activities import Activities
from models.location import Location, LocationActivities

from models.db import Base, engine
from models.auth import User  # make sure this import is correct
from models.activities import Activities
from models.location import Location, LocationActivities
from models.party import Party, PartyPlayer


Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
db = SessionLocal()

# 3. Create default user 'tia' with password 'asdf'
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

# 4. Create activities
activity_names = ["football", "boardgame", "bat", "badminton", "basketball", "tennis", "yoga", "cycling", "volleyball", "run",
                  "swimming", "pingpong", "golf", "darts", "futsal", "e-sports", "karaoke", "bowling", "chess", "poker"]

activity_objs = []
for name in activity_names:
    activity = Activities(name=name, description=f"{name.capitalize()} activity")
    db.add(activity)
    activity_objs.append(activity)
db.commit()
print(f"✅ Created {len(activity_objs)} activities")

# 5. Create 20 locations in Bangkok (GBKK)
for i in range(1, 21):
    location = Location(
        name=f"GBKK Venue {i}",
        address=f"{i} Sukhumvit Road, Bangkok",
        lat=str(round(13.7 + random.uniform(-0.1, 0.1), 6)),
        long=str(round(100.5 + random.uniform(-0.1, 0.1), 6))
    )
    db.add(location)
    db.flush()  # To get location_id

    # Randomly assign 2–4 activities with random prices
    selected_acts = random.sample(activity_objs, k=random.randint(2, 4))
    for act in selected_acts:
        loc_act = LocationActivities(
            location_id=location.location_id,
            activity_id=act.activity_id,
            price=random.randint(100, 500)
        )
        db.add(loc_act)

db.commit()
print("✅ Created 20 locations with random activities")

# Close session
db.close()