import os

from rollie import db, bcrypt
from rollie.models import User, Plant, Community
from rollie.enums import UserRole
from rollie.utils.helper import (
    gen_community_id, time_now_ist
)


def init_data():
    # Add plants
    plants_data = [
        {"name": "North Waste Plant", "location": "North City"},
        {"name": "South Waste Plant", "location": "South City"},
        {"name": "East Waste Plant", "location": "East City"}
    ]

    plants = []
    for p in plants_data:
        plant = Plant.query.filter_by(name=p["name"]).first()
        if not plant:
            plant = Plant(
                name=p["name"],
                location=p["location"],
                created_date=time_now_ist()
            )
            db.session.add(plant)
            db.session.commit()
        plants.append(plant)

    # Add communities
    communities_data = [
        {"name": "Community A", "plant": plants[0]},
        {"name": "Community B", "plant": plants[0]},
        {"name": "Community C", "plant": plants[1]},
        {"name": "Community D", "plant": plants[2]},
    ]

    for c in communities_data:
        community = Community.query.filter_by(name=c["name"]).first()
        if not community:
            community = Community(
                name=c["name"],
                unique_id=gen_community_id(),
                plant_id=c["plant"].id,
                created_date=time_now_ist()
            )
            db.session.add(community)
            db.session.commit()


    # Add operators
    operators_data = [
        {"name": "North Operator", "email": "north.operator@rollienowaste.com", "plant": plants[0]},
        {"name": "South Operator", "email": "south.operator@rollienowaste.com", "plant": plants[1]},
        {"name": "East Operator", "email": "east.operator@rollienowaste.com", "plant": plants[2]},
    ]

    for op in operators_data:
        existing_user = User.query.filter_by(email=op["email"]).first()
        if existing_user:
            continue

        hashed_password = bcrypt.generate_password_hash(os.getenv("TMP_PASSWORD")).decode("utf-8")
        user = User(
            name=op["name"],
            email=op["email"],
            password=hashed_password,
            role=UserRole.PLANT_OPERATOR,
            plant_id=op["plant"].id,
            community_id=None
        )
        db.session.add(user)
        db.session.commit()

    # Add scanner
    existing_user = User.query.filter_by(email="scanner@rollienowaste.com").first()
    if not existing_user:   
        hashed_password = bcrypt.generate_password_hash(os.getenv("TMP_PASSWORD")).decode("utf-8")
        user = User(
            name="Scanner",
            email="scanner@rollienowaste.com",
            password=hashed_password,
            role=UserRole.SCANNER,
            plant_id=None,
            community_id=None
        )
        db.session.add(user)
        db.session.commit()
