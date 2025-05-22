from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from sqlalchemy import create_engine
from config import DATA_DIR
import os

# Инициализация приложения
app = Flask(__name__)
app.secret_key = os.getenv('WEB_SECRET_KEY', 'dev-secret-key')

# Подключение к существующей БД
engine = create_engine(f'sqlite:///{DATA_DIR}/bookings.db')
app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель администратора
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

# Маршруты
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            login_user(admin)
            return redirect(url_for('templates'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/templates')
@login_required
def templates():
    templates = db.session.query(MessageTemplate).all()
    return render_template('templates.html', templates=templates)

@app.route('/edit_template/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_template(id):
    template = MessageTemplate.query.get_or_404(id)
    if request.method == 'POST':
        template.name = request.form['name']
        template.content = request.form['content']
        template.trigger_event = request.form['trigger']
        template.is_active = 'is_active' in request.form
        db.session.commit()
        return redirect(url_for('templates'))
    return render_template('edit_template.html', template=template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)