from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import PlainTextResponse
import subprocess
from app.config import logger, YOPASS, YOPASS_URL

router = APIRouter()

@router.post("/api/v1/yopass/echo", response_class=PlainTextResponse)
def generate_yopass_link(data: str = Form()):
    """Генерирует Yopass ссылку через форму"""
    try:
        result = subprocess.run(
            [
                YOPASS,
                "--api", YOPASS_URL,
                "--url", YOPASS_URL,
                "--expiration=1w",
                "--one-time=true"
            ],
            input=data,
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Ссылка успешно сгенерирована")
        return result.stdout.strip()

        
    except subprocess.CalledProcessError as e:
        logger.error(f"Ошибка - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка {e.stderr}"
        )
    except FileNotFoundError:
        logger.error(f"Yopass binary не найден. Проверьте путь - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Yopass binary не найден. Проверьте путь"
        )