from sqlalchemy import Column,Integer,String,Text,DECIMAL,Enum,ForeignKey,TIMESTAMP,Boolean
from sqlalchemy.orm import relationship
import enum
from sqlalchemy.sql import func

from app.database import Base

class PropertyStatus(enum.Enum):
    AVAILABLE = "available"
    SOLD = "sold"
    RENTED = "rented"

class PropertyType(enum.Enum):
    HOUSE = "house"
    APARTMENT = "apartment"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    VILLA = "villa"
    LAND = "land"
    COMMERCIAL = "commercial"
    OFFICE = "office"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL, nullable=False)
    location = Column(Text, nullable=False)
    status = Column(Enum(PropertyStatus), nullable=False)
    type = Column(Enum(PropertyType), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    disabled = Column(Boolean, nullable=False, default=False)

    # Define the relationship to the manager (User)
    manager = relationship("User", back_populates="properties")

