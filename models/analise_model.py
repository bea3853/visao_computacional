from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from database.connection import Base

class AnaliseModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    image_path = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    objetos = Column(String, nullable=False)
    quantidade_pessoas = Column(Integer, nullable=False)
    rostos = Column(Integer, nullable=False)
    idade = Column(String, nullable=True)
    emocao = Column(String, nullable=True)
    cores = Column(String, nullable=False)
    luminosidade = Column(Float, nullable=False)
    nitidez = Column(Float, nullable=False)
    json_resultado = Column(JSON, nullable=False)