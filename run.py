# run.py — punto de entrada de bariLMS
import os
from app import create_app

flask_app = create_app()

if __name__ == "__main__":
    flask_app.run(
        host="0.0.0.0", debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
