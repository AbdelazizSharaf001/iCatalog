# CRUD functions
#
# @parm var:data    (opt|obl)   - description
# ` opt: optional
# ` obl: obligatory
#
# @return           (type)      - description
#
# imports ------------------------------------------------
from json import loads
from random import choice, randint
from string import ascii_uppercase, digits
from os.path import isfile

from werkzeug.security import generate_password_hash

from flask import (
    url_for,
    jsonify,
    request,
    redirect,
    current_app as app
)

from . import db
from .fn import rand_str
from .models import Usr, Catagory, Item


# filer_by str      ------------------------------------------------
# fstr
# @parm f:obj       (dict)  - filters
# ` f:              -> {key: filter}
# ` f:  (version+)  -> {key: [parameter, filter]}
# @parm p:obj       (str)   - parameter
def fstr(f, p='='):
    out = []
    # p = p if p in ['=', '!=', '<', '>', '<>', '<=', '>='] else '='
    # parameter is listed for next version
    p = '='
    for x in f:
        # if isinstance(f[x], list):
        #     fstr([x, f[x][1]], f[x][0])
        if isinstance(f[x], str):
            out.append('%s%s"%s"' % (str(x), p, str(f[x])))
        else:
            out.append('%s%s%s' % (str(x), p, str(f[x])))
    return ','.join(out)


# crud \fn          ------------------------------------------------
# \create
# \update
#
# cuCRUD
# @parm r:obj       (obl)   - flask-SQLAlchemy object
def cuCRUD(r):
    try:
        if isinstance(r, (Usr, Catagory, Item)):
            db.session.add(r)
            db.session.commit()
            return r
        else:
            return None
    except Exception:
        return None


# \read
#
# rCRUD
# defferen way to ececute simple queries
# @parm s:int|dict  (opt)   - search|filter by
# @parm t:String    (opt)   - Table to execute against
# @parm u:Boolean   (opt)   - user login state
#
# @return           (obj)   - SQLAlchemy object
def rCRUD(s=None, t='Catagory', L=None, u=False):
    # run with flask app context
    with app.app_context():
        # limit for record to be returned
        # if searching by id or limit set to one {1}
        if (isinstance(s, int) and s > -1) or (isinstance(L, int) and L == 1):
            # only get the first occurence
            L = '.first()'
        # if limit is +ve > 1
        elif isinstance(L, int) and L > 1:
            # return a limited number of occurences
            L = '.limit(' + L + ').all()'
        # if limit is Zero {0}
        elif isinstance(L, int) and L == 0:
            # return occurance count
            L = '.count()'
        # otherwise: return all occurances
        else:
            L = '.all()'

        # try/except will take care of incorrect table name
        # Data should be tested for None return on out of index id
        try:
            # prevent Guest users from accessing not published data
            if t == 'Item':
                if bool(u):
                    p = ''
                else:
                    p = '%spublish=True' % (',' if isinstance(s, dict) else '')
            else:
                p = ''

            # if search is +ve int or Zero {0}
            if isinstance(s, int) and s > -1:
                # return one row from the table by id
                return eval('%s.query.filter_by(id=s%s)%s' % (t, p, L))
            if isinstance(s, dict):
                # return rows filtered by all dict keys
                q = '%s.query.filter_by('
                q += fstr(s)
                q += '%s)%s'
                # print(q % (t, p, L))
                return eval(q % (t, p, L))

            # rewrite filter for the query if neaded
            if t == 'Item':
                p = '.filter_by(%s)' % (p)
            # return all (puplic) table
            return eval('%s.query%s%s' % (t, p, L))
        except Exception as e:
            print(e)
            # on any error: return empty json opject
            return []


# \delete
#
# dCRUD
# @parm d:obj       (obl)   - flask-SQLAlchemy object
# @parm c:bool      (opt)   - confirm
def dCRUD(d, c=False):
    try:
        if isinstance(d, (Usr, Catagory, Item)) and c:
            db.session.delete(d)
            db.session.commit()
            return d
        else:
            return None
    except Exception:
        return None


