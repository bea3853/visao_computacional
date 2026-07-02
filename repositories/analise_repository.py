from sqlalchemy.orm import Session
from models.analise_model import AnaliseModel
from typing import List, Optional
from datetime import date

class AnaliseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, analise: AnaliseModel) -> AnaliseModel:
        try:
            self.db.add(analise)
            self.db.commit()
            self.db.refresh(analise)
            return analise
        except Exception as e:
            self.db.rollback()
            raise e

    def get_all(self, search: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[AnaliseModel]:
        query = self.db.query(AnaliseModel)
        
        if search:
            query = query.filter(
                (AnaliseModel.descricao.ilike(f"%{search}%")) | 
                (AnaliseModel.objetos.ilike(f"%{search}%"))
            )
        
        if start_date:
            query = query.filter(AnaliseModel.created_at >= start_date)
        if end_date:
            # Inclui todo o dia selecionado no filtro de fim
            query = query.filter(AnaliseModel.created_at <= f"{end_date} 23:59:59")

        return query.order_by(AnaliseModel.created_at.desc()).all()

    def delete(self, analise_id: int) -> bool:
        try:
            analise = self.db.query(AnaliseModel).filter(AnaliseModel.id == analise_id).first()
            if analise:
                self.db.delete(analise)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise e