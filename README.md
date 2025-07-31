<h1 align="center">🎯 CareerMate Agent</h1>

<p align="center">
  <strong>Identify skill gaps, find job opportunities, and get course recommendations with AI Agents.</strong><br>
  Powered by OpenAI, Pydantic, and Python Async tools.
</p>

<hr>

<h2>🧠 Overview</h2>

<p>
CareerMate is an intelligent career-planning assistant built using a multi-agent architecture. It helps users explore their target jobs, analyze missing skills, find matching job listings, and recommends online courses — all based on user input.
</p>

<ul>
  <li>🔍 <strong>Skill Gap Specialist</strong>: Finds missing skills for a given job</li>
  <li>💼 <strong>Job Finder Specialist</strong>: Suggests jobs based on current skills and location</li>
  <li>📚 <strong>Course Recommender Specialist</strong>: Recommends courses to fill skill gaps</li>
</ul>

<hr>

<h2>🚀 Features</h2>

<ul>
  <li>Goal-oriented conversation routing using OpenAI Agents</li>
  <li>Skill gap analysis using dummy job-skill mappings</li>
  <li>Job listing filtering by skills and location</li>
  <li>Curated course recommendations for missing skills</li>
  <li>Fully async Python architecture</li>
</ul>

<hr>

<h2>📁 Project Structure</h2>

<pre>
careermate/
│
├── agents/                       ← Agent logic and definitions
├── .env                          ← Environment variables for OpenAI
├── careermate.py                 ← Main script
├── requirements.txt              ← Python dependencies
└── README.md
</pre>

<hr>

<h2>⚙️ Installation</h2>

<ol>
  <li>Clone the repository</li>
  <pre><code>git clone https://github.com/your-username/CareerMate.git</code></pre>

  <li>Install the required dependencies</li>
  <pre><code>pip install -r requirements.txt</code></pre>

  <li>Create a <code>.env</code> file in the root folder with the following:</li>
  <pre><code>
BASE_URL= "https://models.github.ai/inference/v1"
API_KEY= "your-openai-api-key-here"
MODEL_NAME= "openai/gpt-4.1-nano"
  </code></pre>

  <li>Run the script</li>
  <pre><code>python careermate.py</code></pre>
</ol>

<hr>

<h2>🧪 Example Queries</h2>

<ul>
  <li><code>I want to become a data scientist</code></li>
  <li><code>I know Python and SQL. Can you find me a job?</code></li>
  <li><code>How can I learn React and Pandas?</code></li>
</ul>

<hr>

<h2>🔗 Sample Data Used</h2>

<ul>
  <li><strong>Jobs</strong>: Data Scientist, Web Developer, Data Analyst</li>
  <li><strong>Skills</strong>: Python, SQL, React, Pandas, JavaScript, etc.</li>
  <li><strong>Courses</strong>: Coursera, Udemy, YouTube, Ostad</li>
</ul>

<hr>

<h2>🙌 Credits</h2>

<p>
Developed by <strong>Mehadi Hassan</strong> as part of a smart agent exploration project using OpenAI's Async API with Pydantic models and multi-agent routing.
</p>

<hr>

<p align="center">⭐ Star this repo if you like it and want to support!</p>
