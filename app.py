from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Замените на более сложный ключ в продакшене
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Путь к вашей базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных и системы логина
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

mail = Mail(app)

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Создание базы данных
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут выбора между логином и регистрацией
@app.route('/choose', methods=['GET'])
def choose():
    return render_template('choose.html')

# Маршрут регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Проверка на существующий аккаунт
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('An account with this username or email already exists.')
            return redirect(url_for('choose'))

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Создание нового пользователя
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

# Маршрут логина
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('profile'))

        flash('Invalid email or password. Please try again.')
        return redirect(url_for('login'))

    return render_template('login.html')

# Страница профиля
@app.route('/profile')
@login_required
def profile():
    return f'Hello, {current_user.username}!'

# Маршрут выхода из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
