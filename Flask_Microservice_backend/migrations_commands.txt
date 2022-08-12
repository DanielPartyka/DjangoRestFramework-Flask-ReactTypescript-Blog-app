export FLASK_APP=main.py
flask db init
flask db migrate
flask db upgrade