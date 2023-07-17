from fastapi import APIRouter

from app.models.user import User
from app.helpers.log_helper import app

router = APIRouter(
    prefix='/user',
    tags=['User Routes']
)

app.set_logger_name(__name__)


@router.get("/", response_model=User)
def get_user():
    response = User(
        first_name="Dinesh",
        last_name="Sinnarasse",
        email="dinesh@eminds.ai"
    )
    app.logger.info("Successfully invoked")
    return response
