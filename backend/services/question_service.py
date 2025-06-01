import json
import logging
import pandas as pd
from ..utils.file_helper import read_file_to_string
from ..utils.logger import setup_logging
from .llm_service import call_llm
from .db_service import get_data
from flask import jsonify, make_response

setup_logging()
logger = logging.getLogger(__name__)

def analyze_question(user_question):
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
    
    logger.info(f'company_name = {company_name}')
    data = get_data(company_name, difficulty)

    questions = data['question'].astype(str).tolist()
    usr_msg = f"""
        questions: {questions}\n
        topic: {question_type}\n
        number: {str(length)}\n
    """
    system_message = read_file_to_string("./prompts/QuestionPicker.txt")

    selected_questions_str = call_llm(system_message, usr_msg)
    logger.info(f"selected_questions response: {selected_questions_str}")
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
    # result = result[result['difficulty'] == difficulty]
    result = result.drop_duplicates()
    logger.info(f"the needed dataframe:\n {result}")
    result = result.reset_index()  # This puts 'question' back as a column and creates a numeric index
    result_json = result.to_dict(orient='records')


    # Placeholder for actual code analysis
    response = {
        "data": result_json,
        "question": user_question
    }
    
    return make_response(jsonify(response), 200)
