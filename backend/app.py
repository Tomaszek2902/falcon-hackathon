import re
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from ai71 import AI71 
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
from pypdf import PdfReader 
from time import *
from pdf2image import convert_from_path
from PIL import Image
from flask_cors import CORS

import os
import json
import shutil
import pytesseract

load_dotenv()

app = Flask(__name__)
CORS(app)

current_path = os.path.abspath(os.getcwd())
falcon_ai_client = AI71(os.getenv("FALCON_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = os.path.join(current_path, "tesseract", "tesseract.exe")

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
            return jsonify({'status': False}), 400
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

@app.route('/api/uploadContent', methods=['POST'])
def upload_content():
    process_id = dict(request.form)["process_id"]
    contents = request.files.getlist("content")
    
    try:
        for file in contents:
            name = secure_filename(file.filename)
            if not os.path.exists(os.path.join(current_path, "db", process_id, "contents")):
                os.makedirs(os.path.join(current_path, "db", process_id, "contents"))
            file.save(os.path.join(current_path, "db", process_id, "contents", name))
        return jsonify({'status': True, "process_id": process_id}), 200
    except Exception as e:
        print(e)
        return jsonify({'status': False}), 400

@app.route('/api/generate', methods=['POST'])
def generate():
    if request.is_json:
        data = request.get_json()
        process_id = data['process_id']
        metadata = {}   # subject, difficulty, formatQ, numQ
        
        db_path = os.path.join(current_path, "db", process_id)
        if not os.path.exists(db_path):
            return jsonify({'error': 'Data does not exist!'}), 400 
        
        # Read metadata
        with open(os.path.join(db_path, "metadata.txt"), "r") as m_file:
            metadata = json.loads(m_file.read())

        # Create training data
        db_contents_path = os.path.join(db_path, "contents")
        if not os.path.exists(db_contents_path):
            return jsonify({'error': 'No contents uploaded for this process!'}), 400 

        with open(os.path.join(db_path, "training_data.txt"), "a+") as t_file:
            contents_name_list = os.listdir(db_contents_path)
            for content_name in contents_name_list:
                t_file.write(f"[{content_name}]\n")
                filepath = os.path.join(db_contents_path, content_name)
                doc = convert_from_path(filepath, poppler_path=os.path.join(current_path, "poppler\poppler-24.07.0\Library\\bin"))

                raw_txt_data = ""
                for no, data in enumerate(doc):                
                    raw_txt_data += re.sub("\\\\n|www.sgexam.com", "", str(pytesseract.image_to_string(data).encode("utf-8")))

                qa_list = re.split(r'END OF PAPER', raw_txt_data)

                for i in range(0, len(qa_list) - 1):
                    questions = filter(lambda x: re.match('^\d+\.', x), re.split(r'(?=\d+\.)', qa_list[i]))
                    answers = filter(lambda x: re.match('^Q\d{1,2}', x), re.split(r'(?=Q\d{1,2})', qa_list[len(qa_list) - 1]))
                    t_file.write("\n\nQuestions: \n\n")
                    t_file.write("\n\n".join(questions))
                    t_file.write("\n\n")
                    t_file.write("Answers: \n\n")
                    t_file.write("\n\n".join(answers))
                t_file.write("========================\n")
            return jsonify({'status': True}), 200
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

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
