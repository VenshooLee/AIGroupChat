from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from models import Database, ConversationModel, DocumentModel, SettingsModel

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    from models import Database
    db = Database()
    db.init_app(app)

    app.db = db
    app.conversation_model = ConversationModel(db)
    app.document_model = DocumentModel(db)
    app.settings_model = SettingsModel(db)

    from routes import register_routes
    register_routes(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    import webbrowser
    import socket
    import sys

    def find_available_port(start_port=5000):
        """查找可用端口"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                    return port
            except OSError:
                continue
        return None

    app = create_app()
    port = find_available_port()
    if port is None:
        print("Error: Could not find an available port")
        sys.exit(1)

    url = f'http://localhost:{port}'
    print(f"Opening {url} in browser...")
    webbrowser.open(url)

    print(f"Server running on {url}")
    app.run(host='0.0.0.0', port=port)
