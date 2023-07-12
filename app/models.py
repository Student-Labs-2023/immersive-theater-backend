from app import db

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(300))
    thumbnail_link = db.Column(db.String(300))

class PerfomanceAuthors(db.Model):
    author_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('authors.id'))
    perfomance_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('perfomances.id'))
    role = db.Column(db.String(60))

class PerfomanceImages(db.Model):
    perfomance_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('perfomances.id'))
    image_link = db.Column(db.String(300), primary_key=True)

class Perfomances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    ticket_link = db.Column(db.String(300))
    description = db.Column(db.String(300))
    duration = db.Column(db.Integer)
    cover_image_link = db.Column(db.String(300))
    thumbnail_link = db.Column(db.String(300))

class AudioImages(db.Model):
    audio_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('audio.id'))
    image_link = db.Column(db.String(300), primary_key=True)

class Audio(db.Model):
    perfomance_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('perfomances.id'))
    order = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    name = db.Column(db.String(100))
    audio_link = db.Column(db.String(300))
    short_audio_link = db.Column(db.String(100))
    description = db.Column(db.String(300))

class Places(db.Mdoel):
    id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    latitude = db.Column(db.Double)
    longitude = db.Column(db.Double)

