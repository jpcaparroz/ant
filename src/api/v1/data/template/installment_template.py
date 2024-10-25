from datetime import date as dt

from fastapi import Body

from schemas.installment_schema import UpdateInstallmentSchema
from schemas.installment_schema import BaseInstallmentSchema


UpdateInstallmentBody = Body(
    title='Installment',
    description='The update installment json representation.',
    examples=[
        UpdateInstallmentSchema(
            spent_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            number=0,
            amount=0,
            due_date=dt(2024, 3, 30),
            value=5.36,
            paid=True
        )
    ]
)


CreateInstallmentBody = Body(
    title='Installment',
    description='The create installment json representation.',
    examples=[
        BaseInstallmentSchema(
            spent_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            number=0,
            amount=0,
            due_date=dt(2024, 3, 30),
            value=5.36,
            paid=True
        )
    ]
)