# depending fns     ------------------------------------------------
# public id
def gen_pid(ln=0, t='Usr'):
    if not isinstance(ln, int):
        ln = 0
    pid = randint(10**(int(ln) - 1 if ln > 32 and ln < 100 else 11),
                  10**(int(ln) if ln > 32 and ln < 100 else 18))
    return gen_pid(ln) if rCRUD({'public_id': pid}, t) else pid


# public token
def gen_tk(pid=0):
    if not isinstance(pid, int):
        return
    token = str(pid) + '-' + \
        ''.join(choice(ascii_uppercase + digits)
                for _ in range(randint(84, 128)))
    return gen_tk(pid) if rCRUD({'public_token': token}, 'Usr') else token


# fill_DB
#
# create database file when it's not existed
# testing: fill database random range of data
def fill_DB(config=None):
    with app.app_context():
        if not isfile('%s/%s' % (app.name,
                                 app.config['SQLALCHEMY_DATABASE_URI'][10:])):
            # DB create
            # print('init DB..........')
            db.create_all()

            if isfile('%s/secrets/init.json' % (app.name)):
                usrData = loads(open('%s/secrets/init.json' % (app.name),
                                     'r').read())
            else:
                usrData = {
                    "uname"		: "iCatalog",
                    "email"		: "iCatalog@iCatalog.com",
                    "password"	: "iCatalog"
                }

            pid = gen_pid()
            admin_user = cuCRUD(
                Usr(
                    id=0,
                    name=usrData['uname'],
                    email=usrData['email'],
                    passwd=generate_password_hash(
                        usrData['password'],
                        method='sha256'),
                    admin=True,
                    public_id=pid,
                    public_token=gen_tk(pid)))

            new_cat = cuCRUD(
                Catagory(
                    id=0,
                    name='Uncatagorized',
                    public_id=gen_pid(None, 'Catagory'),
                    usr=admin_user
                )
            )

            # testing: fill random data for testing crud functionality
            # both create the superuser with Uncatagorized catagory
            # ` and check if it's created successfully
            if app.config['DEBUG'] or app.config['TESTING']:
                # here we start
                # print('add testing data..')

                for x in range(5):
                    pid = gen_pid()
                    new_user = cuCRUD(
                        Usr(
                            name='user_%s' %
                            str(x),
                            email='user_%s@iCatalog.com' %
                            str(x),
                            passwd=generate_password_hash(
                                'user_%s' %
                                str(x),
                                method='sha256'),
                            admin=False,
                            public_id=pid,
                            public_token=gen_tk(pid)
                        )
                    )
                users = [x for x in rCRUD(None, 'Usr')]

                # description
                desc = 'Lorem ipsum dolor sit amet, consectetur adipiscing'
                desc += ' elit ,sed do eiusmod tempor incididunt ut labore et'
                desc += ' dolore magna aliqua. Ut enim ad minim veniam, quis'
                desc += ' nostrud exercitation ullamco laboris nisi ut aliquip'
                desc += ' ex ea commodo consequat. Duis aute irure dolor in '
                desc += ' reprehenderit in voluptate velit esse cillum dolore'
                desc += ' eu fugiat nulla pariatur. Excepteur sint occaecat'
                desc += ' cupidatat non proident, sunt in culpa qui officia'
                desc += ' deserunt mollit anim id est laborum'

                # catagories
                for x in range(randint(25, 50)):
                    # create catagory
                    catx = cuCRUD(
                        Catagory(
                            name='Catagory_' + str(x + 1),
                            public_id=gen_pid(None, 'Catagory'),
                            usr=choice(users)
                        )
                    )
                cats = [x for x in rCRUD() if choice([True, False]) and
                        x.id > 0]

                # fill items automatically
                for i in range(randint(150, 200)):
                    # generate item no. x on the fly
                    cuCRUD(
                        Item(
                            name='Item.%s' % (str(i + 1)),
                            description=desc,
                            public_id=gen_pid(None, 'Item'),
                            publish=choice([True, False]),
                            usr=choice(users),
                            catagory=choice(cats)
                        )
                    )
