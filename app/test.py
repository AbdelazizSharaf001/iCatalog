# Testing
#
# imports ------------------------------------------------
from flask import (
    flash,
    Blueprint,
    render_template,
    current_app as app
)

from .crud import rCRUD

# init blueprint ------------------------------------------------
test = Blueprint('test', __name__)


@test.route('/test/', methods=['GET', 'POST'])
def testing():
    return render_template('test.html')


@test.route('/delete/', methods=['GET', 'POST'])
def delete():
    catx = rCRUD(None, 'Catagory')
    for x in catx:
        flash('[delete] catagory > %s::%s' % (x.name, x.public_id))
    return render_template('confirm.html')
