pip:
    pip install -r requirements.txt
uwsgi:
    uwsgi --http 0.0.0.0:8000 --master --module "django.core.wsgi:get_wsgi_application()"
run:
    make pip
    make uwsgi
