import os
from app import create_app

# Get the environment from an environment variable (default to 'development')
app = create_app()

if __name__ == "__main__":
    app.run(threaded=True)
