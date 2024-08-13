python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt


uvicorn main:app --reload
