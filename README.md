# Assignment Submission Portal

Flask app + pytest tests + GitHub Actions CI + local report receiver.

## Run the application
```
python -m pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Run the tests
```
python -m pytest -v
```

## Start the report receiver
```
python receiver/receiver.py
```
It listens on http://localhost:8000 and saves every received report as `testreport.json`
in the folder where you started it.

## CI setup
- Workflow: `.github/workflows/ci.yml` (runs on every push).
- Test job runs on a self-hosted runner on my PC so `localhost` reaches the receiver.
- Repository secrets: `REPORT_URL` (= `http://localhost:8000`), and for the email bonus
  `EMAIL_USERNAME`, `EMAIL_PASSWORD` (Gmail App Password), `REPORT_EMAIL_TO`.
- Bonus: the `docs/` folder is deployed to GitHub Pages only if all tests pass on `main`.
