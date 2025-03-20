import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres.zhexouweaeltrozujqgv:Espadamaestra2020@aws-0-us-west-1.pooler.supabase.com:5432/postgres'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # Verifica si la conexión sigue activa
        "pool_recycle": 1800,   # Recicla la conexión cada 30 minutos
        "pool_size": 10,        # Máximo de conexiones activas
        "max_overflow": 5,      # Conexiones adicionales si se agota el pool
    }


    # Configuración de JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'supersecretjwtkey')
    JWT_TOKEN_LOCATION = ["cookies"]  # Configura JWT para usar cookies en lugar de headers
    JWT_COOKIE_CSRF_PROTECT = False  # Desactiva CSRF en JWT (puedes activarlo si deseas mayor seguridad)

