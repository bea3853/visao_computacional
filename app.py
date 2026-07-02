import streamlit as strl
import pandas as pd
import json
import os
from database.connection import Base, engine, SessionLocal
from controllers.analise_controller import AnaliseController

# Configuração Global da Interface Streamlit
strl.set_page_config(
    page_title="VisionHub Pro",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização Automática das Tabelas do Neon (PostgreSQL)
Base.metadata.create_all(bind=engine)

db_session = SessionLocal()
controller = AnaliseController(db_session)

# Estilização CSS Customizada para UI Moderna
strl.markdown("""
    <style>
    .main { background-color: #0f1116; color: #e0e6ed; }
    .stButton>button { width: 100%; border-radius: 8px; background-color: #24292e; color: white; }
    .stMetric { background-color: #1a1f29; padding: 15px; border-radius: 10px; border: 1px solid #2d3748; }
    </style>
""", unsafe_allow_html=True)

# --- MENU LATERAL (Sidebar) ---
with strl.sidebar:
    strl.title("📸 VisionHub Navigation")
    strl.markdown("---")
    strl.subheader("📡 Conectividade")
    try:
        # Teste rápido de conexão nativa do Pooler do Neon
        with engine.connect() as conn:
            strl.success("Neon Cloud DB: Conectado")
    except Exception as e:
        strl.error(f"Erro de Conexão DB: {e}")
        
    strl.markdown("---")
    strl.markdown("⚡ *Pipeline OpenCV Engine ativado.*")

# --- CONTEÚDO PRINCIPAL (Tabs para organização estruturada) ---
tab_captura, tab_historico, tab_dashboard = strl.tabs(["📷 Câmera Live", "📜 Histórico de Auditoria", "📊 Analytics"])

with tab_captura:
    strl.subheader("Captura de Imagem Real-Time")
    
    col_cam, col_res = strl.columns([1, 1])
    
    with col_cam:
        # Inicializa o componente nativo de input de mídia do navegador do Streamlit
        camera_input = strl.camera_input("Foco da Lente Corporativa")
        
    with col_res:
        if camera_input is not None:
            strl.info("Foto capturada com sucesso. Processando pipeline de visão...")
            
            try:
                bytes_data = camera_input.getvalue()
                registro = controller.processar_e_salvar(bytes_data)
                
                strl.success("Resultados persistidos no Neon.tech!")
                
                # Exibição dos Componentes de Resposta Metrificada
                strl.markdown(f"### 📋 Sumário da Análise #{registro.id}")
                strl.write(f"**Descrição:** {registro.descricao}")
                strl.write(f"**Objetos Identificados:** {registro.objetos}")
                
                c1, c2, c3 = strl.columns(3)
                c1.metric("Pessoas Detectadas", registro.quantidade_pessoas)
                c2.metric("Luminosidade Média", f"{registro.luminosidade} lx")
                c3.metric("Nitidez (Laplaciano)", f"{registro.nitidez}")
                
                # Disponibilização de Download da Imagem Salva Localmente
                if os.path.exists(registro.image_path):
                    with open(registro.image_path, "rb") as file:
                        strl.download_button(
                            label="📥 Baixar Imagem Capturada",
                            data=file,
                            file_name=os.path.basename(registro.image_path),
                            mime="image/png"
                        )
            except Exception as ex:
                strl.error(f"Erro no processamento interno da pipeline: {ex}")
        else:
            strl.warning("Aguardando input ativo da webcam do dispositivo.")

with tab_historico:
    strl.subheader("Histórico Estruturado")
    
    # Filtros Avançados
    f_col1, f_col2, f_col3 = strl.columns([2, 1, 1])
    with f_col1:
        busca = strl.text_input("🔍 Pesquisar em descrição ou objetos")
    with f_col2:
        data_ini = strl.date_input("Data Inicial", value=None)
    with f_col3:
        data_fim = strl.date_input("Data Final", value=None)
        
    registros = controller.listar_analises(search=busca, start_date=data_ini, end_date=data_fim)
    
    if registros:
        # Ações de Exportação em Lote
        data_dicts = []
        for r in registros:
            d = r.json_resultado.copy()
            d["id"] = r.id
            d["image_path"] = r.image_path
            data_dicts.append(d)
            
        df_export = pd.DataFrame(data_dicts)
        
        exp_col1, exp_col2 = strl.columns(2)
        with exp_col1:
            strl.download_button(
                "📥 Exportar Dataset completo (CSV)", 
                data=df_export.to_csv(index=False).encode('utf-8'), 
                file_name="auditoria_vision.csv", 
                mime="text/csv"
            )
        with exp_col2:
            strl.download_button(
                "📥 Exportar Metadata completa (JSON)", 
                data=json.dumps(data_dicts, indent=4).encode('utf-8'), 
                file_name="auditoria_vision.json", 
                mime="application/json"
            )
            
        strl.markdown("---")
        
        # Renderização Individual em Grid das Consultas
        for item in registros:
            with strl.container():
                col_img, col_txt, col_actions = strl.columns([1, 2, 1])
                
                with col_img:
                    if os.path.exists(item.image_path):
                        strl.image(item.image_path, use_column_width=True)
                    else:
                        strl.error("Arquivo de imagem ausente no servidor.")
                        
                with col_txt:
                    strl.markdown(f"#### Análise Reg: {item.id} — *{item.created_at.strftime('%d/%m/%Y %H:%M:%S')}*")
                    strl.write(f"**Descrição:** {item.descricao}")
                    strl.write(f"**Objetos:** {item.objetos}")
                    strl.write(f"**Pessoas:** {item.quantidade_pessoas} | **Rostos:** {item.rostos}")
                    strl.write(f"**Métricas Físicas:** Cores: {item.cores} | Lum: {item.luminosidade} | Nitidez: {item.nitidez}")
                    
                with col_actions:
                    if os.path.exists(item.image_path):
                        with open(item.image_path, "rb") as f:
                            strl.download_button(
                                label="Download Foto",
                                data=f,
                                file_name=os.path.basename(item.image_path),
                                mime="image/png",
                                key=f"dl_{item.id}"
                            )
                    if strl.button("Excluir Registro", key=f"del_{item.id}"):
                        if controller.remover_analise(item.id):
                            strl.success(f"Registro {item.id} removido. Atualize a página.")
                            
                strl.markdown("---")
    else:
        strl.info("Nenhum registro encontrado para os filtros aplicados.")

with tab_dashboard:
    strl.subheader("Dashboard Analítico de Operações")
    todos_dados = controller.listar_analises()
    
    if todos_dados:
        df_dash = pd.DataFrame([{
            "id": r.id,
            "pessoas": r.quantidade_pessoas,
            "luminosidade": r.luminosidade,
            "nitidez": r.nitidez,
            "data": r.created_at
        } for r in todos_dados])
        
        m_col1, m_col2, m_col3 = strl.columns(3)
        m_col1.metric("Volume de Capturas", len(df_dash))
        m_col2.metric("Média Volumétrica de Pessoas", round(df_dash["pessoas"].mean(), 2))
        m_col3.metric("Média de Nitidez de Lente", round(df_dash["nitidez"].mean(), 2))
        
        strl.markdown("#### Tendência Temporal de Capturas")
        df_dash.set_index("data", inplace=True)
        strl.line_chart(df_dash["pessoas"])
    else:
        strl.info("Aguardando volumetria de dados para plotagem de gráficos.")

db_session.close()