from fastapi import Body

from schemas.spent_schema import UpdateSpentSchema
from schemas.spent_schema import CreateSpentSchema


UpdateSpentBody = Body(
    title='Spent',
    description='The update spent json representation.',
    examples=[
        CreateSpentSchema(
            name='Decathlon',
            description='Voley ball',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            category_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            payment_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            value=32.54,
            parcel_quantity=2,
            parcel_value=16.27,
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
            name='Decathlon',
            description='Golf ball',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            category_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            payment_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            value=5.36,
            parcel_quantity=0,
            parcel_value=0,
            share=True,
            active=True
        )
    ]
)