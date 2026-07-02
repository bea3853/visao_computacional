# Computer Vision Streamlit Enterprise Application

## Descrição
Sistema modular de Visão Computacional para captura em tempo real, auditoria e indexação estruturada de imagens em nuvem utilizando Streamlit e PostgreSQL gerenciado no Neon.tech.

## Tecnologias Empregadas
- **Linguagem Principal:** Python 3.12+
- **Interface e Dashboard:** Streamlit
- **Mecanismo de Visão:** OpenCV (Headless) & Pillow
- **ORM e Banco de Dados:** SQLAlchemy e PostgreSQL (Neon.tech via psycopg)

## Arquitetura Estruturada
O projeto segue estritamente a Clean Architecture segregando responsabilidades em:
1. **Models (Entidades):** Definição relacional pura.
2. **Repositories (Acesso a Dados):** Isolamento de queries SQLAlchemy.
3. **Services (Lógica de Negócio):** Algoritmos computacionais puros do OpenCV.
4. **Controllers (Orquestração):** Mediação entre interface de UI e banco.

## Instalação Local (Sem Ambiente Virtual)
Execute a instalação global das dependências do sistema diretamente do manifesto:
```bash
pip install -r requirements.txt