from flask import Flask,request,jsonify,make_response
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)


class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=True)
    done = db.Column(db.Boolean, default=False)

class TodoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TodoModel
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    done = fields.Boolean(required=True)
    

#db.create_all()
'''
Authentication
'''
@auth.get_password
def get_password(username):
	if username == 'sarang':
		return 'python'
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({ 'error': 'unauthorized Access' }), 403)

@app.route('/todo/api/v1.0/tasks/<int:todo_id>', methods = ['GET'])
@auth.login_required
def get(todo_id):
        task = TodoModel.query.filter_by(id=todo_id).first()
        if not task:
            abort(404)
        todo_schema = TodoSchema()
        result = todo_schema.dump(task)
        return make_response(jsonify({"Task": result}))
        
@app.route('/todo/api/v1.0/tasks', methods = ['GET'])
@auth.login_required
def get_list():
    tasks = TodoModel.query.all()
    todo_schema = TodoSchema(many=True)
    task_list = todo_schema.dump(tasks)
    return make_response(jsonify({"task": task_list}))
    

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = TodoModel.query.filter_by(id=task_id).first()
    
    if task == None:
        abort(400)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"ID Deleted": task_id}))

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
@auth.login_required
def update_task(task_id):
    data = request.get_json(force=True)
    
    task = TodoModel.query.filter_by(id=task_id).first()
    
    if not task:
        abort(404, message="Could not find task with that id")
    if data.get('title'):
        task.title = data['title']
    if data.get('description'):
        task.description = data['description']
    if data.get('done'):
        task.done = data['done']
    db.session.commit()
    
    todo_schema = TodoSchema(only=['id', 'title', 'description','done'])
    result = todo_schema.dump(task)
    return make_response(jsonify({"task": result}))

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def post():
    task = {
	'title': request.json['title'],
	'description': request.json.get('description', ""),
	'done': request.json.get('done', "False")
	}
    todo = TodoModel(title=task['title'], description=task['description'],done = task['done'])  
    
    db.session.add(todo)
    db.session.commit()

    todo_schema = TodoSchema()
    result = todo_schema.dump(todo)
    return make_response(jsonify({"Task": result}),200)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({ 'error' : 'Could not find task with that id' }), 404)
@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify({ 'error' : 'Method Not Allowed' }), 405)
@app.errorhandler(400)
def Bad_Request(error):
	return make_response(jsonify({ 'error' : 'Bad Requestss' }), 400)

@app.errorhandler(500)
def internal_server_Error(error):
	return make_response(jsonify({ 'error' : 'Internal Server Error' }), 500)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)