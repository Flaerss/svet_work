from flask_login import UserMixin
from datetime import datetime
from web_interface import db

class MessageTemplate(db.Model):
    """Шаблоны сообщений"""
    __tablename__ = 'message_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    content = db.Column(db.Text, nullable=False)
    trigger_event = db.Column(db.String(30))  # booking_create, booking_update и т.д.
    platform = db.Column(db.String(10))       # telegram, whatsapp
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(UserMixin, db.Model):
    """Администраторы системы"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admin {self.username}>"