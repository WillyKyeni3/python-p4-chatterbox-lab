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
        # messages = []
        messages = [message.to_dict() for message in Message.query.all()]
        # for message in Message.query.all():
        #     message_dict=message.to_dict()
        #     messages.append(message_dict)
        
        # response = make_response(
        #     messages,
        #     200
        # )


        return make_response(jsonify(messages), 200)

    elif request.method == 'POST':
        data = request.json
        new_message = Message(
            
            body = data.get("body"),
            username = data.get("username"),
           
        )

        db.session.add(new_message)
        db.session.commit()

        # message_dict = new_message.to_dict()

        # response = make_response(
        #     message_dict,
        #     201
        # )

        return make_response(jsonify(new_message.to_dict()), 201)


@app.route('/messages/<int:id>', methods=['GET','PATCH', 'DELETE'])
def messages_by_id(id):
    message=Message.query.filter(Message.id == id).first()

    if message is None:
        return make_response(jsonify(message.to_dict()), 200)
    

    
    if request.method == 'GET':
            return make_response(jsonify(message.to_dict()), 200)
    
       
    elif request.method == 'PATCH':
        data = request.json

        for attr in data:
            setattr(message, attr, data.get(attr))

        db.session.commit()
        return make_response(jsonify(message.to_dict()), 200)

            
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return make_response(jsonify({
            "delete_successful": True,
            "message": "Message deleted."
        }), 200) 
    
with app.app_context():
    # Create a test message
    test_message = Message(body="Test", username="Tester")
    db.session.add(test_message)
    db.session.commit()

    m = Message.query.first()
    id = m.id

if __name__ == '__main__':
    app.run(port=5555)