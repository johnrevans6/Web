from flask import Flask
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config.from_object(__name__)

app.config["DEBUG_TB_ENABLED"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

app.config['DEBUG_TB_PANELS'] = [
	'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
	'flask.ext.mongoengine.panels.MongoDebugPanel']

app.config["MONGODB_SETTINGS"] = {"DB": "koding"}
app.secret_key = 'K0D1nG'

toolbar = DebugToolbarExtension(app)

db = MongoEngine(app)