from flask import Flask, jsonify, request
from dotenv import load_dotenv
from ai71 import AI71 
import os
from time import *
import json
from werkzeug.datastructures import ImmutableMultiDict
import shutil

load_dotenv()

app = Flask(__name__)
current_path = os.path.abspath(os.getcwd())
falcon_ai_client = AI71(os.getenv("FALCON_API_KEY"))

# Endpoints
#   1.  Set Paper API
        # - POST API
        # - Request: Subject, Difficulty, Question Format, No. of Questions
        # - Response: boolean to indicate status (id for db file directory)
#   2. Upload Content API
        # - POST API
        # - Request: Content (PYP / Exercises), id for db file directory
        # - Response: boolean to indicate status
#   3. Generate Exam Paper API
        # - POST API
        # - Request: id for db file directory
        # - Response: response paper
#   4. Quit Paper API
        # - POST API
        # - Request: id for db file directory
        # - Response: boolean to indicate status
#   5. Test AI Prompt API
        # - POST API
        # - Follow AI71 Docs

@app.route('/api/setPaper', methods=['POST'])
def set_paper():
    if request.is_json:
        data = request.get_json()
        subject = data['subject']
        difficulty = data['difficulty']
        formatQ = data['formatQ']
        numQ = data['numQ']
        
        try:        
            process_id = str(time_ns())
            new_file_path = os.path.join(current_path, "db", process_id)
            os.makedirs(new_file_path)
            
            with open(os.path.join(new_file_path, "metadata.txt"), "w") as file:
                filedata = json.dumps(
                    {
                        "subject": subject,
                        "difficulty": difficulty,
                        "formatQ": formatQ,
                        "numQ": numQ
                    }
                )
                file.write(filedata)
            return jsonify({'status': True, "process_id": process_id}), 200
        except Exception as e:
            print(e)
            return jsonify({'status': False}), 400
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

@app.route('/api/uploadContent', methods=['POST'])
def upload_content():
    process_id = dict(request.form)["process_id"]
    content = request.files["content"]
    # TODO
    pass

@app.route('/api/generate', methods=['POST'])
def generate():
    # TODO
    pass

@app.route('/api/quitGenerate', methods=['POST'])    
def quit_generate():
    if request.is_json:
        data = request.get_json()
        process_id = data["process_id"]
        
        try:
            shutil.rmtree(os.path.join(current_path, "db", process_id))
            return jsonify({'status': True}), 200
        except:
            return jsonify({'status': False}), 200
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

@app.route('/api/prompt', methods=['POST'])
def prompt_llm():
    if request.is_json:
        data = request.get_json()
        prompt = data['prompt']
        context = data['context']

        llm_response = falcon_ai_client.chat.completions.create(
            model="tiiuae/falcon-180B-chat",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
            ]
        ).choices[0].message.content

        return jsonify({'response': llm_response}), 200
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
