import os
import json
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

# --- Load environment variables ---
load_dotenv()
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, and MODEL_NAME.")

# --- OpenAI Client Setup ---
client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# --- Models for structured outputs ---
class SkillGap(BaseModel):
    target_job: str
    missing_skills: List[str]
    explanation: str

class JobListing(BaseModel):
    title: str
    company: str
    location: str
    requirements: List[str]

class CourseRecommendation(BaseModel):
    skill: str
    courses: List[str]  # e.g., "Course Name (Platform) - link"

# --- Dummy Data ---
JOB_SKILLS = {
    "data scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas"],
    "web developer": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    "data analyst": ["Excel", "SQL", "Power BI", "Python", "Statistics"],
}

JOB_LISTINGS = [
    {"title": "Junior Data Scientist", "company": "TechCorp", "location": "Remote", "skills": ["Python", "SQL"]},
    {"title": "Web Developer", "company": "WebWorld", "location": "New York", "skills": ["JavaScript", "React"]},
    {"title": "Data Analyst", "company": "DataWorks", "location": "San Francisco", "skills": ["Excel", "SQL", "Python"]},
]

COURSES = {
    "SQL": ["SQL for Beginners (Coursera) - https://example.com/sql", "Learn SQL (Udemy) - https://example.com/sql2"],
    "Statistics": ["Intro to Statistics (Khan Academy) - https://example.com/stat"],
    "Pandas": ["Data Analysis with Pandas (YouTube) - https://example.com/pandas"],
    "Python": ["Python 101 (Codecademy) - https://example.com/py"],
    "React": ["React Crash Course (Ostad) - https://ostad.app/course/react-native-workshop"],
}

# --- Tools ---
@function_tool
def get_missing_skills(user_skills: List[str], target_job: str) -> dict:
    """
    Identify missing skills by comparing the user's current skills with 
    the required skills for a given target job.

    Args:
        user_skills (List[str]): The skills the user already has.
        target_job (str): The job title the user is aiming for.

    Returns:
        dict: A dictionary containing the target job, missing skills, and an explanation.
    """
    required_skills = JOB_SKILLS.get(target_job.lower())
    if not required_skills:
        return {"error": f"No data for job: {target_job}"}
    missing = [skill for skill in required_skills if skill not in user_skills]
    return {
        "target_job": target_job,
        "missing_skills": missing,
        "explanation": f"To become a {target_job}, you need to learn: {', '.join(missing)}"
    }


@function_tool
def find_jobs(user_skills: List[str], location: Optional[str] = None) -> List[dict]:
    """
    Find job listings that match the user's current skills.
    Optionally filter jobs by location.

    Args:
        user_skills (List[str]): A list of skills the user possesses.
        location (Optional[str]): (Optional) Preferred job location.

    Returns:
        List[dict]: A list of matching job dictionaries.
    """
    matches = []
    for job in JOB_LISTINGS:
        if all(skill in user_skills for skill in job["skills"]):
            if location and location.lower() not in job["location"].lower():
                continue
            matches.append(job)
    return matches


@function_tool
def recommend_courses(missing_skills: List[str]) -> List[dict]:
    """
    Recommend online courses to help the user learn missing skills.

    Args:
        missing_skills (List[str]): A list of skills the user needs to learn.

    Returns:
        List[dict]: A list of dictionaries, each containing a skill and recommended courses.
    """
    recommendations = []
    for skill in missing_skills:
        courses = COURSES.get(skill)
        if courses:
            recommendations.append({
                "skill": skill,
                "courses": courses
            })
    return recommendations


# --- Specialist Agents ---
skill_gap_agent = Agent(
    name="Skill Gap Specialist",
    handoff_description="Identifies skill gaps for a given career goal.",
    instructions="""
    You help users find out what skills they are missing for a specific job role.
    Use the get_missing_skills tool to compare the user's current skills with the job's required skills.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[get_missing_skills],
    output_type=SkillGap
)

job_finder_agent = Agent(
    name="Job Finder Specialist",
    handoff_description="Suggests job listings based on skills and location.",
    instructions="""
    You help users find job opportunities based on their current skills and optionally their preferred location.
    Use the find_jobs tool and return 2-3 good matches.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[find_jobs],
    output_type=List[JobListing]
)

course_recommender_agent = Agent(
    name="Course Recommender Specialist",
    handoff_description="Finds learning resources for missing skills.",
    instructions="""
    You help users find courses to learn specific skills.
    Use the recommend_courses tool and suggest a few courses for each missing skill.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    tools=[recommend_courses],
    output_type=List[CourseRecommendation]
)

# --- Main Controller Agent ---
conversation_agent = Agent(
    name="CareerMate",
    instructions="""
    You are the user's friendly career planning assistant.
    - Greet users and understand their career goals.
    - If the user mentions a job goal (e.g. 'I want to become a data analyst'), send to Skill Gap Specialist.
    - If the user asks about job opportunities, send to Job Finder Specialist.
    - If the user asks how to learn something or mentions skill gaps, send to Course Recommender Specialist.
    """,
    model=OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=client),
    handoffs=[skill_gap_agent, job_finder_agent, course_recommender_agent]
)

# --- Main Function ---
async def main():
    queries = [
        "I want to become a data scientist",
        "I know Python and SQL. Can you find me a job?",
        "How can I learn React and Pandas?",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")

        result = await Runner.run(conversation_agent, query)
        output = result.final_output

        print("\nFINAL RESPONSE:")

        # Skill Gap Analysis
        if isinstance(output, SkillGap):
            print("\n🔍 SKILL GAP ANALYSIS")
            print(f"Target Role: {output.target_job}")
            print(f"Missing Skills: {', '.join(output.missing_skills)}")
            print(f"Note: {output.explanation}")

        # Job Listings
        elif isinstance(output, list) and all(isinstance(job, JobListing) for job in output):
            print("\n💼 JOB LISTINGS")
            for i, job in enumerate(output, 1):
                print(f"{i}. {job.title} at {job.company} ({job.location})")
                print(f"   Required Skills: {', '.join(job.requirements)}")

        # Course Recommendations
        elif isinstance(output, list) and all(isinstance(c, CourseRecommendation) for c in output):
            print("\n📚 COURSE RECOMMENDATIONS")
            for rec in output:
                print(f"\nSkill: {rec.skill}")
                for i, course in enumerate(rec.courses, 1):
                    print(f"  {i}. {course}")

        else:
            print(output)


if __name__ == "__main__":
    asyncio.run(main())
