from fastapi import Body

from schemas.payment_schema import UpdatePaymentSchema
from schemas.payment_schema import CreatePaymentSchema


UpdatePaymentBody = Body(
    title='Payment',
    description='The update payment json representation.',
    examples=[
        UpdatePaymentSchema(
            name='Credit',
            description='Credit payment method...',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            share=True,
            active=True
        )
    ]
)


CreatePaymentBody = Body(
    title='Payment',
    description='The create payment json representation.',
    examples=[
        CreatePaymentSchema(
            name='Debit',
            description='Debit payment method...',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            share=True,
            active=True
        )
    ]
)