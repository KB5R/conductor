from python_freeipa import Client
import urllib3
from app.config import IPA_HOST

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_freeipa_client(host: str = None):
    """Создаёт клиент FreeIPA без авторизации"""
    host = host or IPA_HOST
    if not host:
        raise Exception("Не задан IPA_HOST в .env файле")
    
    return Client(host=host, verify_ssl=False)


def resolve_username(client, identifier: str) -> str:
    """
    Преобразует identifier (username или email) в username.
    
    Args:
        client: FreeIPA клиент
        identifier: username или email
        
    Returns:
        username пользователя
        
    Raises:
        ValueError: если пользователь не найден
    """
    # Если это не email - возвращаем как есть
    if "@" not in identifier:
        return identifier
    
    # Ищем по email
    search_result = client._request(
        "user_find",
        args=[],
        params={"mail": identifier.lower()}
    )
    
    # Проверяем что нашли
    if search_result.get('count', 0) == 0:
        raise ValueError(f"Пользователь с email '{identifier}' не найден")
    
    users_list = search_result.get('result', [])
    if not users_list:
        raise ValueError(f"Пользователь с email '{identifier}' не найден")
    
    return users_list[0]['uid'][0]