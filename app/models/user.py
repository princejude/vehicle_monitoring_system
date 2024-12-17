from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "user"  # Explicit table name for clarity and consistency

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="user")  # Options: "admin" or "user"
    active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    # ----- Password Management -----
    def set_password(self, password):
        """
        Hashes and stores the user's password securely.
        """
        if not password:
            raise ValueError("Password cannot be empty.")
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifies the user's password against the stored hash.
        """
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    # ----- Flask-Login Properties -----
    @property
    def is_active(self):
        """
        Returns True if the user is active.
        """
        return self.active

    @property
    def is_authenticated(self):
        """
        Returns True for authenticated users.
        """
        return True

    @property
    def is_anonymous(self):
        """
        Returns False for non-anonymous users.
        """
        return False

    def get_id(self):
        """
        Returns the unique identifier for the user.
        """
        return str(self.id)

    # ----- Helper Methods -----
    def promote_to_admin(self):
        """
        Promote the user to an admin role.
        """
        self.role = "admin"
        self.is_admin = True

    def deactivate(self):
        """
        Deactivate the user account.
        """
        self.active = False

    def activate(self):
        """
        Activate the user account.
        """
        self.active = True

    def __repr__(self):
        """
        Represent the user object as a string.
        """
        return f"<User(username='{self.username}', role='{self.role}', active={self.active})>"
