# Main catalog
#
# imports ------------------------------------------------
from os.path import join

from flask import (
    flash,
    url_for,
    jsonify,
    request,
    redirect,
    Blueprint,
    render_template,
    current_app as app,
    send_from_directory
)
from flask_login import login_required, current_user

from nltk import (
    corpus,
    wordpunct_tokenize,
    download as nltk_dl
)

from . import db, login_manager
from .fn import get_uname
from .crud import (
    cuCRUD,
    rCRUD,
    dCRUD,
    gen_pid
)
from .models import Usr, Catagory, Item


# init blueprint ------------------------------------------------
main = Blueprint('main', __name__)


# favicon   ------------------------------------------------
@main.route('/favicon.ico')
def favicon():
    return send_from_directory(
        join(
            app.root_path,
            'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon')


# index     ------------------------------------------------
@main.route('/')
def index():
    return render_template('index.html')


# about     ------------------------------------------------
@main.route('/about/')
def about():
    return render_template('about.html')


# profile   ------------------------------------------------
@main.route('/profile/')
@login_required
def profile():
    cats = [x.serialize for x in rCRUD()]
    res = []
    i = 0
    for cat in cats:
        # if the catagory has items to view or the uncatagorized one
        if rCRUD({'catagory_id': cat['id']}, 'Item', 0, True) or i == 0:
            # append it to response
            res.append(cat)
        i += 1

    return render_template('profile.html',
                           cats=res,
                           items=rCRUD({'usr_id': current_user.public_id},
                                       'Item', None,
                                       current_user.is_authenticated))


# catalog   ------------------------------------------------
@main.route('/catalog/')
def catalog():
    cats = [x.serialize for x in rCRUD()]
    res = []
    i = 0
    for cat in cats:
        # if the catagory has items to view or the uncatagorized one
        if rCRUD({'catagory_id': cat['id']}, 'Item', 0, True) or i == 0:
            # append it to response
            res.append(cat)
        i += 1

    return render_template('catalog.html',
                           cats=res,
                           items=rCRUD(None, 'Item', None,
                                       current_user.is_authenticated))


@main.route('/Catagory/<int:c_id>/')
def category(c_id):
    cats = [x.serialize for x in rCRUD()]
    res = []
    i = 0
    for cat in cats:
        # if the catagory has items to view or the uncatagorized one
        if rCRUD({'catagory_id': cat['id']}, 'Item', 0, True) or i == 0:
            # append it to response
            res.append(cat)
        i += 1

    return render_template('catalog.html',
                           cats=res,
                           items=rCRUD({'catagory_id': c_id}, 'Item', None,
                                       current_user.is_authenticated))


# catagory  ------------------------------------------------
@main.route('/catagory/new/', methods=['POST'])
@login_required
def new_cat():
    nltk_dl('words')
    words = set(corpus.words.words())
    cat_name = str(request.form.get('cat_name'))

    # limit catagory name to:
    # - 2 words
    # - 30 characters
    if len(cat_name.split(' ')) > 2 or len(cat_name) > 30:
        flash('Too long name,\nonly two words (max 30 char) allowd\n\n\n' +
              'just take a moment and tell me is this seems to be a' +
              ' catagory name :)\n"' + cat_name + '"')
        # redirect back
        return redirect(request.referrer)

    # prevent Non-meaningful words as much as possible
    noMean = ", ".join('\n' + w for w in wordpunct_tokenize(cat_name)
                       if w.lower() not in words)
    if noMean:
        flash('Non-meaningful words found:' + noMean)
        # redirect back
        return redirect(request.referrer)

    # [if checks passed]
    # create catalog obj
    catx = cuCRUD(Catagory(name=cat_name,
                           public_id=gen_pid(None, 'Catagory'),
                           usr=current_user))
    if catx:
        flash_msg = cat_name
        flash_msg += '...\nCatagory created\n\n\n'
        flash_msg += ' This won\'t have effect on the catagory side list'
        flash_msg += ' unless you add new item to it.'
    else:
        flash_msg = 'Couldn\'t create a new catalog..\n\n\n' + cat_name
    flash(flash_msg)

    # redirect back
    return redirect(request.referrer)


@main.route('/catagory/edit/', methods=['POST'])
@login_required
def edit_cat():
    cat_id = str(request.form.get('cat_id'))

    s = {'public_id': cat_id}

    if current_user.id != 0:
        s['usr_id'] = current_user.public_id

    catx = rCRUD(s, 'Catagory', 1)
    if catx:
        cat_name = str(request.form.get('cat_name'))
        if not(cat_name in [x.name for x in rCRUD()]):
            nltk_dl('words')
            words = set(corpus.words.words())

            # limit catagory name to:
            # - 2 words
            # - 30 characters
            if len(cat_name.split(' ')) > 2 or len(cat_name) > 30:
                flash('Too long name,\nonly two words (max 30 char) ' +
                      'allowd\n\n\n' +
                      'just take a moment and tell me is this seems to be a' +
                      ' catagory name :)\n"' + cat_name + '"')
                # redirect back
                return redirect(request.referrer)

            # prevent Non-meaningful words as much as possible
            noMean = ", ".join('\n' + w for w in wordpunct_tokenize(cat_name)
                               if w.lower() not in words)
            if noMean:
                flash('Non-meaningful words found:' + noMean)
                # redirect back
                return redirect(request.referrer)

            catx.name = cat_name
            cuCRUD(catx)
    else:
        flash('Problem found...\n\nthere could be no catagory ' +
              'or you have no access permisions to proceed')

    # redirect back
    return redirect(request.referrer)


@main.route('/catagory/del/<int:c_id>/', methods=['GET', 'POST'])
@login_required
def del_catagory(c_id):
    # addithional security
    # block entry of un authenticated users
    if current_user.is_authenticated:
        # do not filter access availability with SuperUser
        if current_user.id != 0:
            # if not SuperUser
            # check access availability of user to item
            flash('This is an admin feature')
            return redirect(url_for('auth.catalog'))
    else:
        # block exploits
        return redirect(url_for('auth.logout'))

    # reed catagory data
    catx = rCRUD({'public_id': c_id}, 'Catagory', 1)

    # 'Undefined' catagory restrict delete
    if catx.id == 0:
        flash('[Rejected] delete\n\nThis catagory can not be deleted')
        return redirect(url_for('auth.catalog'))

    # item found
    if catx:
        # POST request
        # do not proceed if request is comming from another page
        if request.method == 'POST' and request.url == request.referrer:
            # check for user confermation
            confirm = bool(request.form.get('confirm'))
            # No confirmation
            if not confirm:
                # redirect to catalog
                redirect(url_for('main.catalog'))

            # try to delete
            # Expected
            # ` success: [obj] Item instance
            # ` failuer: None
            dcat = dCRUD(catx, confirm)
            if dcat:
                # feedback to on success
                fbk = '[%s] was deleted' % (dcat.name)

                # reed Undefined public_id
                un_d = rCRUD(0).public_id

                # move items to 'Undefined'
                for x in rCRUD({'catagory_id': c_id}, 'Item'):
                    x.catagory_id = un_d
                    cuCRUD(x)
                    # add ro feedback
                    fbk += '\n[update] item:catagory > %s::%s' % (
                        x.name, x.catagory_id)

                # flash feedback
                flash(fbk)
            else:
                flash('Problem found...\n\nthere could be no catagory ' +
                      'or you have no access permisions to proceed')
            # go to catalog at the end
            return redirect(url_for('main.catalog'))

        # GET request
        else:
            flash('[delete] catagory > %s::%s' % (catx.name, catx.public_id))
            for x in rCRUD({'catagory_id': c_id}, 'Item'):
                flash('[update] item:catagory > %s::Undefined'
                      % (x.name))
            return render_template('confirm.html')

    # Catagory not found
    else:
        flash('Problem found...\n\nCatagory Not found..\n' +
              'there could be no catagory '
              'or you have no access permisions to proceed')
        # redirect back
        return redirect(request.referrer)


# items     ------------------------------------------------
@main.route('/item/add/', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        # reject post request from Guest user
        if not current_user.is_authenticated:
            return redirect(url_for('auth.logout'))

        i_name = request.form.get('item_name')
        public = not(bool(request.form.get('private')))
        cat_id = request.form.get('catagory')
        desc = request.form.get('descrepton')

        # only accept data types needed
        if not(isinstance(i_name, str) and isinstance(public, bool) and
               isinstance(cat_id, (str, int)) and isinstance(desc, str)):
            # reject access and logout user to inforce stop modifications
            return redirect(url_for('auth.logout'))
        # for int passed as string
        elif isinstance(cat_id, (str)):
            try:
                # try to get int value from the string
                cat_id = int(cat_id)
            except Exception:
                # if string is non-convertable into int
                # also logout user that sends unwanted data types
                return redirect(url_for('auth.logout'))

        if len(i_name) < 5 or len(desc.split(' ')) < 20:
            # check minimuc character and word count
            flash('Minimum Character count failed\n\n' +
                  '[Item Name] min:&emsp;5 characters' +
                  '[description] min:&emsp;20 word')
        if len(i_name) > 150 or len(i_name.split(' ')) > 12:
            # check maximum character and word count
            flash('MAximum Character count failed\n\n' +
                  '[Item Name] max:&emsp;150 characters' +
                  '[Item Name] max:&emsp;12 word')
        else:
            # get catagory
            catx = rCRUD({'public_id': cat_id}, 'Catagory', 1)
            if not catx:
                # for filtered catagories (version+/)
                catx = rCRUD(0)
                flash('Catagory specified is not found\n' +
                      'Item automaticly added to %s\n' % (catx.name) +
                      'You could modify that later')

            # add item
            cuCRUD(Item(name=i_name,
                        description=desc,
                        public_id=gen_pid(None, 'Item'),
                        publish=public,
                        usr=current_user,
                        catagory=catx))

    res = [x.serialize for x in rCRUD()]
    cats = []
    i = 0
    for cat in res:
        # if the catagory has items to view or the uncatagorized one
        if rCRUD({'catagory_id': cat['id']}, 'Item', 0, True) or i == 0:
            # append it to response
            cats.append(cat)
        i += 1

    item = rCRUD(0, 'Item', 1, bool(current_user.is_authenticated))

    return render_template('item.html',
                           operation='Add item',
                           item=item,
                           cats=cats,
                           catz=res)


@main.route('/item/edit/<int:i_id>/', methods=['GET', 'POST'])
@login_required
def edit_item(i_id):
    item = rCRUD({'public_id': i_id}, 'Item', 1,
                 bool(current_user.is_authenticated))

    if not item:
        flash('Item was not found')
        return redirect(url_for('main.catalog'))

    if request.method == 'POST':
        # reject post request from Guest user
        if not current_user.is_authenticated:
            return redirect(url_for('auth.logout'))

        i_name = request.form.get('item_name')
        public = not(bool(request.form.get('private')))
        cat_id = request.form.get('catagory')
        desc = request.form.get('descrepton')

        # only accept data types needed
        if not(isinstance(i_name, str) and isinstance(public, bool) and
               isinstance(cat_id, (str, int)) and isinstance(desc, str)):
            # reject access and logout user to inforce stop modifications
            return redirect(url_for('auth.logout'))
        # for int passed as string
        elif isinstance(cat_id, (str)):
            try:
                # try to get int value from the string
                cat_id = int(cat_id)
            except Exception:
                # if string is non-convertable into int
                # also logout user that sends unwanted data types
                return redirect(url_for('auth.logout'))

        if len(i_name) < 5 or len(desc.split(' ')) < 20:
            # check minimuc character and word count
            flash('Minimum Character count failed\n\n' +
                  '[Item Name] min:&emsp;5 characters' +
                  '[description] min:&emsp;20 word')
        if len(i_name) > 150 or len(i_name.split(' ')) > 12:
            # check maximum character and word count
            flash('MAximum Character count failed\n\n' +
                  '[Item Name] max:&emsp;150 characters' +
                  '[Item Name] max:&emsp;12 word')
        else:
            # get catagory
            catx = rCRUD({'public_id': cat_id}, 'Catagory', 1)
            if not catx:
                # for filtered catagories (version+/)
                catx = rCRUD(0)
                flash('Catagory specified is not found\n' +
                      'Item automaticly added to %s\n' % (catx.name) +
                      'You could modify that later')

            # update data with sission (on the fly)
            item.name = i_name
            item.publish = public
            item.catagory = catx
            item.description = desc

            # update item
            cuCRUD(item)

    res = [x.serialize for x in rCRUD()]
    cats = []
    i = 0
    for cat in res:
        # if the catagory has items to view or the uncatagorized one
        if rCRUD({'catagory_id': cat['id']}, 'Item', 0, True) or i == 0:
            # append it to response
            cats.append(cat)
        i += 1

    return render_template('item.html',
                           operation='Add item',
                           item=item.serialize,
                           cats=cats,
                           catz=res)


@main.route('/item/del/<int:i_id>', methods=['GET', 'POST'])
@login_required
def del_item(i_id):
    # filters for gitting item
    s = {'public_id': i_id}

    # addithional security
    # block entry of un authenticated users
    if current_user.is_authenticated:
        # do not filter access availability with SuperUser
        if current_user.id != 0:
            # if not SuperUser
            # check access availability of user to item
            s['usr_id'] = current_user.public_id
    else:
        # block exploits
        return redirect(url_for('auth.logout'))

    # reed item data
    itemx = rCRUD(s, 'Item', 1)

    # item found
    if itemx:
        # POST request
        # do not proceed if request is comming from another page
        if request.method == 'POST' and request.url == request.referrer:
            # check for user confermation
            confirm = bool(request.form.get('confirm'))
            # No confirmation
            if not confirm:
                # redirect to catalog
                redirect(url_for('main.catalog'))

            # try to delete
            # Expected
            # ` success: [obj] Item instance
            # ` failuer: None
            ditem = dCRUD(itemx, confirm)

            # return feedback on both cases
            if ditem:
                flash('[%s] was deleted' % (ditem.name))
            else:
                flash('Problem found...\n\nthere could be no catagory ' +
                      'or you have no access permisions to proceed')

            # go to catalog at the end
            return redirect(url_for('main.catalog'))

        # GET request
        else:
            # show item name and id
            flash('[delete] Item > %s::%s' % (itemx.name, itemx.public_id))
            # render
            return render_template('confirm.html')

    # item not found
    else:
        flash('Problem found...\n\nItem Not found..\n' +
              'there could be no item '
              'or you have no access permisions to proceed')
        # redirect back
        return redirect(request.referrer)
