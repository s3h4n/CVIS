from application import create_app
from flask_cors import CORS

app = create_app()
app.app_context().push()
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
