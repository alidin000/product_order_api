from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import get_db

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the FastAPI Product and Order Management API!",
        "endpoints": {
            "Products": {
                "POST /products": "Create a new product",
                "GET /products": "Retrieve a list of all products",
                "GET /products/{id}": "Retrieve details of a specific product by its ID",
                "PUT /products/{id}": "Update a specific product by its ID",
                "DELETE /products/{id}": "Delete a specific product by its ID"
            },
            "Orders": {
                "POST /orders": "Create a new order",
                "GET /orders": "Retrieve a list of all orders",
                "PATCH /orders/{id}/status": "Update the status of a specific order by its ID"
            }
        }
    }


# Products endpoints
@app.post("/products", response_model=schemas.Product)
async def create_product(product: schemas.ProductCreate, db: AsyncSession  = Depends(get_db)):
    return await crud.create_product(db, product)

@app.get("/products", response_model=List[schemas.Product])
async def get_products(db: AsyncSession  = Depends(get_db)):
    return await crud.get_products(db)

@app.get("/products/{id}", response_model=schemas.Product)
async def get_product(id:int , db: AsyncSession  = Depends(get_db)):
    product = await crud.get_product(db, id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{id}", response_model=schemas.Product)
async def update_product(id:int, product: schemas.ProductCreate, db: AsyncSession  = Depends(get_db)):
    return await crud.update_product(db, id, product)

@app.delete("/products/{id}", response_model=schemas.Product)
async def delete_product(id:int , db: AsyncSession  = Depends(get_db)):
    return await crud.delete_product(db, id)

# Order endpoints
@app.post("/orders", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession  = Depends(get_db)):
    try:
        return await crud.create_order(db, order)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/orders", response_model=List[schemas.Order])
async def get_orders(db: AsyncSession  = Depends(get_db)):
    return await crud.get_orders(db)

@app.patch("/orders/{id}/status", response_model=schemas.Order)
async def update_order_status(id: int, order_status: schemas.OrderStatusUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_order_status(db, id, order_status.status)
