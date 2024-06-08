import os

from Backend import create_app

# Creating the app instance
app = create_app()

if __name__=="__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', True))