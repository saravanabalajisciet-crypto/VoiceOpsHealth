from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------
# GLOBAL SESSION STATE
# -------------------------
STATE = {
    "stage": "complaint",   # complaint | followup
    "patient": {},
    "complaint": "",
    "questions": [],
    "answers": {},
    "index": 0,
    "lang": "ta"
}

# -------------------------
# CLINICAL QUESTION BANK
# -------------------------
CLINICAL_QUESTIONS = {
    "fever": [
        ("duration", {
            "ta": "எத்தனை நாளாக காய்ச்சல் உள்ளது?",
            "en": "How many days have you had fever?"
        }),
        ("temperature", {
            "ta": "உடல் வெப்பம் அதிகமாக உள்ளதா?",
            "en": "Is your body temperature high?"
        }),
        ("chills", {
            "ta": "குளிர் நடுக்கம் இருக்கிறதா?",
            "en": "Do you have chills?"
        }),
        ("body_pain", {
            "ta": "உடல் வலி உள்ளதா?",
            "en": "Do you have body pain?"
        })
    ],
    "headache": [
        ("duration", {
            "ta": "எத்தனை நாளாக தலைவலி இருக்கிறது?",
            "en": "How long have you had a headache?"
        }),
        ("location", {
            "ta": "வலி எங்கு உள்ளது?",
            "en": "Where is the pain located?"
        }),
        ("severity", {
            "ta": "வலி அதிகமாக உள்ளதா?",
            "en": "Is the pain severe?"
        })
    ]
}

# -------------------------
# MAIN PROCESS ENDPOINT
# -------------------------
@app.route("/process", methods=["POST"])
def process():
    global STATE

    text = request.form.get("text", "").lower()
    name = request.form.get("name", "")
    age = request.form.get("age", "")
    lang = request.form.get("lang", "ta")

    STATE["lang"] = lang

    # -------------------------
    # STEP 1: COMPLAINT DETECTION
    # -------------------------
    if STATE["stage"] == "complaint":
        STATE["patient"] = {
            "name": name,
            "age": age
        }

        if "காய்ச்சல்" in text or "fever" in text:
            STATE["complaint"] = "Fever"
            STATE["questions"] = CLINICAL_QUESTIONS["fever"]
        elif "தலை" in text or "headache" in text:
            STATE["complaint"] = "Headache"
            STATE["questions"] = CLINICAL_QUESTIONS["headache"]
        else:
            STATE["complaint"] = "General Health Issue"
            STATE["questions"] = []

        STATE["stage"] = "followup"
        STATE["index"] = 0
        STATE["answers"] = {}

        if STATE["questions"]:
            return jsonify({
                "type": "question",
                "question": STATE["questions"][0][1][lang]
            })

    # -------------------------
    # STEP 2: FOLLOW-UP QUESTIONS
    # -------------------------
    if STATE["stage"] == "followup" and STATE["questions"]:
        key, _ = STATE["questions"][STATE["index"]]
        STATE["answers"][key] = text

        STATE["index"] += 1

        if STATE["index"] < len(STATE["questions"]):
            return jsonify({
                "type": "question",
                "question": STATE["questions"][STATE["index"]][1][lang]
            })

    # -------------------------
    # STEP 3: FINAL REPORT
    # -------------------------
    report = {
        "patient": STATE["patient"],
        "complaint": STATE["complaint"],
        "details": STATE["answers"]
    }

    # RESET STATE (important for next patient)
    STATE = {
        "stage": "complaint",
        "patient": {},
        "complaint": "",
        "questions": [],
        "answers": {},
        "index": 0,
        "lang": "ta"
    }

    return jsonify({
        "type": "final",
        "report": report
    })


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
