Create venv and install:
python -m venv venv
venv\Scripts\activate  # windows
pip install -r requirements.txt


Run migrations and seed data:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py seed_sample_data
python manage.py runserver


Open: http://127.0.0.1:8000/movies/ — pick a show, book, simulate payment, see ticket code.
