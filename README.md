 VoiceOps Health 

VoiceOps Health is a voice-based patient intake system built to simplify how hospitals collect patient complaints.

Instead of filling long forms, patients can speak naturally in Tamil or English. The system listens, asks relevant follow-up questions, and prepares a structured intake report before the doctor sees the patient.

 What It Does
- Captures patient complaints using voice
- Asks complaint-specific follow-up questions
- Supports Tamil and English input
- Generates a clean, structured medical intake report
- Provides a simple, hospital-ready user interface


 ☁️ Azure Integration (Planned Architecture)
This MVP is designed to be fully compatible with Microsoft Azure services.
In a production setup:
- Azure Speech-to-Text will handle multilingual voice input
- Azure OpenAI will classify complaints and guide adaptive questioning
- Azure App Service will host the backend securely
- Azure Blob Storage will store audio and intake reports
This allows the system to scale without changing the core workflow.

 🧠 Why a Rule-Based MVP?
Healthcare systems require safety, clarity, and predictability.
For this MVP, we intentionally used a rule-based approach to clearly demonstrate the intake workflow and ensure deterministic behavior. Once validated, AI can be introduced as an enhancement rather than a replacement.



 🛠️ Tech Stack
- Frontend: HTML, CSS, JavaScript  
- Backend: Python (Flask)  
- Voice Input:** Browser Speech API (MVP)  
- AI (Planned):Azure OpenAI  
  Demo Video: https://www.loom.com/share/1aad5d7b2c4a49fd93a8d8f7a73de117
