from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        
        messages = Message.query.order_by(Message.created_at.asc()).all()
        messages_list = [message.to_dict() for message in messages]
        return make_response(jsonify(messages_list), 200)

    elif request.method == 'POST':
        
        body = request.form.get('body')
        username = request.form.get('username')
        if not body or not username:
            return make_response({"error": "Missing body or username"}, 400)
        
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        
        return make_response(new_message.to_dict(), 201)

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    
    message = Message.query.get(id)
    
    if not message:
        return make_response({"error": "Message not found"}, 404)
    
    if request.method == 'PATCH':
        
        body = request.form.get('body')
        if body:
            message.body = body
            db.session.commit()
        
        return make_response(message.to_dict(), 200)
    
    elif request.method == 'DELETE':
        
        db.session.delete(message)
        db.session.commit()
        
        return make_response({"message": "Message deleted"}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)