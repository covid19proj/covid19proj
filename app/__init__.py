import os
from flask import Flask

app = Flask(__name__)
app.static_folder = 'static'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


from app import routes