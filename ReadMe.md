python -m venv venv
source venv/bin/activate
pip install django pillow django-crispy-forms
django-admin startproject mayine_project
cd mayine_project
python manage.py startapp shop