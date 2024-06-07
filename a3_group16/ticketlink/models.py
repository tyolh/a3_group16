from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')


class Event(db.Model):
    __tablename__ = 'events' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time, nullable=False)
    description = db.Column(db.String(255))
    location = db.Column(db.String(255))
    sport = db.Column(db.String(255), default='AFL')
    image = db.Column(db.String(400))
    status = db.Column(db.String(255), default='Upcoming')
    price = db.Column(db.Integer)
    # ... Create the Comments db.relationship
	# relation to call event.comments and comment.event
    comments = db.relationship('Comment', backref='event')
    tickets = db.relationship('Ticket', backref='event') # Creates relationship with the booking table to keep data consistent


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


class Ticket(db.Model):
    __tablename__ = 'tickets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, nullable=False)
    date = db.Column(db.Date)
    description = db.Column(db.String(500))
    tick_avail = db.Column(db.Boolean, default=1)
    cost = db.Column(db.String(3))
    card_no = db.Column(db.String(16))
    expiry = db.Column(db.Date)
    CVV = db.Column(db.String(3)) 
    # Define the one-to-many relationship with the ticket availability.
    quantities = db.relationship('TicketAvailable', backref='ticket', lazy='dynamic')
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def to_dict(self):
        e_dict = {
            b.name: str(getattr(self, b.name)) for b in self.__table__.columns
        }
        h_quantities = []
        # Add details of related tickets to the event's h_dict
        for ticketavailable in self.quantities:
            qty_data = {
                'id': ticketavailable.id,
                'num_tix': ticketavailable.num_tix,
                'event_id': ticketavailable.event_id
            }
            h_quantities.append(qty_data)
        e_dict['quantities'] = h_quantities
        return e_dict


class TicketAvailable(db.Model):
    __tablename__ = 'quantities'
    id = db.Column(db.Integer, primary_key=True)
    ticketnum = db.Column(db.Integer, nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'))

