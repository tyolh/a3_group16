from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, User
from .forms import EventForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
# additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/AFL')
def AFL():
    return render_template('events/afl.html')

@eventbp.route('/Basketball')
def Basketball():
    return render_template('events/basketball.html')
  
@eventbp.route('/Boxing')
def Boxing():
    return render_template('events/boxing.html')
  
@eventbp.route('/Cricket')
def Cricket():
    return render_template('events/cricket.html')
  
@eventbp.route('/Golf')
def Golf():
    return render_template('events/golf.html')

@eventbp.route('/Tennis')
def Tennis():
    return render_template('events/tennis.html')
  
  
@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    form = CommentForm()
    return render_template('events/detail.html', event=event, form=form)

@eventbp.route('/booking')
def booking():
    return render_template('events/booking.html')
  


@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(name=form.name.data,
                  date = form.date.data,
                  start_time = form.start_time.data,
                  location = form.location.data,
                  description=form.description.data,
                  status = form.status.data,
                  sport = form.sport.data,
                  price = form.price.data,
                  image=db_file_path,)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('events/create.html', form=form)

def load_user(user_id):
    return User.get(user_id)

def check_upload_file(form):
  # get file data from form
  fp = form.image.data
  filename = fp.filename
  # get the current path of the module file… store image file relative to this path
  BASE_PATH = os.path.dirname(__file__)
  # upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH, 'static/image', secure_filename(filename))
  # store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path


@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    if form.validate_on_submit():
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user)
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment)
      db.session.commit()
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')
      # print('Your comment has been added', 'success')
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))
