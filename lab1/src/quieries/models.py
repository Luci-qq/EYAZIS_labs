import sqlalchemy as _sql
from quieries.database import Base

class TextsOrm(Base):
    __tablename__ = 'texts'
    
    name = _sql.Column(_sql.String, primary_key=True, index=True, nullable=False)
    raw_text = _sql.Column(_sql.String, nullable=False)
    tokens = _sql.Column(_sql.ARRAY(_sql.String), nullable=True)
    collocations = _sql.Column(_sql.ARRAY(_sql.String), nullable=True)

class CurrentTableOrm(Base):
    __tablename__ = 'current_table'

    name = _sql.Column(_sql.String, nullable=False, primary_key=True)