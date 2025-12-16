from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from app.dependencies import get_user_client

router = APIRouter()

@router.post("/api/v1/utils/text-to-json")
async def text_to_json(users_text: str):
    """
    Отдаем:
    ivan@test.com
    petr@test.com
    anna@test.com

    Получаем:
    ["ivan@test.com", "petr@test.com", "anna@test.com"]
    """
    identifiers = [
        email.strip() 
        for line in users_text.split('\n') 
        if line.strip() 
        for email in line.split()
    ]
    return identifiers

@router.get("/api/v1/users/search-by-email/{email}")
def search_user_by_email_debug(email: str, request: Request):
    """
    Поиск пользователя по email (для отладки)

    Показывает что именно возвращает FreeIPA при поиске
    """
    try:
        client = get_user_client(request)

        # Пробуем разные варианты поиска
        results = {}

        # 1. Точное совпадение
        try:
            search_exact = client._request(
                "user_find",
                args=[],
                params={"mail": email}
            )
            results["exact_match"] = {
                "query": email,
                "type": str(type(search_exact)),
                "is_dict": isinstance(search_exact, dict),
                "is_list": isinstance(search_exact, list),
                "data": search_exact
            }
        except Exception as e:
            results["exact_match"] = {"error": str(e)}

        # 2. Lowercase
        try:
            search_lower = client._request(
                "user_find",
                args=[],
                params={"mail": email.lower()}
            )
            results["lowercase"] = {
                "query": email.lower(),
                "type": str(type(search_lower)),
                "is_dict": isinstance(search_lower, dict),
                "is_list": isinstance(search_lower, list),
                "data": search_lower
            }
        except Exception as e:
            results["lowercase"] = {"error": str(e)}

        # 3. Поиск по username (если это вдруг username)
        try:
            user_show = client._request("user_show", args=[email.split('@')[0]], params={})
            results["by_username"] = user_show.get('result', {})
        except Exception as e:
            results["by_username"] = {"error": str(e)}

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/api/v1/report/full-usersgroups-info")
def fullusersgroupsinfo(request: Request):
    """
    Получение информации о всех пользователях и его группах
    """
    try:
        client = get_user_client(request)
        result = client._request("user_find", args=[], params={"all":True})

        user_data = []
        csv_lines = ["username,email,groups"]

        for user in result['result']:
            username = user['uid'][0]
            email = user.get('mail', [None])[0]
            groups = user.get('memberof_group', [])

            user_info = {
                "username": username,
                "email": email,
                "groups": groups
            }
            user_data.append(user_info)

            email_str = email or ''
            groups_str = ';'.join(groups)
            csv_lines.append(f"{username},{email_str},{groups_str}")

        csv_content = '\n'.join(csv_lines)
        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=users_groups_report.csv"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка: {str(e)}"
        )

@router.get("/api/v1/report/full-info")
def full_info(request: Request):
    """
    Получение информации о всех пользователях и его группах
    """
    try:
        client = get_user_client(request)
        result = client._request("user_find", args=[], params={"all":True})

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка: {str(e)}"
        )
