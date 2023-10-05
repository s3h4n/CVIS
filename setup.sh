python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt --use-pep517

mkdir -p database/images
touch database/cvis.db

flask db init

python3 manage.py

flask run
