from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

@router. get("/api/v1/tempalates/templates-excel")
def output_exel_templats() -> FileResponse:
    """
    Скачать шаблон excel для массового создания пользователя
    """
    return FileResponse(
        path="templates/freeipa_users_template.xlsx",
        filename="freeipa_users_template.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)