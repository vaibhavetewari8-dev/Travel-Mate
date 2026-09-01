from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    destination = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, default="")
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    budget = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    itinerary_days = db.relationship(
        "ItineraryDay", backref="trip", cascade="all, delete-orphan"
    )
    expenses = db.relationship(
        "Expense", backref="trip", cascade="all, delete-orphan"
    )
