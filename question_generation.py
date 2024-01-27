# question_generation.py

import sys
import os
from openai import OpenAI
from prompt import question_generation_prompt
from exception import CustomException
from dotenv import load_dotenv, find_dotenv
import re
import json

# Load environment variables
load_dotenv(find_dotenv())

# Set up OpenAI API key and AWS credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def clean_question(question):
    # Add your cleaning logic here
    cleaned_question = re.sub(r'[^a-zA-Z0-9\s]', '', question)
    return cleaned_question

# Global variable to store generated questions
global_questions = []


def generate_question_and_audio_async(resume):
    try:
        print("Inside generating questions")
        chat_response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": question_generation_prompt + str(resume)},
            ]
        )
        print(chat_response.choices[0].message.content)

        # Extract the generated questions from the API response
        questions = chat_response.choices[0].message.content
        print("Questions are: ",questions)

        questions_dict = json.loads(questions)
        print("Keys in Question_dict:", questions_dict.keys())

        # Access the list of questions
        question_list = questions_dict.get("question", []) or questions_dict.get("questions", [])
        print("Question_list is", question_list)


        # Cleaning questions
        cleaned_questions = [clean_question(question) for question in question_list]

        global_questions = cleaned_questions

        print("Global Questions are: ", global_questions)
        return cleaned_questions, question_list
    
    except Exception as e:
        raise CustomException("Error generating questions and audio", error_detail=e)

# if __name__ == '__main__':
#     generate_question_and_audio_async("""PROFILE
# Results-driven professional with expertise in Natural Language
# Processing (NLP) and machine learning, proficient in utilizing
# a range of technologies and tools, including Hugging Face
# '
# s
# open-source models, advanced techniques such as Retrieval
# Augmented Generation (RAG), and specific tools like Wisper
# AI by OpenAI. Proven track record of successfully
# implementing and leading projects centered around Large
# Language Models (LLM). Skilled in data cleaning and
# preprocessing, with a focus on automating educational
# assessment processes and enhancing student support systems.
# PROFESSIONAL EXPERIENCE
# Data Scientist
# iNeuron Intelligence Pvt. Ltd.
# 2023/09 – present | Bengaluru, India
# • Developed an implemented an LLM model using Hugging-
# Face and Retrieval Augmented Generation(RAG) for
# automated assignment and quiz generation.
# • Streamlined grading processes through an automated
# evaluation system, enhancing efficiency and accuracy.
# • Led a team in utilizing Hugging Face
# '
# s open-source models
# and Retrieval Augmented Generation (RAG) to extract
# transcripts from 23,000 videos.
# • Curated a knowledge base of FAQs from video transcripts,
# contributing to student query resolution systems.
# • Applied NLP techniques to analyze and extract insights from
# chat support data, enhancing the adaptability of LLM models.
# Associate Tech Engineer
# iNeuron Intelligence Pvt. Ltd.
# 2023/01 – 2023/09 | Bengaluru
# • Managed email and live chat support channels, optimizing
# response time and resolution efficiency.
# • Analyzed user inquiries using data analytics, contributing to
# targeted improvements in the support system.
# • Developed a comprehensive knowledge base by categorizing
# and documenting frequently asked questions, laying the
# groundwork for subsequent projects.
# • Collaborated with cross-functional teams to communicate
# user feedback and ensure user-centric improvements in
# support processes.
# • Delivered high-quality support, fostering positive customer
# relationships and contributing to ongoing process
# enhancements.
# Intern
# iNeuron Intelligence Pvt. Ltd.
# 2022/10 – 2023/01 | Bengaluru
# • Worked on an insurance price prediction project using
# machine learning algorithms.
# • Utilized end-to-end approach, from data preprocessing to
# model deployment on AWS.
# • Developed and fine-tuned ML models to accurately estimate
# insurance prices.
# PROJECTS
# Automated Educational Assessment System
# • Developed and implemented an LLM model using Hugging
# Face and Retrieval Augmented Generation (RAG) for
# automated assignment and quiz generation.
# • Streamlined grading processes through an automated
# evaluation system, enhancing efficiency.
# Knowledge Ocean from Video Transcripts
# • Led a team in utilizing Hugging Face
# '
# s open-source models
# and Retrieval Augmented Generation (RAG) to extract
# transcripts from 23,000 videos.
# • Curated a knowledge base of FAQs from video transcripts,
# contributing to student query resolution systems.
# • Contributed to the fine-tuning of the LLM model through
# the generated knowledge base, enhancing its adaptability to
# student queries.
# AI-Powered Mock Interview Platform
# • Developed a realistic mock interview platform using cutting-
# edge NLP and ML technologies to simulate diverse and
# lifelike interview scenarios.
# • Implemented a real-time feedback system, offering users
# personalized insights into their communication skills,
# content quality, and overall interview performance.
# • Designed a user-friendly interface allowing individuals to
# customize interview parameters, including industry-specific
# questions, interview duration, and difficulty levels.
# • Demonstrated project efficacy in enhancing interview
# readiness, boosting user confidence, and improving success
# rates in actual job interviews.
# SKILLS
# Programming Languages (Python)
# Data Manipulation and Analysis (Numpy, Pandas)
# Data Visualization (Matplotlib, Seaborn)
# Machine Learning (scikit-learn, TensorFlow, PyTorch)
# Deep Learning (ANN, CNN, RNN)
# GPT-3/ChatGPT (Foundational Models (e.g., GPT-
# 3/ChatGPT), Prompt Creation and Validation)
# Large Language Models (LLM), Natural Language
# Processing (NLP) Techniques
# Transformer Architectures (BERT, GPT)
# Databases (MySQL, MongoDB)
# Web Scraping (BeautifulSoup, Scrapy, Selenium) PowerBI
# EDUCATION
# MBA (Business Analytics)
# Sinhgad Institute of Management (SPPU)
# 2019/08 – 2021/08 | Pune
# B.E. (Computer Engineering)
# Genba Sopanrao Moze College of Engineering (SPPU)
# 2014/08 – 2019/07 | Pune
# Parag Darade Data Scientist
# paragdarade234@gmail.com 9970118144 Bengaluru, Karnataka, India
# https://www.linkedin.com/in/parag-darade https://github.com/ParagDD""")

