# Amdocs GenAI Graduate Hackathon 2024 - 2025  
## Misinformation Detection and Fact-Checking on Social Media  

### **Problem Statement**  
Develop AI-driven solutions to effectively detect misinformation and enhance fact-checking capabilities in online content.  

### **Challenge**  
Design algorithms that can autonomously identify and verify the accuracy of information across various digital platforms. Propose innovative approaches to distinguish credible sources from unreliable ones, ensuring accurate dissemination of information to users.  

### **Objectives**  
- Create AI models capable of detecting and flagging misinformation in real-time.  
- Develop tools to cross-reference information with credible sources and verify its authenticity.  
- Implement scalable solutions that can adapt to evolving patterns of misinformation and disinformation campaigns.  
- Enhance transparency by providing users with clear indicators of content reliability and trustworthiness.  

### **Expected Outcomes**  
- Robust AI algorithms that significantly reduce the spread of false information online.  
- Tools for fact-checking and verifying information sources efficiently and accurately.  
- Improved user trust and confidence in the information they consume on digital platforms.  

---

## **Demo Video**  
[Watch the Demo](https://youtu.be/dAyzBoMMBO8)  

---

## **Steps to Run the Code**  

### **1. Clone the GitHub Repository**  
```bash
git clone <repo-url>
cd <repo-folder>
```

### **2. Create a New Python Environment**  
```bash
python -m venv env
```

### **3. Activate the Virtual Environment**  
#### **Windows:**  
```bash
env\Scripts\activate
```
#### **Mac/Linux:**  
```bash
source env/bin/activate
```

### **4. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **5. Set Up Backend**  
- Copy all backend files into the `env` folder.  
- Edit the `.env` file and add your API keys.  

### **6. Run the FastAPI Server**  
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### **7. Set Up Frontend**  
Navigate to the frontend folder and run:  
```bash
npm install
npm start
```

---


