recruitment_ai_project/
├── backend/
│   ├── main.py                        # FastAPI entry point
│   ├── routes/
│   │   └── endpoints.py               # All route definitions (imported into main.py)
│   ├── agents/
│   │   ├── _init_.py
│   │   ├── summarizer.py             # JD summarization using Hugging Face
│   │   ├── parser.py                 # CV parsing and skill extraction
│   │   ├── matcher.py                # Semantic similarity computation
│   │   ├── shortlister.py            # Shortlisting based on scores
│   │   ├── notifier.py               # Email invite sender
│   │   └── utils.py                  # Common utilities
│   └── models/
│       └── dummy.txt                 # (Optional) Pretrained model weights, saved embeddings, etc.
│
├── frontend/
│   ├── app.py                        # Streamlit app entry point
│   ├── pages/
│   │   ├── 1_Upload_JD.py            # Upload & summarize JD
│   │   ├── 2_Upload_CVs.py           # Upload and parse candidate CVs
│   │   ├── 3_Match.py                # Show matches and shortlist
│   │   └── 4_Invite.py               # Invite candidates
│   └── utils/
│       ├── api.py                    # API call helper functions
│       └── parser.py                 # Frontend text parsing
│
├── data/
│   ├── sample_jd.txt                 # Sample job description
│   ├── cv_1.pdf                      # Candidate CVs
│   ├── cv_2.pdf
│   └── shortlisted.json              # Shortlisted candidates
│
├── .gitignore
├── requirements.txt                 # Dependencies for both backend & frontend
├── README.md                        # Project overview and instructions
└── run.sh                           # Script to run backend and frontend
