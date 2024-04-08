from fastapi import FastAPI, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List
from typing_extensions import Annotated

from .database import Base, engine
from .dependencies import get_db

from . import models, schemas


Base.metadata.create_all(bind=engine)
        
app = FastAPI(title="Addess Book")


@app.post(
    "/address/",
    tags=["Address"],
    response_model=schemas.AddressSchema
)
def create_address(
    data: schemas.CreateAddressSchema,
    db: Session = Depends(get_db)
):
    """
    API for create address into the system
    """
    address = models.Address(**data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address

@app.get(
    "/address/",
    tags=["Address"],
    response_model=List[schemas.AddressSchema]
)
def list_address(
    *,
    db: Session = Depends(get_db),
    limit: Annotated[int, Query] = 10,
    skip: Annotated[int, Query] = 0,
    search: Annotated[str, Query] = ""
):
    """
    API for list address according search key
    """
    addresses = (
        db.query(models.Address)
        .order_by(models.Address.id.desc())
    )
    if search:
         addresses = addresses.filter(
            or_(
                models.Address.name.icontains(search),
                models.Address.location.icontains(search),
                models.Address.latitude==search,
                models.Address.longitude==search,
            )
         )
    addresses = addresses.limit(limit).offset(skip)
    return addresses

@app.patch(
    "/address/{id}/",
    tags=["Address"],
    response_model=schemas.AddressSchema
)
def update_addreess(
    id: int,
    data: schemas.UpdateAddressSchema,
    db: Session = Depends(get_db)
):
    """
    API for update a single address
    """
    address = db.get(models.Address, id)
    if not address:
            raise HTTPException(status_code=404, detail="Address not found")
    updating_data = data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    for k, v in updating_data.items():
        setattr(address, k, v)
    db.commit()
    db.refresh(address)
    return address

@app.delete(
    "/address/{id}/",
    tags=["Address"],
)
def delete_address(
     id: int,
     db: Session = Depends(get_db)
):
    """
    API for remove address from the system.
    """
    obj = db.get(models.Address, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(obj)
    db.commit()
    return {"status": "SUCCESS"}
