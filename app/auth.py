# imports			-----------------------------------------------
from os import path
from time import time
from json import loads

from httplib2 import Http

from flask import (
    abort,
    flash,
    url_for,
    jsonify,
    request,
    session,
    redirect,
    Blueprint,
    render_template,
    current_app as app
)

from flask_login import (
    login_user,
    logout_user,
    current_user,
    login_required,
    user_loaded_from_header
)

from werkzeug.security import generate_password_hash, check_password_hash
from oauth2client.client import credentials_from_clientsecrets_and_code

from . import db, login_manager
from .fn import rand_str
from .crud import cuCRUD, rCRUD, gen_pid, gen_tk
from .models import Usr


# init blueprint	-----------------------------------------------
auth = Blueprint('auth', __name__)


# helper function	-----------------------------------------------
# user loader
# logged user data identifier
@login_manager.user_loader
def load_user(user_id):
    # return user id of loaded user
    return rCRUD(int(user_id), 'Usr')


# reset token for current user
@auth.route('/reset_token')
@login_required
def reset_token():
    if str(request.referrer) == str(request.host_url)[:-1] + \
            str(url_for('main.profile')):
        user = rCRUD(current_user.id, 'Usr')
        user.public_token = gen_tk(current_user.public_id)
        cuCRUD(user)
    return redirect(request.referrer)

# change password for current user
@auth.route('/change_password', methods=['POST'])
@login_required
def chpwd():
    if str(request.referrer) == str(request.host_url)[:-1] + \
            str(url_for('main.profile')):
        pwd = request.form.get('chpwd', False)
        if pwd:
            user = rCRUD(current_user.id, 'Usr')
            user.passwd = generate_password_hash(pwd, method='sha256')
            cuCRUD(user)
            return redirect(url_for('auth.logout'))
    return redirect(request.referrer)


# generate state
def gen_state(force=False, n_s=None):
    if force or not(app.config.get('STATE', []).get('state', False)) \
            or int(time()) > app.config['STATE']['exp']:
        app.config['STATE'] = {
            'state': n_s if isinstance(n_s, str) and len(n_s) > 5
            else rand_str(),
            'exp': int(time()) + 5 * 60
        }


def validate_state(state):
    print(state)
    if not(state and app.config['STATE']['state'] == state):
        abort(406)


# API auth          -----------------------------------------------
# httpauth
# to work with API and custom requests
#
# @parm apiauth:obj (obl)   - {request.authorization} as is
def httpauth(apiauth):
    user = None
    if apiauth and apiauth.username and apiauth.password:
        s = {'public_id': apiauth.username,
             'public_token': apiauth.password}
        return rCRUD(s, 'Usr', 1, True)


# Logout			-----------------------------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


# internal auth		-----------------------------------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    if request.method == 'POST':
        try:
            print(request.referrer[:len(request.base_url)], request.base_url)
            email = request.form.get('email', '')
            password = request.form.get('password', False)
            u_state = request.form.get('state', False)
            remember = True if request.form.get('remember', False) else False

            user = rCRUD({'email': email}, 'Usr', 1)

            if not(isinstance(user, Usr) and
                   check_password_hash(user.passwd, password)):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login'))

            login_user(user, remember=remember)
            return redirect(url_for('main.catalog'))
        except Exception:
            flash('Problem found, please try again.')
            return redirect(url_for('auth.login'))
    else:
        gen_state()
        return render_template('login.html',
                               state=app.config['STATE']['state'],
                               name='Login')


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    if request.method == 'POST':
        try:
            name = request.form.get('name', '')
            email = request.form.get('email', '')
            password = request.form.get('password', '')

            for x in [email, name, password]:
                if x == '':
                    flash('Insuficiant Data provided.')
                    return redirect(url_for('auth.signup'))

            if rCRUD({'email': email}, 'Usr', 1):
                flash('Email address already exists.')
                return redirect(url_for('auth.signup'))

            pid = gen_pid()
            cuCRUD(
                Usr(
                    name=name,
                    email=email,
                    passwd=generate_password_hash(
                        password,
                        method='sha256'),
                    public_id=pid,
                    public_token=gen_tk(pid)
                )
            )

            return redirect(url_for('auth.login'))
        except Exception:
            flash('''Problem found! please, try regester again.''')
            return redirect(url_for('auth.signup'))
    else:
        gen_state()
        return render_template('signup.html',
                               state=app.config['STATE']['state'],
                               name='Sign up')


