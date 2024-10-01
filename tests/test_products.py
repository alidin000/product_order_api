import pytest
from app import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_product(db: AsyncSession):
    product_data = schemas.ProductCreate(name="Test Product", price=10.0, quantity=100)
    print("Here is the debug")
    print(type(db))
    product = await crud.create_product(db, product_data)

    assert product.name == product_data.name
    assert product.price == product_data.price
    assert product.quantity == product_data.quantity

@pytest.mark.asyncio
async def test_get_products(db: AsyncSession):
    await crud.create_product(db, schemas.ProductCreate(name="Test Product 1", price=10.0, quantity=100))
    await crud.create_product(db, schemas.ProductCreate(name="Test Product 2", price=20.0, quantity=50))
    
    products = await crud.get_products(db)
    assert len(products) == 2

@pytest.mark.asyncio
async def test_get_product(db: AsyncSession):
    product_data = schemas.ProductCreate(name="Test Product", price=10.0, quantity=100)
    product = await crud.create_product(db, product_data)
    
    retrieved_product = await crud.get_product(db, product.id)
    assert retrieved_product.id == product.id
    assert retrieved_product.name == product.name
