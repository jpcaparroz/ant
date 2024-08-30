from fastapi import APIRouter

from api.v1.endpoints import user
from api.v1.endpoints import category
from api.v1.endpoints import payment


router = APIRouter()
router.include_router(user.router, prefix='/user', tags=['User'])
router.include_router(category.router, prefix='/category', tags=['Category'])
router.include_router(payment.router, prefix='/payment', tags=['Payment'])