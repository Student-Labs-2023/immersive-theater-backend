from app import db

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(300), nullable=False)
    thumbnail_link = db.Column(db.String(300), nullable=False)

class PerfomanceAuthors(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), primary_key=True)
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    role = db.Column(db.String(60), nullable=False)

class PerfomanceImages(db.Model):
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    image_link = db.Column(db.String(300), nullable=False, primary_key=True)

class Perfomances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ticket_link = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    cover_image_link = db.Column(db.String(300), nullable=False)
    thumbnail_link = db.Column(db.String(300), nullable=False)

class AudioImages(db.Model):
    audio_id = db.Column(db.Integer, db.ForeignKey('audio.id'), primary_key=True)
    image_link = db.Column(db.String(300), nullable=False, primary_key=True)

class Audio(db.Model):
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    name = db.Column(db.String(100), nullable=False)
    audio_link = db.Column(db.String(300), nullable=False)
    short_audio_link = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False)
