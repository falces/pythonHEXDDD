from flask import Flask
from config.database import configureDatabase
from config.environment import configureEnvironment
from config.exceptionHanlder import exceptionHandler
from config.log import configureLogs
from config.signals import configureSignals
from config.controllers import configureControllers


app = Flask(__name__)

configureLogs(app)
signals = configureSignals(app)
configureEnvironment(app)
db = configureDatabase(app)
exceptionHandler(app)
configureControllers(app)

@app.route('/', methods=['GET'])
def index():
    return {'status': 'API is running'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)