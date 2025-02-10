from app.extensions import db

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('habitacion.id'), nullable=False)
    
    def __repr__(self):
        return f"<Reserva {self.id}>"