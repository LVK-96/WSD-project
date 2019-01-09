web: cd wsd_project && gunicorn wsd_project.wsgi --log-level=info --log-file -
release: python wsd_project/manage.py migrate && python wsd_project/manage.py collectstatic
