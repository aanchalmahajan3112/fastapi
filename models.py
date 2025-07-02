from sqlalchemy import Column, Integer, String, ForeignKey  
from .database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = 'products'
    id= Column(Integer, primary_key=True, index=True)
    name=Column(String)
    description=Column(String)
    price=Column(Integer)
    seller_id=Column(Integer, ForeignKey('sellers.id'))  # Foreign key to the Seller table
    seller=relationship('Seller', back_populates='products')  # Establish relationship with Seller

class Seller(Base):
    __tablename__ = 'sellers'
    id= Column(Integer, primary_key=True, index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)  # In a real application, consider hashing passwords
    products= relationship('Product', back_populates='seller')  # Establish relationship with Product