# import asyncio
# async def main():
#     print("Before calling async function")

#     # Calling the asynchronous function using await
#     await generate_question_and_audio_async(resume="Parag Darade  Data Scientist paragdarade234@gmail.com 9970118144 Bengaluru, Karnataka, India https://www.linkedin.com/in/parag-darade https://github.com/ParagDD PROFILE Results-driven professional with expertise in Natural Language Processing (NLP) and machine learning, proficient in utilizing a range of technologies and tools, including Hugging Face's open-source models, advanced techniques such as Retrieval Augmented Generation (RAG), and specific tools like Wisper AI by OpenAI. Proven track record of successfully implementing and leading projects centered around Large Language Models (LLM). Skilled in data cleaning and preprocessing, with a focus on automating educational assessment processes and enhancing student support systems. PROJECTS Automated Educational Assessment System evolutionizing Student Evaluation through LLM Automation •Developed and implemented an LLM model using Hugging Face and Retrieval Augmented Generation (RAG) for automated assignment and quiz generation. •Streamlined grading processes through an automated evaluation system, enhancing efficiency. Knowledge Ocean from Video Transcripts Unleashing a Sea of Knowledge from 23,000 Videos •Led a team in utilizing Hugging Face's open-source models and Retrieval Augmented Generation (RAG) to extract transcripts from 23,000 videos. •Curated a knowledge base of FAQs from video transcripts, contributing to student query resolution systems. •Contributed to the fine-tuning of the LLM model through the generated knowledge base, enhancing its adaptability to student queries. Chat Data Analysis for Enhanced Support Elevating Support Systems through NLP-Driven Insights •Extracted insights from chat support data using Hugging Face models, including Retrieval Augmented Generation (RAG). •Integrated cleaned data into projects, enhancing the adaptability of LLM models. SKILLS Programming Languages (Python) Data Manipulation and Analysis (Numpy, Pandas) Data Visualization (Matplotlib, Seaborn) Machine Learning (scikit-learn, TensorFlow, PyTorch) Deep Learning (ANN, CNN, RNN) GPT-3/ChatGPT (Foundational Models (e.g., GPT-3/ChatGPT), Prompt Creation and Validation) Large Language Models (LLM), Natural Language Processing (NLP) Techniques Transformer Architectures (BERT, GPT) Databases (MySQL, MongoDB) Web Scraping (BeautifulSoup, Scrapy, Selenium) PowerBI PROFESSIONAL EXPERIENCE Data Scientist iNeuron Intelligence Pvt. Ltd. 2023/09 – present | Bengaluru, India •Developed an implemented an LLM model using Hugging-Face and Retrieval Augmented Generation(RAG) for automated assignment and quiz generation. •Streamlined grading processes through an automated evaluation system, enhancing efficiency and accuracy. •Led a team in utilizing Hugging Face's open-source models and Retrieval Augmented Generation (RAG) to extract transcripts from 23,000 videos. •Curated a knowledge base of FAQs from video transcripts, contributing to student query resolution systems. •Applied NLP techniques to analyze and extract insights from chat support data, enhancing the adaptability of LLM models. Associate Tech Engineer iNeuron Intelligence Pvt. Ltd. 2023/01 – 2023/09 | Bengaluru •Managed email and live chat support channels, optimizing response time and resolution efficiency. •Analyzed user inquiries using data analytics, contributing to targeted improvements in the support system. •Developed a comprehensive knowledge base by categorizing and documenting frequently asked questions, laying the groundwork for subsequent projects. •Collaborated with cross-functional teams to communicate user feedback and ensure user-centric improvements in support processes. •Delivered high-quality support, fostering positive customer relationships and contributing to ongoing process enhancements. Intern iNeuron Intelligence Pvt. Ltd. 2022/10 – 2023/01 | Bengaluru •Worked on an insurance price prediction project using machine learning algorithms. •Utilized end-to-end approach, from data preprocessing to model deployment on AWS. •Developed and fine-tuned ML models to accurately estimate insurance prices. EDUCATION MBA (Business Analytics) Sinhgad Institute of Management (SPPU) 2019/08 – 2021/08 | Pune B.E. (Computer Engineering) Genba Sopanrao Moze College of Engineering (SPPU) 2014/08 – 2019/07 | Pune COURSES Full Stack Data Science Bootcamp iNeuron")

#     print("After calling async function")

# # Run the asynchronous event loop
# asyncio.run(main())