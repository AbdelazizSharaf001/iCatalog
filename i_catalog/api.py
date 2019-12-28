# API
#
# imports -----------------------------------------------
from flask import (
    flash,
    url_for,
    jsonify,
    request,
    redirect,
    Response,
    Blueprint,
    render_template,
    current_app as app
)
from flask_login import login_user, current_user

from . import db
from .crud import rCRUD
from .auth import httpauth
from .models import Usr, Catagory, Item


# init blueprint    -----------------------------------------------
api = Blueprint('api', __name__)


# API Frontend      -----------------------------------------------
@api.route('/')
def index():
    return render_template('api.html')


@api.route('/json/')
def json():
    try:
        with open('%s/etc/api_jq/1.js' % (app.name), 'r') as api_jq:
            return render_template('jsonapi.html', api_jq=api_jq.read())
    except BaseException:
        return render_template('jsonapi.html', api_jq=api_jq)


# JSON endpoint     -----------------------------------------------
# Returns JSON of all items in catalog
@api.route('/json/items/', methods=['GET', 'POST'])
def json_items():
    user = httpauth(request.authorization)
    i = 0
    res = [x.serialize for x in rCRUD(None, 'Item', None, bool(user))]
    for _ in res:
        res[i]['catagory'] = rCRUD({'public_id': res[i]['catagory_id']},
                                   'Catagory', 1).name
        res[i]['creator'] = rCRUD({'public_id': res[i]['creator']},
                                  'Usr', 1).name
        i += 1
    return jsonify(res)


# Returns JSON of all categories in catalog
@api.route('/json/categories/', methods=['GET', 'POST'])
def json_cats():
    user = httpauth(request.authorization)
    cats = [x.serialize for x in rCRUD()]
    res = []
    i = 0
    for cat in cats:
        cat['items count'] = rCRUD({'catagory_id': cat['id']},
                                   'Item', 0, True)
        cat['creator'] = rCRUD({'public_id': cat['creator']}, 'Usr', 1).name
        # if the catagory has items to view or the uncatagorized one
        if cat['items count']:
            # append it to response
            res.append(cat)
        i += 1

    return jsonify(res)


# Returns JSON of selected item in catalog
@api.route('/json/category/<int:c_id>/item/<int:i_id>/',
           methods=['GET', 'POST'])
def json_itemx(c_id, i_id):
    user = httpauth(request.authorization)
    s = {'public_id': i_id, 'catagory_id': c_id}
    i = rCRUD(s, 'Item', 1, bool(user))
    if i:
        res = i.serialize
        res['catagory'] = rCRUD({'public_id': c_id}, 'Catagory', 1).name
        res['creator'] = rCRUD({'public_id': res['creator']}, 'Usr', 1).name
        return jsonify(res)
    return jsonify({})


# Returns JSON of selected item in catalog
@api.route('/json/category/<int:c_id>/', methods=['GET', 'POST'])
def json_catx(c_id):
    user = httpauth(request.authorization)
    cat = rCRUD({'public_id': c_id}, 'Catagory', 1)
    if cat:
        # Get catagory
        r = cat.serialize
        # add items count
        r['items count'] = rCRUD({'catagory_id': c_id}, 'Item', 0, bool(user))
        # add items
        items = [x.serialize['id'] for x in rCRUD({'catagory_id': c_id},
                                                  'Item', None, bool(user))]
        r['items'] = items
        return jsonify(r)
    return jsonify({})


# Returns JSON of all pf the intire catalog
@api.route('/json/catalog/', methods=['GET', 'POST'])
def json_cat():
    user = httpauth(request.authorization)
    cats = [x.serialize for x in rCRUD()]
    usrs = [x.serialize for x in rCRUD(None, 'Usr')]
    res = []
    i = 0
    for cat in cats:
        cat['items count'] = rCRUD({'catagory_id': cat['id']},
                                   'Item', 0, bool(user))
        cat['creator'] = rCRUD({'public_id': cat['creator']}, 'Usr', 1).name
        j = 0
        items = [x.serialize for x in rCRUD({'catagory_id': cat['id']},
                                            'Item', None, bool(user))]
        for _ in items:
            items[j]['creator'] = rCRUD({'public_id': items[j]['creator']},
                                        'Usr', 1).name
            j += 1
        cat['items'] = items
        if cat['items count']:
            res.append(cat)
        i += 1
    return jsonify(res)
