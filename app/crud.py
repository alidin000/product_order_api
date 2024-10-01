from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy.orm import joinedload
from .models import Product, Order, OrderItem
from .schemas import ProductCreate, OrderCreate
from app import schemas

# Product CRUD
async def create_product(db:AsyncSession, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    return await db.get (Product, product_id)

async def update_product(db: AsyncSession, product_id: int, product: ProductCreate):
    db_product = await get_product(db, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        
        await db.commit()
        await db.refresh(db_product)
    return db_product

async def delete_product(db: AsyncSession, product_id: int):
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit() 
    return db_product

# Order CRUD
async def create_order(db: AsyncSession, order: OrderCreate):
    db_order = Order(status="in_progress")
    db.add(db_order)
    
    await db.commit()
    await db.refresh(db_order)

    for item in order.items:
        db_product = await get_product(db, item.product_id)
        if db_product and db_product.quantity >= item.quantity:
            db_product.quantity -= item.quantity
            db_order_item = OrderItem(
                order_id=db_order.id, 
                product_id=item.product_id, 
                quantity=item.quantity
            )
            db.add(db_order_item)
        else:
            raise Exception(f"Not enough stock for product with ID {item.product_id}")

    await db.commit()

    result = await db.execute(
        select(Order).options(selectinload(Order.items)).filter(Order.id == db_order.id)
    )
    db_order = result.scalar()

    return schemas.Order.from_orm(db_order)



async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order).options(selectinload(Order.items)))
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int):
    return await db.get(Order, order_id)

async def update_order_status(db: AsyncSession, id: int, status: str):
    result = await db.execute(select(Order).options(joinedload(Order.items)).filter(Order.id == id))
    order = result.scalars().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Not Found")

    order.status = status

    await db.commit()
    await db.refresh(order)

    return order