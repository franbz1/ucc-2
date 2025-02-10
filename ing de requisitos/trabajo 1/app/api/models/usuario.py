from app.extensions import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Usuario {self.nombre}>"