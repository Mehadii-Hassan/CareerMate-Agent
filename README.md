# 🧠 CareerMate – Multi-Agent Career Advisor

CareerMate is a multi-agent AI assistant built using the OpenAI SDK and Pydantic models. It helps users explore and plan their career by answering three types of questions:

- 🔍 **Skill Gap Analysis** – What skills are needed for a job role?
- 💼 **Job Matching** – Which jobs match my skills?
- 📚 **Course Recommendation** – How can I learn missing skills?

## 🚀 Features
- Structured outputs using Pydantic models
- Modular agent system for Skill Gap, Job Finder, and Course Recommender
- Sample query runner using asyncio
- Tool-augmented reasoning with OpenAI function calling

## 🛠️ Tech Stack
- Python 3.8+
- OpenAI SDK (Async)
- Pydantic
- dotenv
- Custom Agent Framework (from `agents.py`)

## 📁 Project Structure
├── .env # Your OpenAI credentials
├── requirements.txt # what you needed
├── careermate.py # Careermate agent code
├── README.md # Project documentation

## Install dependencies
pip install -r requirements.txt

## Set up environment variables
BASE_URL= "https://models.github.ai/inference/v1"
API_KEY= "your_api_key_here"
MODEL_NAME= "openai/gpt-4.1-nano"

## Run the app
run careermate.py

##🧩 Available Agents
🎯 Skill Gap Specialist
Identifies missing skills for a target job role.
get_missing_skills(user_skills, target_job)

🔍 Job Finder Specialist
Matches user skills to available job listings.
find_jobs(user_skills, location=None)

📚 Course Recommender Specialist
Suggests courses to learn missing skills.
recommend_courses(missing_skills)

##💡 Example Queries
"I want to become a data scientist"
"I know Python and SQL. Can you find me a job?"
"How can I learn React and Pandas?"

