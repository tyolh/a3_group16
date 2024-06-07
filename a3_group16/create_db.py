from ticketlink import db, create_app
app = create_app()
ctx = app.app_context()
ctx.push()
db.session.commit()
db.create_all()
