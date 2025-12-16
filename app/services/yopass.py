import subprocess
from app.config import YOPASS, YOPASS_URL

def create_yopass_link(username: str, password: str):
    secret_data = f"{username}\n{password}"

    link = subprocess.run(
        [YOPASS, "--api", YOPASS_URL, "--url", YOPASS_URL, "--expiration=1w", "--one-time=true"],
        input=secret_data,
        capture_output=True,
        text=True
    )

    yopass_link = link.stdout.strip()
    return yopass_link