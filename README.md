# Custom Email Generator

This is a personalized **AI-powered email assistant** that learns your writing style from your past Gmail messages and uses LLMs (like NVIDIA or Groq) to generate professional, personalized emails.

The system features a conversational UI built with Streamlit and a step-by-step prompt workflow that ensures your generated emails maintain your original tone and structure.

---

## Features

- Learns your **email style** from Gmail "Sent" messages
- Step-by-step email drafting: recipient → signature → purpose → extra context
- LLM-powered email generation with subject, body, and closing
- Built-in SMTP support for **sending emails**
- Clear, editable preview before sending
- Tooltips to assist with setup (e.g., App Password)

---

## Project Structure

```text
custom_email_generator/
├── app.py                        # Main Streamlit app
├── fetch_sent_emails.py         # Gmail IMAP fetcher
├── style_extractor.py           # Email style extractor
├── prompt_generator.py          # LLM prompt builder
├── nvidia_llm.py                # Email generation with NVIDIA LLM
├── smtp_sender.py               # SMTP email sending
├── data/
│   └── sent_emails.json         # Extracted emails from Gmail
├── requirements.txt
├── .gitignore
└── README.md
```

