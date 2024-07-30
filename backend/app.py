from flask import Flask, jsonify, request
from dotenv import load_dotenv
from ai71 import AI71 
import os

load_dotenv()

app = Flask(__name__)
falcon_ai_client = AI71(os.getenv("FALCON_API_KEY"))

# Endpoints
#   1. Generate Exam Paper API
        # - POST API
        # - Request: Subject, Question Format, Content (PYP / Exercises)
        # - Response: New, Generated Exam Paper
#   2. Test AI Prompt API
        # - POST API
        # - Follow AI71 Docs

@app.route('/api/paper', methods=['POST'])
def generate_exam_paper():
    pass

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
            ],
        ).choices[0].message.content

        return jsonify({'response': llm_response}), 200
    else:
        return jsonify({'error': 'Request data should be JSON!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
