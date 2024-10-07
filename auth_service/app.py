from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime

from models import User
from config import Config, db  

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid credentials'}), 401

        token = jwt.encode({
            'username': user.username,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return render_template('login.html')


with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
