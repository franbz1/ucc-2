from app.extensions import db

class Habitacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False, unique=True)
    costo_por_noche = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"<Habitacion {self.numero}>"