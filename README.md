# Amdocs GenAI Graduate Hackathon 2024 - 2025 
# Misinformation Detection and Fact-Checking on Social Media
Problem Statement: Develop AI-driven solutions to effectively detect misinformation and enhance fact-checking capabilities in online content.

Challenge: Design algorithms that can autonomously identify and verify the accuracy of information across various digital platforms. Propose innovative approaches to distinguish credible sources from unreliable ones, ensuring accurate dissemination of information to users.

Objectives:

Create AI models capable of detecting and flagging misinformation in real-time.
Develop tools to cross-reference information with credible sources and verify its authenticity.
Implement scalable solutions that can adapt to evolving patterns of misinformation and disinformation campaigns.
Enhance transparency by providing users with clear indicators of content reliability and trustworthiness.
Expected Outcomes:

Robust AI algorithms that significantly reduce the spread of false information online.
Tools for fact-checking and verifying information sources efficiently and accurately.
Improved user trust and confidence in the information they consume on digital platforms.

Here is the demo video link: https://drive.google.com/drive/folders/1JhW3rSaQIj5yboHy1kUDyQo1krXnG4Yq?usp=sharing
This is our submission code for the above problem statement.
Steps to run the code:
1. First clone the github repo
2. Now create a new python environment:
python -m venv env
cd env
pip install -r requirements.txt
3. Now copy all the backend files in the env folder and edit the .env file with your API Keys.
4. Now run the python file(FastAPI server):
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
5. Once the python backend is running, go to frontend and run the following command:
npm install
npm start


