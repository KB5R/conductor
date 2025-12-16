from app.dependencies import user_sessions, get_user_client
from app.services.freeipa import resolve_username
from fastapi import APIRouter, Request


router = APIRouter()

@router.post("/api/v1/users/bulk-delete")
def bulk_delete_users(identifiers: list[str], request: Request):
    """
    Массовое удаление пользователей
    
    Принимает username или email

    ["ivan.ivanov", "petr@test.com", "petya.petrov"]
    """
    results = {"success": [], "failed": []}
    client = get_user_client(request)

    for identifier in identifiers:
        try:
            # Находим username (по email или напрямую)
            username = resolve_username(client, identifier)
            
            # Удаляем пользователя
            client._request("user_del", args=[username], params={})
            
            # Добавляем в успешные
            results["success"].append({
                "identifier": identifier,
                "username": username
            })
            
        except ValueError as e:
            # Пользователь не найден
            results["failed"].append({
                "identifier": identifier,
                "error": str(e)
            })
        except Exception as e:
            # Любая другая ошибка (FreeIPA, сеть и т.д.)
            results["failed"].append({
                "identifier": identifier,
                "error": f"Ошибка удаления: {str(e)}"
            })

    return results


@router.post("/api/v1/users/bulk-disable")
def bulk_disable_users(identifiers: list[str], request: Request):
    """
    Массовое удаление пользователей
    
    Принимает username или email

    ["ivan.ivanov", "petr@test.com", "petya.petrov"]
    """
    results = {"success": [], "failed": []}
    client = get_user_client(request)

    for identifier in identifiers:
        try:
            # Находим username (по email или напрямую)
            username = resolve_username(client, identifier)
            
            # Удаляем пользователя
            client._request("user_disable", args=[username], params={})
            
            # Добавляем в успешные
            results["success"].append({
                "identifier": identifier,
                "username": username
            })
            
        except ValueError as e:
            # Пользователь не найден
            results["failed"].append({
                "identifier": identifier,
                "error": str(e)
            })
        except Exception as e:
            # Любая другая ошибка (FreeIPA, сеть и т.д.)
            results["failed"].append({
                "identifier": identifier,
                "error": f"Ошибка отключения: {str(e)}"
            })

    return results


@router.post("/api/v1/users/bulk-enable")
def bulk_enable_users(identifiers: list[str], request: Request):
    """
    Массовое включение пользователей
    
    Принимает username или email

    ["ivan.ivanov", "petr@test.com", "petya.petrov"]
    """
    results = {"success": [], "failed": []}
    client = get_user_client(request)

    for identifier in identifiers:
        try:
            # Находим username (по email или напрямую)
            username = resolve_username(client, identifier)
            
            # Удаляем пользователя
            client._request("user_enable", args=[username], params={})
            
            # Добавляем в успешные
            results["success"].append({
                "identifier": identifier,
                "username": username
            })
            
        except ValueError as e:
            # Пользователь не найден
            results["failed"].append({
                "identifier": identifier,
                "error": str(e)
            })
        except Exception as e:
            # Любая другая ошибка (FreeIPA, сеть и т.д.)
            results["failed"].append({
                "identifier": identifier,
                "error": f"Ошибка включения: {str(e)}"
            })

    return results


@router.post("/api/v1/users/bulk-reset-password")
def bulk_reset_password(identifiers: list[str], request: Request):
    """
    Массовый сброс паролей пользователей

    Можно передавать username или email - API сам определит:
    ["ivan.ivanov", "petr@test.com", "elena.sidorova"]
    """
    results = {
        "success": [],
        "failed": []
    }

    client = get_user_client(request)

    for identifier in identifiers:
        try:
            # Находим username (вся логика внутри функции)
            username = resolve_username(client, identifier)  # ← ВОТ И ВСЁ!

            # Сбрасываем пароль
            reset_result = client._request(
                "user_mod",
                args=[username],
                params={"random": True}
            )

            password = reset_result['result']['randompassword']

            results["success"].append({
                "identifier": identifier,
                "username": username,
                "password": password
            })

        except Exception as e:
            results["failed"].append({
                "identifier": identifier,
                "error": str(e)
            })

    return results
