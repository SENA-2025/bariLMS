import os
from appPF import create_app

flask_appPF = create_app()

if __name__ == "__main__":
    flask_appPF.run(
        host = "0.0.0.0",
        debug= os.getenv(
            "FLASK_DEBUG",
            "false"
        )
        .lower() == "true"
    )