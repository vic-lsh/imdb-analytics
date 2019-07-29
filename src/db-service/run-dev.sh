export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=9000
# Use no reload to suppress reloader's default behavior to run the code twice
flask run --no-reload