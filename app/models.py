from . import db

class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    full_name = db.Column(db.String(300), nullable=False)
    thumbnail_link = db.Column(db.String(300), nullable=False)

    def __init__(self, **kwargs):
        super(Authors, self).__init__(**kwargs)

    def __repr__(self):
        return f"<authors {self.id}>"

class PerfomanceAuthors(db.Model):
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), primary_key=True)
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    role = db.Column(db.String(60), nullable=False)

    def __init__(self, **kwargs):
        super(PerfomanceAuthors, self).__init__(**kwargs)
    
    def __repr__(self):
        return f"<perfomance_authors {self.author_id}>"

class PerfomanceImages(db.Model):
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    image_link = db.Column(db.String(300), primary_key=True, nullable=False)

    def __init__(self, **kwargs):
        super(PerfomanceImages, self).__init__(**kwargs)

    def __repr__(self):
        return f"<perfomance_images {self.perfomance_id}>"

class Perfomances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    cover_image_link = db.Column(db.String(300), nullable=False)
    thumbnail_link = db.Column(db.String(300), nullable=False)
    tag = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, **kwargs):
        super(Perfomances, self).__init__(**kwargs)
    
    def __repr__(self):
        return f"<perfomances {self.id}>"

class AudioImages(db.Model):
    audio_id = db.Column(db.Integer, db.ForeignKey('audio.id'), primary_key=True)
    image_link = db.Column(db.String(300), nullable=False, primary_key=True)
    
    def __init__(self, **kwargs):
        super(AudioImages, self).__init__(**kwargs)

    def __repr__(self):
        return f"<audio_images {self.audio_id}>"

class Audio(db.Model):
    perfomance_id = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    order = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'))
    name = db.Column(db.String(100), nullable=False)
    audio_link = db.Column(db.String(300), nullable=False)
    short_audio_link = db.Column(db.String(300), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    def __init__(self, **kwargs):
        super(Audio, self).__init__(**kwargs)

    def __repr__(self):
        return f"<audio {self.id}, {self.name}>"

class Places(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Double, nullable=False)
    longitude = db.Column(db.Double, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super(Places, self).__init__(**kwargs)

    def __repr__(self):
        return f"<places {self.id}>"

class Payments(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    perfomance_id  = db.Column(db.Integer, db.ForeignKey('perfomances.id'), primary_key=True)
    ticket_link = db.Column(db.String(50), primary_key=True)
    status = db.Column(db.String(30), nullable=False)

    def __init__(self, **kwargs):
        super(Payments, self).__init__(**kwargs)

    def __repr__(self):
        return f"<payments {self.user_id}, {self.perfomance_id}>"
