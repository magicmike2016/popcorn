from app import create_app, db

app = create_app()

# Crear las tablas dentro del contexto de la app
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)




