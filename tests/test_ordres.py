import pytest
from fastapi import HTTPException
from app import crud, schemas
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_create_order(db: AsyncSession):
    product = await crud.create_product(db, schemas.ProductCreate(name="Test Product", price=10.0, quantity=100))
    
    order_data = schemas.OrderCreate(items=[{"product_id": product.id, "quantity": 1}])
    order = await crud.create_order(db, order_data)

    assert order.status == "in_progress"
    assert len(order.items) == 1
    assert order.items[0].product_id == product.id

@pytest.mark.asyncio
async def test_get_orders(db: AsyncSession):
    product = await crud.create_product(db, schemas.ProductCreate(name="Test Product", price=10.0, quantity=100))
    await crud.create_order(db, schemas.OrderCreate(items=[{"product_id": product.id, "quantity": 1}]))
    
    orders = await crud.get_orders(db)
    assert len(orders) == 1

@pytest.mark.asyncio
async def test_update_order_status(db: AsyncSession):
    product = await crud.create_product(db, schemas.ProductCreate(name="Test Product", price=10.0, quantity=100))
    order_data = schemas.OrderCreate(items=[{"product_id": product.id, "quantity": 1}])
    order = await crud.create_order(db, order_data)
    
    updated_order = await crud.update_order_status(db, order.id, "completed")
    assert updated_order.status == "completed"

# Edge case tests
@pytest.mark.asyncio
async def test_create_order_with_insufficient_stock(db: AsyncSession):
    product = await crud.create_product(db, schemas.ProductCreate(name="Test Product", price=10.0, quantity=1))
    
    order_data = schemas.OrderCreate(items=[{"product_id": product.id, "quantity": 2}])
    
    with pytest.raises(Exception, match="Not enough stock for product with ID"):
        await crud.create_order(db, order_data)

@pytest.mark.asyncio
async def test_create_order_with_nonexistent_product(db: AsyncSession):
    order_data = schemas.OrderCreate(items=[{"product_id": 9999, "quantity": 1}])
    
    with pytest.raises(Exception, match="Not enough stock for product with ID"):
        await crud.create_order(db, order_data)

@pytest.mark.asyncio
async def test_update_order_status_with_nonexistent_order(db: AsyncSession):
    with pytest.raises(HTTPException, match="Not Found"):
        await crud.update_order_status(db, 9999, "completed")
