from flask import Flask
from app.config import Config
from app.extensions import db, migrate
from app.api.routes.usuarios import usuarios_bp
from app.api.routes.reservas import reservas_bp
from app.api.routes.habitaciones import habitaciones_bp
from app.api.routes.login import login_bp
from flask_cors import CORS

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  migrate.init_app(app, db)
  
  CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

  with app.app_context():
    db.create_all()
    
  app.register_blueprint(usuarios_bp)
  app.register_blueprint(reservas_bp)
  app.register_blueprint(habitaciones_bp)
  app.register_blueprint(login_bp)

  return app