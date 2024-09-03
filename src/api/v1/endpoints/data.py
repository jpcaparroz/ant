from io import BytesIO

from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd

from models.category_model import CategoryModel
from models.payment_model import PaymentModel
from models.spent_model import SpentModel
from schemas.generic_schema import HttpDetail
from core.deps import get_current_user
from core.deps import get_session
from api.v1.data.crud import category_crud
from api.v1.data.crud import payment_crud
from api.v1.data.crud import spent_crud


router = APIRouter(dependencies=[Depends(get_current_user)])


### search a way to only get current user info by router dependency
@router.post("/create/category", status_code=status.HTTP_201_CREATED, 
                                 response_model=HttpDetail)
async def create_categories_from_excel(sheet_name: str, 
                                       file: UploadFile,
                                       current_user = Depends(get_current_user),
                                       db: AsyncSession = Depends(get_session)):
    df = pd.read_excel(BytesIO(await file.read()), sheet_name)

    for value in df.iloc[:, 0].dropna().values:
        try:
            await category_crud.create_category_query(CategoryModel(name=value, 
                                                              user_id=current_user.user_id), 
                                                      db)
        except Exception as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return HttpDetail(detail='Categories created successfully')


@router.post("/create/payment", status_code=status.HTTP_201_CREATED, 
                                response_model=HttpDetail)
async def create_payments_from_excel(sheet_name: str, 
                                     file: UploadFile,
                                     current_user = Depends(get_current_user),
                                     db: AsyncSession = Depends(get_session)):
    df = pd.read_excel(BytesIO(await file.read()), sheet_name)

    for value in df.iloc[:, 0].dropna().values:
        try:
            await payment_crud.create_payment_query(PaymentModel(name=value, 
                                                                 user_id=current_user.user_id), 
                                                    db)
        except Exception as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return HttpDetail(detail='Payments created successfully')


@router.post("/create/spent", status_code=status.HTTP_201_CREATED, 
                              response_model=HttpDetail)
async def create_spents_from_excel(sheet_name: str, 
                                   file: UploadFile,
                                   current_user = Depends(get_current_user),
                                   db: AsyncSession = Depends(get_session)):
    df = pd.read_excel(BytesIO(await file.read()), sheet_name)
    df.iloc[:,2] = df.iloc[:,2].fillna('')
    
    for index, row in df.iterrows():
        date = row.iloc[0]
        name = row.iloc[1]
        description = row.iloc[2]
        category = row.iloc[3]
        parcel_quantity = int(row.iloc[4]) if row.iloc[4] != '-' else None
        payment = row.iloc[5]
        value = float(row.iloc[6])

        try:
            category_id = await category_crud.get_category_id_query(category, db)
            payment_id = await payment_crud.get_payment_id_query(payment, db)
            
            spent = SpentModel(
                date= date,
                name= name,
                description= description,
                user_id= current_user.user_id,
                category_id= category_id,
                payment_id= payment_id,
                parcel_quantity= parcel_quantity if parcel_quantity else 0,
                parcel_value= value / parcel_quantity if parcel_quantity else 0,
                value= value
            )

            await spent_crud.create_spent_query(spent, db)
            
        except Exception as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return HttpDetail(detail='Spents created successfully')

