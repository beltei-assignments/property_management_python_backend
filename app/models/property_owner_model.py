from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class PropertyOwner(Base):
    __tablename__ = "property_owners"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ownership_start = Column(Date, nullable=False)
    ownership_end = Column(Date, nullable=True)

    property = relationship("Property", back_populates="owners")
    owner = relationship("User")
