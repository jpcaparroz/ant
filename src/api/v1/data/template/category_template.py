from fastapi import Body

from schemas.category_schema import UpdateCategorySchema
from schemas.category_schema import CreateCategorySchema


UpdateCategoryBody = Body(
    title='Category',
    description='The update category json representation.',
    examples=[
        UpdateCategorySchema(
            name='Sport',
            description='A category...',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            share=True,
            active=True
        )
    ]
)


CreateCategoryBody = Body(
    title='Category',
    description='The create category json representation.',
    examples=[
        CreateCategorySchema(
            name='Sport',
            description='A category...',
            user_id='52ecc8a1-be32-4542-8992-d0be6200ac61',
            share=True,
            active=True
        )
    ]
)