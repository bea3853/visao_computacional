import os
from datetime import datetime
from sqlalchemy.orm import Session
from repositories.analise_repository import AnaliseRepository
from services.cv_service import CVService
from models.analise_model import AnaliseModel
from config.settings import Settings
from typing import List, Optional, Dict, Any
from datetime import date

class AnaliseController:
    def __init__(self, db: Session):
        self.repository = AnaliseRepository(db)

    def processar_e_salvar(self, image_bytes: bytes) -> AnaliseModel:
        # Garante diretório de armazenamento
        os.makedirs(Settings.UPLOAD_FOLDER, exist_ok=True)
        
        # Executa análise computacional
        dados_analise = CVService.analisar_imagem(image_bytes)
        
        # Salva o arquivo fisicamente
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"capture_{timestamp}.png"
        filepath = os.path.join(Settings.UPLOAD_FOLDER, filename)
        
        with open(filepath, "wb") as f:
            f.write(image_bytes)
            
        # Mapeamento de DTO para ORM Model
        model = AnaliseModel(
            image_path=filepath,
            descricao=dados_analise["descricao"],
            objetos=dados_analise["objetos"],
            quantidade_pessoas=dados_analise["quantidade_pessoas"],
            rostos=dados_analise["rostos"],
            idade=dados_analise["idade"],
            emocao=dados_analise["emocao"],
            cores=dados_analise["cores"],
            luminosidade=dados_analise["luminosidade"],
            nitidez=dados_analise["nitidez"],
            json_resultado=dados_analise
        )
        
        return self.repository.save(model)

    def listar_analises(self, search: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[AnaliseModel]:
        return self.repository.get_all(search, start_date, end_date)

    def remover_analise(self, analise_id: int) -> bool:
        return self.repository.delete(analise_id)