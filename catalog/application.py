#!/usr/bin/python
#
# application.py - Udacity Project 3
#
# Nik Ho, 2015
#
# Main Flask application file for the project. Implements a Item Catelogue in
# the form of a Album of Dinosaurs. The project uses Bootstrap 4 Alpha for
# styling and a number of pages are rendered by passing data to a JavaScript
# front end using AJAX / JSON calls.
#
# Licence: MIT
#
import os
import random
import string
from flask import (Flask, render_template, request, redirect, jsonify, url_for,
                   flash)
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from werkzeug import secure_filename
from database_model import Base, User, Category, CategoryItem
# IMPORTS FOR THIS STEP - Udacity oauth2 course
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Config for file uploads
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = set(['bmp', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# Create the Flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Load client secrets for Google oauth
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Dinosaur Catalogue"


# Create SQLAlchemy DB engine
engine = create_engine('sqlite:///itemcatalogue.db')
Base.metadata.bind = engine


# Create SQLAlchemy DB session
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Render the login page where the user can login."""
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Function taken from the Udacity OAuth2 course.

    Used to authenticate the user to the site using their Google account.
    The function only uses the users Google account to login to the site,
    it doesn't store any user information in the database.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Set the Login Session state
    login_session['logged_in'] = True

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px; \
               -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    """Log user out of the application; Clears users info from the session."""
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['logged_in']
        del login_session['state']
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        flash("Successfully Logged Out!")
        return redirect(url_for('home'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        # return response
        flash("Something went wrong: %s" % response)
        return redirect(url_for('home'))


@app.route('/')
@app.route('/catalogue/')
def home():
    """Main catalogue ('Home') page with a list of recently added items.

    This function is very simple because the home.html page which it renders
    has JavaScript which calls the recent() function via AJAX to get the nine
    most recent additions to the items cataluge.
    """
    categories = session.query(Category).all()
    return render_template('home.html', categories=categories,
                           session=login_session)


@app.route('/catalogue/<int:category_id>/items/new/', methods=['GET', 'POST'])
def createItem(category_id):
    """Page to CREATE an individual item within a given category."""
    if 'logged_in' not in login_session:
        flash('You must be logged in to edit items!!')
        return redirect(url_for('home'))
    if request.method == 'POST':
        # Save dinosaur details
        newDinosaur = CategoryItem(name=request.form['name']
                                   .title(),
                                   description=request.form['description']
                                   .capitalize(),
                                   image_caption=request.form['caption']
                                   .title(),
                                   category_id=request.form['category'],
                                   meaning=request.form['meaning']
                                   .capitalize(),
                                   period=request.form['period']
                                   .capitalize(),
                                   diet=request.form['diet']
                                   .capitalize())
        # Save the dinosaur (item) image
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fileUrl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fileUrl)
            newDinosaur.image_url = '/' + fileUrl
        else:
            newDinosaur.image_url = 'holder.js/300x300?text=No Image!'
        # Add the new Dinosaur to the connection session
        session.add(newDinosaur)
        flash('New Dinosaur Successfully Created!')
        # Commit the change to the database
        session.commit()
        return redirect(url_for('home'))
    else:
        # GET request; determine the dinosaur category when loading the GET
        # page to prefill the correct dinosaur category field on the create
        # item page.
        if category_id == 0:
            from_home = True
            cat = {'id': 0}
        else:
            from_home = False
            cat = (
                session.query(
                    Category).filter_by(
                        id=category_id).one()).serialize
        cats = session.query(Category).all()
        return render_template('create.html', category=cat, categories=cats,
                               from_home=from_home)


@app.route('/catalogue/<int:category_id>/items/<int:item_id>/')
def showItem(category_id, item_id):
    """Display the individual item page. READable by all users."""
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(CategoryItem).filter_by(id=item_id).one()
    # return item.name
    return render_template('item.html', dinosaur=item, category=category)


@app.route('/catalogue/<int:category_id>/items/<int:category_item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(category_id, category_item_id):
    """Allows a logged in user to UPDATE catalogue item information."""
    if 'logged_in' not in login_session:
        flash('You must be logged in to edit items!!')
        return redirect(url_for('home'))
    category = session.query(Category).filter_by(id=category_id).one()
    dino = session.query(CategoryItem).filter_by(id=category_item_id).one()
    if request.method == 'GET':
        # Render the edit item page
        return render_template('update.html', dinosaur=dino,
                               category=category)
    if request.method == 'POST':
        # Save dinosaur details
        if request.form['name']:
            dino.name = request.form['name'].title()
        if request.form['description']:
            dino.description = request.form['description'].capitalize()
        if request.form['caption']:
            dino.image_caption = request.form['caption'].title()
        if request.form['category']:
            dino.category_id = request.form['category']
        if request.form['meaning']:
            dino.meaning = request.form['meaning'].capitalize()
        if request.form['period']:
            dino.period = request.form['period'].capitalize()
        if request.form['diet']:
            dino.diet = request.form['diet'].capitalize()
        # Save the dinosaur (item) image
        if request.files['image']:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fileUrl = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(fileUrl)
                dino.image_url = '/' + fileUrl
            else:
                dino.image_url = 'holder.js/300x300?text=No Image!'
        # Add the new Dinosaur to the connection session
        session.add(dino)
        flash('Dinosaur Successfully Updated!!')
        # Commit the change to the database
        session.commit()
        return redirect(url_for('home'))


@app.route('/catalogue/<int:category_id>/items/<int:category_item_id>/delete/')
def deleteItem(category_id, category_item_id):
    """DELETE an individual item. Users must be logged in to delete items."""
    if 'logged_in' not in login_session:
        flash('You must be logged in to delete items!!')
        return redirect(url_for('home'))
    itemToDelete = session.query(
        CategoryItem).filter_by(id=category_item_id).one()
    session.delete(itemToDelete)
    session.commit()
    flash('Dinosaur Successfully Deleted!!')
    return redirect(url_for('home'))


"""JSON APIs to view Catalogue Information"""


@app.route('/catalogue/home')
def recent():
    """Get the nine most recent entries added to the item catalogue.

    This function is called from the 'Home' page by an AJAX call when the page
    loads. The JavaScript on the Home page then renders item 'cards' using the
    returned JSON result.

    the function can also be called otherwise to get the results in raw JSON
    format.
    """
    rec = session.query(
        CategoryItem).order_by((CategoryItem.id).desc()).limit(9)
    rec_items = [item.serialize for item in rec]
    return_object = {'CategoryItems': rec_items}
    return jsonify(return_object)


@app.route('/catalogue/categories/json')
def getCategories():
    """Get an object list of all item categories."""
    cats = session.query(Category).all()
    cat_list = [cat.serialize for cat in cats]
    cat_object = {"Categories": cat_list}
    return jsonify(cat_object)


@app.route('/catalogue/category/<int:category_id>/json')
def getCategory(category_id):
    """Get Category information by passing the Categoy Id."""
    cat = session.query(Category).filter_by(id=category_id).one().serialize
    return jsonify(cat)


@app.route('/catalogue/<int:category_id>')
@app.route('/catalogue/<int:category_id>/items')
def catalogue(category_id):
    """List all items in the category; users cannot delete categories."""
    # Query Category info and serialize to return as JSON
    cat = (session.query(Category).filter_by(id=category_id).one()).serialize
    # Query Category Item info and serialize to return as JSON
    i = session.query(CategoryItem).filter_by(category_id=category_id).all()
    cat_items = [item.serialize for item in i]
    # Put queried items in dict and return a single JSON object
    return_object = {'Category': cat, 'CategoryItems': cat_items}
    return jsonify(return_object)


@app.route('/catalogue/item/<int:item_id>/json')
def getItem(item_id, category_id=0):
    """Get catalogue item by passing the item Id."""
    item = session.query(CategoryItem).filter_by(id=item_id).one().serialize
    return jsonify(item)


@app.route('/catalogue/items/json')
def getAllItems():
    """Get a object list of all catalogue items."""
    items = session.query(CategoryItem).all()
    item_list = [item.serialize for item in items]
    item_object = {"Items": item_list}
    return jsonify(item_object)


@app.route('/catalogue/dump/json')
def getCatalogueDump():
    """Get an list of all categories, with all items in that category."""
    category_list = []
    categories = session.query(Category).all()
    categories_list = [category.serialize for category in categories]
    for category in categories_list:
        items = session.query(
            CategoryItem).filter_by(category_id=category["id"]).all()
        items_list = [item.serialize for item in items]
        category["dinosaurs"] = items_list
        category_list.append(category)
    return jsonify({"categories": category_list})


"""Helper functions"""


def allowed_file(filename):
    """Check if the file is allowed to be uploaded to the web server."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Unused user related helper functions.

# The functions below are not used as user information is not stored on the
# local database. Could be useful to add functionality later on.


# def getUserID(email):
#     try:
#         user = session.query(User).filter_by(email = email).one()
#         return user.id
#     except:
#         return None


# def getUserInfo(user_id):
#     user = session.query(User).filter_by(id = user_id).one()
#     return user


# def createUser(login_session):
#     newUser = User(name = login_session['username'], email =
#         login_session['email'], picture = login_session['picture'])
#     session.add(newUser)
#     session.commit()
#     user = session.query(User)
#            .filter_by(email = login_session['email']).one()
#     return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
