recruitment_ai_streamlit/
├── app.py                 # Main Streamlit app
├── agents/
│   ├── summarizer.py      # JD summarizer using Hugging Face
│   ├── parser.py          # CV parsing using PyMuPDF
│   ├── matcher.py         # Matching logic with sentence similarity
│   ├── shortlister.py     # Top-k selection logic
│   └── notifier.py        # Send emails using smtplib
├── data/
│   ├── jds/
│   └── cvs/
├── utils/
│   └── helpers.py         # Reusable functions
├── requirements.txt
└── README.md
