from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
import datetime

@as_declarative()
class Base:
    """
    Base class which provides automated table name
    and common columns for all models
    """
    @declared_attr
    def __tablename__(cls) -> str:
        import re
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower() + "s" # pluralize table name

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=datetime.datetime.utcnow)