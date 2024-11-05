import os


# retrieved allowed oerigins from env file

allowed_origins = os.getenv('CORS_ORIGINS', '').split(',')

class Config:
    DEBUG = False
    TESTING = False
    CORS_ORIGINS = []  # Define a list of allowed origins, can be extended via environment variables

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'

    # Default allowed origins for development, including localhost, ngrok, and IPs with regex
    CORS_ORIGINS = [
        r'http://192\.168\.0\.105(:\d+)?',# Allow 192.168.0.105 on any port
        r'http://157\.245\.87\.194(:\d+)?'
        # Allow server official ip address for app
    ] + allowed_origins

class ProductionConfig(Config):
    ENV = 'production'
    # Allow only the production URLs without regex or subdomains
    CORS_ORIGINS = [
        r'http://192\.168\.0\.105(:\d+)?',# Allow 192.168.0.105 on any port
        r'http://157\.245\.87\.194(:\d+)?'
        # Allow server official ip address for app
    ] + allowed_origins

class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'

    # Inherit all the origins from both DevelopmentConfig and ProductionConfig
    CORS_ORIGINS = DevelopmentConfig.CORS_ORIGINS + ProductionConfig.CORS_ORIGINS


# Use environment variable for selecting the configuration
def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }
    return config_map.get(env, DevelopmentConfig)

