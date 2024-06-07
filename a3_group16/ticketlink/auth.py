from flask import Blueprint, render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm, EventForm, BookEvent, CommentForm, UpdateEvent
#new imports:
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User, Event, Comment
from . import db

#create a blueprint
authbp = Blueprint('auth', __name__ )

@authbp.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    #the validation of form is fine, HTTP request is POST
    if (register.validate_on_submit()==True):
            #get username, password and email from the form
            uname = register.user_name.data
            pwd = register.password.data
            email = register.email_id.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.name==uname))
            if user:#this returns true when user is not None
                flash('Username already exists, please try another')
                return redirect(url_for('auth.register'))
            # don't store the password in plaintext!
            pwd_hash = generate_password_hash(pwd)
            #create a new User model object
            new_user = User(name=uname, password_hash=pwd_hash, emailid=email)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and redirect to HTML page
            return redirect(url_for('main.index'))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('user.html', form=register, heading='Register')

@authbp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the database
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name==user_name))
        #if there is no user with that name
        if user is None:
            error = 'Incorrect username'#could be a security risk to give this much info away
        #check the password - notice password hash function
        elif not check_password_hash(user.password_hash, password): # takes the hash and password
            error = 'Incorrect password'
        if error is None:
            #all good, set the login_user of flask_login to manage the user
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@authbp.route('/book_tickets/<id>', methods=['GET', 'POST'])
def book_event(id):
    form = BookEvent()
    #get an events object associated to the page and the comment
    event_obj = Event.query.filter_by(id=id).first()
    if form.validate_on_submit():
      #read the comment from the form
      Ticket = Ticket ( Event = event_obj,
            emailid = form.emailid.data,
            quantity = form.quantity.data,
            price = Ticket.quantity * Event.price,
            cardnum = form.cardnum.data,
            expiry = form.expiry.data,
            CVV = form.CVV.data) 
      #here the back-referencing works - comment.Event is set
      # and the link is created

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')
      print('Your event has been booked', 'success') 
    # using redirect sends a GET request to destination.show
    return render_template('logoutscreen.html', heading='Event Booked')

@authbp.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
    updated = Event.query.filter_by(id=id).first()

    form = UpdateEvent(obj=updated)
    if form.validate_on_submit():
        # Call the function that checks and returns image
        form.populate_obj(updated)
        # Using https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/
        updated.name = form.name.data
        updated.date = form.date.data
        updated.start_time = form.start_time.data
        updated.description = form.description.data
        updated.location = form.location.data
        updated.price = form.price.data
        updated.status = form.status.data
        updated.sport = form.sport.data
        
        # Commit the changes to the database
        db.session.add(updated)
        db.session.commit()

        print('Successfully updated event details', 'success')
        # Always end with a redirect when form is valid
        return redirect(url_for('main.index'))

    return render_template('user.html', form=form)

@authbp.route('/<id>')
def show(id):
    events = Event.query.filter_by(id=id).first()
    # create the comment form
    comment = CommentForm()    
    if comment.validate_on_submit():
        print('Successfully created new event', 'success')
        #Always end with redirect when form is valid
        return redirect(url_for('auth.show'))
    return render_template('index.html', Event=events, form=comment)


@authbp.route('/<id>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get an events object associated to the page and the comment
    event_obj = Event.query.filter_by(id=id).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        Event=event_obj,
                        User=current_user) 
      #here the back-referencing works - comment.Event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('auth.show', id=id))



@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
