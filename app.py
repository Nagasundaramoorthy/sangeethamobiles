from flask import render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from models import db, User, app

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            user.online = True
            db.session.commit()
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        users = User.query.filter(User.username != session['username'], User.online == True).all()
        return render_template('dashboard.html', users=users, username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        if user:
            user.online = False
            db.session.commit()
        session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('initiate_call')
def initiate_call(data):
    recipient = data['recipient']
    caller = data['caller']
    emit('incoming_call', {'caller': caller}, room=recipient)  # Notify recipient

@socketio.on('accept_call')
def accept_call(data):
    caller = data['caller']
    recipient = data['recipient']
    emit('call_accepted', {'recipient': recipient}, room=caller)  # Notify caller

@socketio.on('join')
def join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{username} has entered the room.'}, room=room)

# WebSocket: Leave Room
@socketio.on('leave')
def leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{username} has left the room.'}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)