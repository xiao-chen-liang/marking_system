from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
from view.function import function
from view.account import account


app = Flask(__name__)
swagger = Swagger(app)
CORS(app)

# Register the blueprint
app.register_blueprint(function)
app.register_blueprint(account)

if __name__ == '__main__':
    app.run(debug=True)
