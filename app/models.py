from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, DateTime
from . import db, login_manager


class User(UserMixin, db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
        is_active (bool): Indicates whether the user is active or not.
        last_login (DateTime): The date and time of the user's last login (optional).
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_login: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    # Relationships
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="user"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Activity(db.Model):
    """
    Represents an activity in the system.

    Attributes:
        id (int): The unique identifier for the activity.
        description (str): The description of the activity.
        type (str): The type of the activity.
        participants (int): The number of participants for the activity.
        user_id (int): The ID of the user who saved the activity.
    """

    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(256))
    type: Mapped[str] = mapped_column(String(64))
    participants: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("users.id"))

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity {self.description}>"
