import os
import sys

class Settings:
    # Captura as variáveis de ambiente fornecidas pelo Render ou OS local
    # Como solicitado, não utilizaremos .env em arquivos locais
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg://neondb_owner:mock_password@ep-mock-data-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
    )
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "images")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-secret-key")

    @classmethod
    def validate(cls) -> None:
        if not cls.DATABASE_URL:
            print("ERRO: DATABASE_URL não definida.", file=sys.stderr)