from flask import Flask, jsonify, request, Response, json

app = Flask(__name__)

question_list = [
	
	{
		'question': 'What is Github',
		'answer': 'GitHub Inc. is a web-based hosting service for version control using Git.',
		'q_id': 1

	},

	{
		'question':'What is Pivotal Tracker?',
		'answer': 'Pivotal Tracker is a straightforward project-planning tool.',
		'q_id': 2

	}

]

def sanitize_input(usr_input):
	if ("question" in usr_input and "answer" in usr_input and "q_id" in usr_input):
		return True
	else:
		return False


@app.route('/questions')
def return_all_questions():
	return jsonify({'question_list': question_list})

@app.route('/questions/<int:q_id>')
def return_single_question(q_id):
	val = {}
	for question in question_list:
		if question["q_id"] == q_id:
			val = {
				'question': question["question"],
				'answer': question["answer"],
				'q_id': question["q_id"]
			}
	return jsonify(val)




@app.route('/questions', methods=['POST'])
def post_question():
	request_data = request.get_json()
	if(sanitize_input(request_data)):
		new_question = {
			"question": request_data['question'],
			"answer": request_data['answer'],
			"q_id": request_data['q_id']
		}
		question_list.insert(0, new_question)
		response = Response("", 201, mimetype='application/json')
		response.headers['Location'] = "/questions/"+ str(new_question['q_id'])
		return response
	else:
		invalid_question = {
			"error": "Invalid quetion passed in request",
			"help": "Data should be in the format {'question': 'asked question', 'answer':'given answer', 'q_id''question id as an integer'"
		}
		response = Response(json.dumps(invalid_question), 400, mimetype='application/json')
		return response

@app.route('/questions/<int:q_id>', methods=['PATCH'])
def update_question(q_id):
	request_data = request.get_json()
	updated_question = {}
	if ("answer" in request_data):
		updated_question["answer"] = request_data['answer']
	if ("question" in request_data):
		updated_question["question"] = request_data['question']
	for question in question_list:
		if question["q_id"] == q_id:
			question.update(updated_question)
	response = Response("", 204)
	response.headers['Location'] = "/questions/" + str(q_id)
	return response


@app.route('/questions/<int:q_id>', methods=['DELETE'])
def delete_qustion(q_id):
	i = 0;
	for question in question_list:
		if question["q_id"] == q_id:
			question_list.pop(i)
			response = Response("", 204)
			return response
		i += 1
	invalid_question = {
		"error": "Question with the id provided was not found"
	}
	response = Response(json.dumps(invalid_question), 400, mimetype='application/json')
	return response








app.run()
