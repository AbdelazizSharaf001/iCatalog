#!/bin/bash
echo '-----------'
if ! [ -s '/ex.txt' ];  # <False> if file is empty or not found
then
    # echo (cat /ex.txt)
    # echo ">>> /ex.txt is found.. directly serving"
# else
    # echo (cat /ex.txt)
    echo ">>> First execution.. Installing reqquirements.."

    # installing cron
    # apt update -y --fix-missing;
    # apt install -y --no-install-recommends cron

    # # run on host
    # python -m venv .venv
    # .venv/bin/pip install --upgrade --no-cache-dir -r requirements.txt
    # . .venv/bin/activate
    pip3 install -U --no-cache-dir -r requirements.txt

    # cache cleaner
    # apt clean autoclean -y
    # apt autoremove -y
    # apt autoclean -y

    echo '1' > /ex.txt
    # echo '-----------'
fi;

# sleep 60

# rm -rf /var/lib/{apt,dpkg,cache,log}/
FLASK_DEBUG=true flask run --host 0.0.0.0 --port 80
# gunicorn -c /code/gunicorn.conf.py wsgi:application
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf