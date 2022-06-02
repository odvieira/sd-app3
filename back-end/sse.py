from flask import Flask, render_template
from flask_sse import sse
from flask_cors import CORS
from flask_apscheduler import APScheduler
import os
from controller import Controller

# Flask
app = Flask(__name__)

# Cors
CORS(app)

# Redis
app.config["REDIS_URL"] = os.environ.get("REDIS_URL")
app.register_blueprint(sse, url_prefix='/stream')

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/events')
def get_events(user):
    sse.publish(, type='dataUpdate')
    return "Message sent!"

if __name__ == '__main__':
    app.run()