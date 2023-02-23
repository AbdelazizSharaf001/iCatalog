# Non flask functions
#
# imports ------------------------------------------------
from os import path
from json import loads
from random import choice, randint
from string import ascii_uppercase, digits

from flask import current_app as app
from flask_login import current_user


# functions ------------------------------------------------
# random string
def rand_str(ln=0):
    return ''.join(choice(ascii_uppercase + digits)
                   for _ in range(ln if ln > 0 else randint(32, 46)))


# secrets load
def secrets_load(secrets='i_catalog/secrets',
                 f={'g': 'G_client_secrets.json',
                    'fb': 'FB_app_secrets.json'}):
    # google secrets
    if path.isfile('%s/%s' % (secrets, f['g'])):
        # if secrets file is provided load from it
        g_secrets = loads(open('%s/%s' % (secrets, f['g']), 'r').read())['web']
    else:
        # if no secrets provided
        g_secrets = {
            'redirect_uris'	: ['http://localhost:5000'],
            'client_id'		: '',
            'client_secret'	: ''
        }

    # facebook secrets
    if path.isfile('%s/%s' % (secrets, f['fb'])):
        # if secrets file is provided load from it
        fb_secrets = loads(open('%s/%s' % (secrets, f['fb']), 'r').read())
    else:
        # if no secrets provided
        fb_secrets = {
            'app_id': '',
            'app_secret': ''
        }

    # return it rendered as json
    return {
        'google': g_secrets,
        'facebook': fb_secrets
    }


# get name of looged user
def get_uname():
    # run with flask app context
    with app.app_context():
        # return username or "Guest"
        return current_user.name if current_user.is_authenticated else 'Guest'


# Deserialize datetime object into string form for JSON processing.
def dump_datetime(value, zone='utc'):
    if value is None:
        return None
    return {
        'zone': zone,
        'full': value.strftime("%c"),
        'day': value.strftime("%a"),
        'date': value.strftime("%x"),
        'pdate': value.strftime("%b %d, %Y"),
        'clock': value.strftime("%X")
    }
