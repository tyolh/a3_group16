from flask import Blueprint, jsonify, request
from ticketlink.models import Ticket, TicketAvailable
from ticketlink import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/Ticket')
def get_hotel():
    tickets = db.session.scalars(db.select(Ticket)).all()
    ticket_list = [t.to_dict() for t in tickets]
    return jsonify(tickets=ticket_list)

# Note you can have multiple functions with the same route path
# as long as they deal with different HTTP methods
@api_bp.route('/tickets', methods=['POST'])
def create_():
    # Check body of request object for Content-Type: application/json
    json_dict = request.get_json()
    if not json_dict:
        return jsonify(message="No input data provided!"), 400
    # Creating SQLAlchemy Hotel object from JSON dictionary
    ticket = Ticket(name=json_dict['name'], description=json_dict['description'],
        event_id=json_dict['event_id'])
    # Reading the nested Room object
    for quantity_json in json_dict['quantities']:
        # Only valid if Room has a 0 to many rel with Hotel
        if "ticket_id" in quantity_json:
            quantities = db.session.scalar(db.select(TicketAvailable).where(TicketAvailable.id==quantity_json.id))
        else:
            quantities = TicketAvailable(type=quantity_json['ticket_type'], num_tix=quantity_json['num_tix'],
                description=quantity_json['room_description'], rate=quantity_json['room_rate'],
                ticket_id=ticket.id)
    db.session.add(ticket, quantities)
    db.session.commit()
    return jsonify(message='Successfully created new event!'), 201

# Delete existing Hotel (should also deleted related Rooms)
@api_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    ticket = db.session.scalar(db.select(Ticket).where(Ticket.id==ticket_id))
    db.session.delete(ticket)
    db.session.commit()
    return jsonify(message='Record deleted!'), 200

# Update existing Hotel
@api_bp.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    json_dict = request.get_json()
    ticket = db.session.scalar(db.select(Ticket).where(Ticket.id==ticket_id))
    ticket.name = json_dict['name']
    ticket.description = json_dict['description']
    db.session.commit()
    return jsonify(message='Record updated!'), 200
