from sqlalchemy.future import select
from sqlalchemy.orm import Session

from .models import Product, Order, OrderItem
from .schemas import ProductCreate, OrderCreate

# Product CRUD
async def create_product(db:Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def get_products(db: Session):
    result = await db.execute(select(Product))
    return result.scalars().all()

async def get_product(db: Session, product_id: int):
    return await db.get (Product, product_id)

async def update_product(db: Session, product_id: int, product: ProductCreate):
    db_product = await get_product(db, product_id)
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        
        await db.commit()
        await db.refresh(db_product)
    return db_product

async def delete_product(db: Session, product_id: int):
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit() 
    return db_product

# Order CRUD
async def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)

    for item in order.items:
        db_product = await get_product(db, item.product_id)
        if db_product and db_product.quantity >= item.quantity:
            db_product.quantity -= item.quantity
            db_order_item = OrderItem(
                order_id=db_order.id, product_id=item.product_id, quantity=item.quantity
            )
            db.add(db_order_item)
        else:
            raise Exception(f"Not enough stock for product {db_product.name}")
    
    await db.commit()
    return db_order

async def get_orders(db: Session):
    result = await db.execute(select(Order))
    return result.scalars().all()

async def get_order(db: Session, order_id: int):
    return await db.get(Order, order_id)

async def update_order_status(db: Session, order_id: int, status: str):
    db_order = await get_order(db, order_id)
    if db_order: 
        db_order.status = status
        await db.commit() 
        await db.refresh(db_order)
    return db_order