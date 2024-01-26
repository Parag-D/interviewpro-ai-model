# prompt.py

question_generation_prompt = """
Given a candidate's resume, extract the following details:
- Skills: 
- Experience: 
- Projects: 

Generate between 5 and 12 'ADVANCED' interview questions tailored to the candidate's profile. Make sure to follow the suggestions given below strictly.
1. Include general questions like "Introduce yourself" along with questions that a human interviewer might ask. 
2. Questions from 2-5 should be based on the skills extracted, and the questions should be technical and conceptual, focusing on the core concepts, definitions and indepth unserstanding of the mentioned technologies. the complexity should be HARD and the questions should be from advanced topics. for example: skills: machine learning questions: What is Gradient Descent and learning rate? 
3. Questions 6-9 should be based on the projects, and 9-12 should be based on the professional experience.

Provide output in json format:
{
  "question": ["question1", "question2", ...]
}

"""



# question_generation_prompt = """

# Given a candidate's resume with the following details:
# - Skills: [List of skills]
# - Experience: [Job title]
# - Education: [Educational background]

# Generate between 5 and 12 interview questions tailored to the candidate's profile. Include general questions like "Introduce yourself" along with questions that a human interviewer might ask. Each question should prompt the candidate to provide detailed insights into their skills, experience, and education. Use natural language and make the questions open-ended to encourage detailed responses.

# Provide output in json format:
# {
# "question":["question1","question2",...]

# """


answer_validation = """
You are an expert interviewer and you have been provided with the interview data. Your task is to analyse the interview and provide suggestions, goods and bads from the interview.
"""

analysis_prompt = """
You are an expert interviewer and you have been provided with the interview data. Your task is to analyse the interview and provide suggestions to the candidate, goods and bads from the interview.
also rate the technical, interpersonal skills.
Don't generate random information in the response. 
If the answer is not provided or it is a giberish then return "You have not given the interview seriously. Please try again after preparing."
Make sure to provide the correct and accurate information for overall rating.

Make sure to follow the below given format:

provide response in json format.
feedback": {
    "strengths": {
     
    },
    "areas_for_improvement": {
      
    },
    "suggestions": {
      
    },
    "overall_rating": {
      "technical_skills":(out of 10) ,
      "interpersonal_skills": (out of 10) 
    }
  }
}

"""