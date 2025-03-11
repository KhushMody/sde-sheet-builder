import os
import json
import logging
import pandas as pd
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from flask_cors import CORS
from groq import Groq
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import chardet


logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to debug
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@database:5432/interview_prep")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    question = db.Column(db.Text, nullable=False)
    acceptance = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    question_link = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

def read_file_to_string(file_path):
    try:
        # Use raw string or forward slashes for compatibility
        file_path = os.path.join(os.getcwd(), file_path)
        
        with open(file_path, 'rb') as file:
            raw_data = file.read()
            encoding = chardet.detect(raw_data)['encoding']
            logger.info(f"encoding = {encoding}")
        
        with open(file_path, 'r', encoding=encoding) as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        logger.info(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None

def get_data(company_name):
    if company_name:
        # Use a raw SQL query to fetch all questions for the given company
        sql_query = text(f"SELECT * FROM question WHERE company = :company_name")
        
        # Execute the query with a parameter to prevent SQL injection
        result = db.session.execute(sql_query, {'company_name': company_name})

        # Fetch all rows and convert them to a list of dictionaries
        rows = result.mappings().all()

        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(rows)
        logger.info(f"DataFrame created with {len(df)} rows")

    else:
        df = pd.DataFrame()
    
    return df

def call_llm(sys_msg, user_msg):
    
    client = Groq(api_key=GROQ_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":"system",
                "content": sys_msg
            },
            {
                "role": "user",
                "content": user_msg
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
    )

    return chat_completion.choices[0].message.content

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    user_question = data.get("question", "")

    if not user_question:
        return jsonify({"error": "User question is required"}), 400

    system_message = read_file_to_string("./prompts/QuestionSolver.txt")
    usr_msg = f"Users's Question: \n{user_question}"

    question_details = call_llm(system_message, usr_msg)
    company_name, difficulty, question_type, length = None, None, None, None
    try:
        question_details = json.loads(question_details)
        company_name = question_details["company_name"].lower()
        difficulty = question_details["difficulty"]
        question_type = question_details["question_type"]
        length = int(question_details["length"])
    except json.JSONDecodeError as e:
        logger.error("Failed to decode JSON: %s", e)
    except KeyError as e:
        logger.warning("Missing key in question details: %s", e)

    logger.info("Company: %s, Difficulty: %s, Type: %s, Length: %d", company_name, difficulty, question_type, length)

    company_list = read_file_to_string("./companies.txt")
    company_set = set([company.strip().lower() for company in company_list.split('\n') if company.strip()])

    if company_name not in company_set:
        company_name = None
    
    data = get_data(company_name)

    questions = data['question'].astype(str).tolist()
    usr_msg = f"""
        questions: {questions}\n
        topic: {question_type}\n
    """
    system_message = read_file_to_string("./prompts/QuestionPicker.txt")

    selected_questions_str = call_llm(system_message, usr_msg)
    selected_questions_list = None

    try:
        selected_questions = json.loads(selected_questions_str)
        selected_questions_list = selected_questions['questions']
    except json.JSONDecodeError as e:
        logger.error("Failed to decode JSON: %s", e)
    except KeyError as e:
        logger.warning("Missing key in selected_questions: %s", e)

    indexed_data = data.set_index('question')
    existing_questions = [q for q in selected_questions_list if q in indexed_data.index]
    result = indexed_data.loc[existing_questions]
    result = result[result['difficulty'] == difficulty]
    result = result.head(length)
    logger.info(f"the needed dataframe:\n {result}")
    result = result.reset_index()  # This puts 'question' back as a column and creates a numeric index
    result_json = result.to_dict(orient='records')


    # Placeholder for actual code analysis
    response = {
        "data": result_json,
        "question": user_question
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)