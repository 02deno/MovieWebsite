
import json
from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,current_user
from .models import Film


from .models import Film, User
from . import db
from werkzeug.utils import secure_filename
import uuid as uuid  #allow us to create unique user id
import os
from website.form import SearchForm

#normally upload to cdn,not local computer 
# this is for now 
UPLOAD_FOLDER = '/Users/pc/Desktop/book web/website/static/images/'

views = Blueprint('views',__name__)

@views.route('/',methods =  ['GET','POST']) 
@login_required
def home() : 
    return render_template("home.html",user = current_user)

@views.route('/anasayfa',methods =  ['GET','POST']) 
@login_required
def anasayfa() : 
    films = Film.query
    users = User.query
    return render_template("anasayfa.html",user = current_user,films =films,users= users)

@views.route('/search',methods =  ['POST']) 
def search() : 
    form = SearchForm()
    film = Film.query 
    film = film.filter(Film.movieText.like('%'+form.searched.data+'%'))
    film = film.order_by(Film.movieName).all()
    return render_template("bireyselSearch.html",
        form = form,
        searched = form.searched.data,
        user=current_user,
        film = film)

@views.route('/searchHome',methods =  ['POST']) 
def searchHome() : 
    form = SearchForm()
    film = Film.query 
    film = film.filter(Film.movieName.like('%'+form.searched.data+'%'))
    film = film.order_by(Film.directorName).all()
    return render_template("search.html",
        form = form,
        searched = form.searched.data,
        user=current_user,
        film = film)





@views.route('/add-movie',methods =  ['GET','POST']) 
@login_required
def addMovie() : 
    if request.method == 'POST':
        movieName = request.form.get('movieName')
        directorName = request.form.get('directorName')
        movieText = request.form.get('movieText')
        rate = request.form.get('input-1')
        image = request.files['image']

       

        #grab image name
        image_filename = secure_filename(image.filename)
        #set UUID,randomize filename
        #aynı id ile file yüklemek yaygın olan bişi
        #onu rastgele değiştirmek gerekiyo
        image_name = str(uuid.uuid1()) + "_" + image_filename

        #save that image
        
   
        print(request.form)

        if len(movieName) < 1 :
            flash('Title is too short!!',category='error')
        elif len(directorName) < 3 :
            flash('Director Name is too short!!',category='error')
        elif len(movieText) < 1 :
            flash('Note is too short!!',category='error')
        else :
            image.save(os.path.join(UPLOAD_FOLDER,image_name))
            new_film = Film(movieName= movieName,
            directorName = directorName,
            movieText = movieText,
            rate = rate,
            image_name = image_name,
            user_id = current_user.id)
            db.session.add(new_film)
            db.session.commit()
            
           
            flash('Film added!',category='success')
    return render_template("add_movie.html",user = current_user)

@views.route('/delete-film',methods = ['POST'])
def delete_film():
    film = json.loads(request.data)
    filmId = film['filmId']
    film= Film.query.get(filmId)
    if film :
        if film.user_id == current_user.id :
            db.session.delete(film)
            db.session.commit()
    return jsonify({}) #return empty response

