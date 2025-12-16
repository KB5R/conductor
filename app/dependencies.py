from fastapi import HTTPException, Request
from python_freeipa import Client
from datetime import datetime, timedelta
from app.services.freeipa import create_freeipa_client

# Хранилище сессий (в продакшене используйте Redis или базу)
user_sessions = {}
# Словарь для хранения клиентов FreeIPA по сессии
ipa_clients = {}


def cleanup_session(session_id: str):
    """Удаляет сессию и связанный FreeIPA клиент"""
    if session_id in user_sessions:
        del user_sessions[session_id]
    if session_id in ipa_clients:
        del ipa_clients[session_id]


def authenticate_user(username: str, password: str) -> Client:
    """Аутентификация пользователя в FreeIPA"""
    try:
        client = create_freeipa_client()
        client.login(username, password)
        return client
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail=f"Ошибка аутентификации: {str(e)}"
        )


def get_user_client(request: Request) -> Client:
    """Получает клиент FreeIPA для текущего пользователя из сессии"""
    session_id = request.cookies.get("ipa_session")
    
    if not session_id:
        raise HTTPException(status_code=401, detail="Не авторизован")
    
    if session_id not in user_sessions:
        raise HTTPException(status_code=401, detail="Сессия истекла")
    
    session_data = user_sessions[session_id]

    # Проверяем срок действия сессии
    if datetime.now() > session_data["expires"]:
        cleanup_session(session_id)
        raise HTTPException(status_code=401, detail="Сессия истекла")
    
    if session_id not in ipa_clients:
        raise HTTPException(status_code=401, detail="Ошибка сессии")
    
    return ipa_clients[session_id]