# =========================================================================
# init blueprint	        -----------------------------------------------
oAuth = Blueprint('oAuth', __name__)


# oAuth (external auth)		-----------------------------------------------
@oAuth.route('/', methods=['POST'])
def oAuthState():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    gsign = app.config.get_namespace('GOOGLE_LOGIN_')
    FBsign = app.config.get_namespace('FACEBOOK_LOGIN_')

    if (request.form.get('order') and
            request.url_root[:-1] in gsign['acc_domains'] and
            request.form.get('state') and
            request.form.get('state') == app.config['STATE']['state']):

        if request.form.get('order') == 'G_id' and gsign['client_id']:
            return jsonify(gsign['client_id'][::-1])
        elif request.form.get('order') == 'FB_id' and FBsign['app_id']:
            # stop signin button untill end of development
            # return jsonify(FBsign['app_id'][::-1])
            return jsonify('')

    return jsonify('')


@oAuth.route('/gconnect', methods=['POST'])
def gconnect():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not(request.headers.get('X-Requested-With')
           and request.data):
        abort(400)

    # check for state health
    validate_state(request.args.get('state'))

    # check if secrets exists
    if not path.isfile('%s/secrets/G_client_secrets.json' % (app.name)):
        abort(500)

    # Exchange auth code for access token, refresh token, and ID token
    credentials = credentials_from_clientsecrets_and_code(
        '%s/secrets/G_client_secrets.json' % (app.name),
        ['profile', 'email'],
        request.data
    )

    # Get profile info from ID token
    name = credentials.id_token['name']
    email = credentials.id_token['email']

    # check for existing user
    user = rCRUD({'email': email}, 'Usr', 1)

    # create user if not exist
    if not user:
        pid = gen_pid()
        user = cuCRUD(
            Usr(
                name=name,
                email=email,
                passwd=generate_password_hash(
                    rand_str(),
                    method='sha256'),
                public_id=pid,
                public_token=gen_tk(pid)
            )
        )

    # make sure user exists/created
    if not user:
        # go to /signup after Failer and ajax success
        flash('Failed to login with google account.')
        return jsonify({'go': url_for('auth.signup')})

    # login
    login_user(user, remember=True)
    # /catalog after Logging ajax success
    return jsonify({'go': url_for('main.profile')})


# under developement
@oAuth.route('/fbconnect', methods=['POST'])
def fbconnect():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))

    # If this request does not have `X-Requested-With` header,
    # this could be a CSRF
    if not(request.headers.get('X-Requested-With')
           and request.data and request.args.get('id')):
        abort(400)

    # check for state health
    validate_state(request.args.get('state'))

    # check if secrets exists
    if not path.isfile('%s/secrets/FB_app_secrets.json' % (app.name)):
        abort(500)

    # Exchange auth code for access token, refresh token, and ID token
    # get instance to establish connection
    h = Http()
    # build the url
    url = 'https://graph.facebook.com/oauth/access_token'
    url += '?grant_type=fb_exchange_token'
    url += '&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app.config.get('FACEBOOK_LOGIN_APP_ID'),
        app.config.get('FACEBOOK_LOGIN_APP_SECRET'),
        request.data
    )
    print('\n', request.data[1, -1], '\n')
    print(url, '\n')
    # exchange tokens
    access_token = h.request(
        url, 'GET'
    )[1]
    # .split(',')[0].split(':')[1].replace('"', '')
    print('ACCESS: ', access_token, '\n')

    # get instance to establish connection
    h = Http()
    # rebuild url
    url = 'https://graph.facebook.com/%s' % (request.args.get('id'))
    url += '?fields=name,email'
    url += '&access_token=%s' % (access_token)
    # get user data
    data = loads(h.request(url, 'GET')[1])
    for x in data:
        print(x)

    # Get profile info from ID token
    name = data['name']
    email = data['email']

    # check for existing user
    user = rCRUD({'email': email}, 'Usr', 1)

    # create user if not exist
    if not user:
        pid = gen_pid()
        user = cuCRUD(
            Usr(
                name=name,
                email=email,
                passwd=generate_password_hash(
                    rand_str(),
                    method='sha256'),
                public_id=pid,
                public_token=gen_tk(pid)
            )
        )

    # make sure user exists/created
    if not user:
        # go to /signup after Failer and ajax success
        flash('Failed to login with google account.')
        return jsonify({'go': url_for('auth.signup')})

    # login
    login_user(user, remember=True)
    # /profile after Logging ajax success
    return jsonify({'go': url_for('main.profile')})
