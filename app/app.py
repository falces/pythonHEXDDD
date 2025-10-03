from flask import Flask
from config.database import configureDatabase
from config.environment import configureEnvironment
from config.exceptionHanlder import exceptionHandler
from config.log import configureLogs
from config.signals import configureSignals


app = Flask(__name__)

configureLogs(app)
signals = configureSignals(app)
configureEnvironment(app)
db = configureDatabase(app)
exceptionHandler(app)

from Infrastructure.Controller.Controller import v1ControllerBase
from Infrastructure.Controller.ToolsController import toolsController

app.register_blueprint(v1ControllerBase, url_prefix='/api/v1')
app.register_blueprint(toolsController, url_prefix='/tools')

@app.route('/', methods=['GET'])
def index():
    return {'status': 'API is running'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)