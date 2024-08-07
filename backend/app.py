import re
from flask_cors import CORS
from flask import Flask, jsonify, request, send_file
from dotenv import load_dotenv
from ai71 import AI71 
from werkzeug.utils import secure_filename
from time import *
from pdf2image import convert_from_path
from flask_cors import CORS

import os
import json
import shutil
import pytesseract
import string
import textwrap
from fpdf import FPDF

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
                doc = convert_from_path(filepath)

                raw_txt_data = ""
                for _, data in enumerate(doc):                
                    raw_txt_data += re.sub("\\\\n|www.sgexam.com", "", str(pytesseract.image_to_string(data).encode("ascii", "ignore")))
                filtered_txt_data = ''.join(filter(lambda x: x in set(string.printable), raw_txt_data))
                t_file.write(filtered_txt_data)

                # qa_list = re.split(r'END OF PAPER', raw_txt_data)
                # for i in range(0, len(qa_list) - 1):
                #     questions = filter(lambda x: re.match('^\d+\.', x), re.split(r'(?=\d+\.)', qa_list[i]))
                #     answers = filter(lambda x: re.match('^Q\d{1,2}', x), re.split(r'(?=Q\d{1,2})', qa_list[len(qa_list) - 1]))
                #     t_file.write("\n\nQuestions: \n\n")
                #     t_file.write("\n\n".join(questions))
                #     t_file.write("\n\n")
                #     t_file.write("Answers: \n\n")
                #     t_file.write("\n\n".join(answers))
                
                context = f"""You are a high school teacher tasked with creating new educational content based on existing material. Your goal is to generate new questions and answers that align with the style, subject, and difficulty level of the provided examples.

                                First, carefully examine the following sample questions and answers:

                                1. Question: 'What is the Pythagorean theorem?'
                                Answer: 'The Pythagorean theorem states that in a right-angled triangle, the square of the hypotenuse is equal to the sum of the squares of the other two sides.'

                                2. Question: 'How do you find the area of a triangle?'
                                Answer: 'The area of a triangle is calculated by multiplying the base by the height and dividing by 2.'

                                Now, follow these steps to create new content:

                                1. Identify the Subject and Scope: 
                                Analyze the sample questions to determine the subject (in this case, mathematics) and the specific topics covered (geometry, basic formulas).

                                2. Generate New Questions: 
                                Create a new set of {metadata['numQ']} questions that fit within the same subject and scope. Ensure the questions are unique but maintain the same style and complexity as the samples. The questions should be of {metadata['difficulty']} difficulty and include {metadata['formatQ']} question types.

                                3. Provide Answers: 
                                For each new question, provide a clear and concise answer that matches the level of detail in the sample answers.

                                4. Format the Output: 
                                Present your new questions and answers in the exact JSON structure provided below. Do not deviate from this format:

                                {{
                                "questions": [
                                    {{
                                    "question": "Your new question here",
                                    "answer": "Your new answer here"
                                    }},
                                    {{
                                    "question": "Your second new question here",
                                    "answer": "Your second new answer here"
                                    }}
                                ]
                                }}

                                Important Notes:
                                - Ensure that your new questions and answers are different from the samples but related to the same subject.
                                - Maintain the {metadata['difficulty']} difficulty level as specified.
                                - Include {metadata['formatQ']} question types as requested.
                                - Generate exactly {metadata['numQ']} questions.
                                - Double-check that your output strictly follows the provided JSON structure.
                                - Do not include any additional text or explanations outside of the JSON structure.

                                Please proceed with generating new questions and answers based on these instructions."""
                
                llm_response = falcon_ai_client.chat.completions.create(
                    model="tiiuae/falcon-180B-chat",
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": filtered_txt_data},
                    ]   
                ).choices[0].message.content
                print(llm_response)

                generated_qa_data = clean_and_convert_to_dict(llm_response)
                qa_text_data = ""
                i = 1
                for qa in generated_qa_data['questions']:
                    qa_text_data += f"{i}. {qa['question']}\n"
                    qa_text_data += f"Answer: {qa['answer']}\n\n\n"
                    i += 1
                text_to_pdf(qa_text_data, os.path.join(db_path, "generated_paper.pdf"))
                return send_file(os.path.join(db_path, "generated_paper.pdf"), as_attachment=True)
                # return jsonify({'response': llm_response, 'status': 'success'}), 200

        return jsonify({'error': 'An error occured!'}), 400
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

def clean_and_convert_to_dict(input_string):
    # Convert to a dictionary
    # result_dict = json.loads(input_string)
    # return result_dict

    result_dict = {}
    while True:
        try:
            result_dict = json.loads(input_string)
            break
        except Exception:
            input_string = input_string[:-1]
            if input_string[-1] == "}":
                input_string += "]}"
            continue
    return result_dict

def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')

if __name__ == '__main__':
    app.run(debug=True)
