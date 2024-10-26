from datetime import date as dt

from fastapi import Body

from schemas.spent_schema import UpdateSpentSchema
from schemas.spent_schema import CreateSpentSchema


UpdateSpentBody = Body(
    title='Spent',
    description='The update spent json representation.',
    examples=[
        CreateSpentSchema(
            date=dt(2024, 3, 30),
            name='Decathlon',
            description='Voley ball',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            category_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            payment_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            value=32.54,
            installment_quantity=2,
            installment_value=16.27,
            share=True,
            active=True
        )
    ]
)


CreateSpentBody = Body(
    title='Spent',
    description='The create spent json representation.',
    examples=[
        UpdateSpentSchema(
            date=dt(2024, 3, 30),
            name='Decathlon',
            description='Golf ball',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            category_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            payment_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            value=5.36,
            installment_quantity=0,
            installment_value=0,
            share=True,
            active=True
        )
    ]
)