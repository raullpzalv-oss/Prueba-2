import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import json
import uuid
import random
import io

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Incidencias - Rodalies Catalunya",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0055a4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #0055a4;
        border-left: 4px solid #0055a4;
        padding-left: 10px;
        margin: 2rem 0 1rem 0;
    }
    .incidencia-card {
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        background-color: white;
    }
    .impacto-bajo { background-color: #d4edda; }
    .impacto-medio { background-color: #fff3cd; }
    .impacto-alto { background-color: #f8d7da; }
    .btn-primary {
        background-color: #0055a4;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
    }
    .ia-generated {
        border-left: 3px solid #28a745;
        padding-left: 10px;
        background-color: #f8fff9;
    }
    .station-line {
        font-size: 0.8em;
        color: #666;
        margin-left: 5px;
    }
    .tren-item {
        background-color: #f8f9fa;
        padding: 8px;
        margin: 5px 0;
        border-radius: 5px;
        border-left: 3px solid #0055a4;
    }
</style>
""", unsafe_allow_html=True)

class SistemaIA:
    """Clase para generar contenido automático usando IA simulada"""
    
    @staticmethod
    def generar_copernico(incidencia):
        """Generar contenido para Copernico basado en la incidencia"""
        tipo = incidencia['tipo']
        repercusion = incidencia['repercusion']
        linea = incidencia.get('linea', '')
        estacion_a = incidencia.get('estacion_a', '')
        estacion_b = incidencia.get('estacion_b', '')
        
        # Descripción automática
        descripcion = f"Incidente de {tipo.lower()} en la línea {linea}"
        if estacion_a and estacion_b:
            descripcion += f" entre {estacion_a} y {estacion_b}"
        
        # Consecuencias basadas en la repercusión
        consecuencias_map = {
            "Afectación tren puntual": "Afecta a un tren específico con retrasos moderados",
            "Demoras leves en la línea": "Retrasos generalizados de 5-15 minutos en la línea",
            "Demoras graves en la línea": "Retrasos significativos de 15-30 minutos afectando múltiples trenes",
            "Interrupción parcial del Servicio": "Servicio reducido en parte del trayecto",
            "Interrupción total del Servicio": "Suspensión completa del servicio en la línea afectada"
        }
        
        consecuencias = consecuencias_map.get(repercusion, "Consecuencias por determinar")
        
        # Acción comercial
        acciones_comerciales = [
            "Se aplicarán bonificaciones a los usuarios afectados según la normativa vigente",
            "Se habilita transporte alternativo por autobús para los trayectos afectados",
            "Los abonos temporales se extenderán por el tiempo de afectación",
            "Se recomienda consultar canales oficiales para actualizaciones en tiempo real"
        ]
        
        accion_comercial = random.choice(acciones_comerciales)
        
        return {
            'descripcion': descripcion,
            'consecuencias': consecuencias,
            'accion_comercial': accion_comercial
        }
    
    @staticmethod
    def generar_sia_barcelona(incidencia):
        """Generar mensajes para SIA Barcelona en múltiples idiomas"""
        tipo = incidencia['tipo']
        linea = incidencia.get('linea', '')
        estacion_a = incidencia.get('estacion_a', '')
        estacion_b = incidencia.get('estacion_b', '')
        
        # Catalán
        mensajes_cat = {
            'monitor': f"Incident {tipo} línia {linea}. Retards previstos.",
            'teleindicador': f"INCIDENT {tipo.upper()} - LÍNIA {linea}",
            'megafonia': f"Atenció viatgers. Incident a la línia {linea}. Consulteu informacions."
        }
        
        # Castellano
        mensajes_cast = {
            'monitor': f"Incidente {tipo} línea {linea}. Retrasos previstos.",
            'teleindicador': f"INCIDENTE {tipo.upper()} - LÍNEA {linea}",
            'megafonia': f"Atención viajeros. Incidente en la línea {linea}. Consulten informaciones."
        }
        
        # Inglés
        mensajes_eng = {
            'monitor': f"{tipo} incident line {linea}. Expected delays.",
            'teleindicador': f"INCIDENT {tipo.upper()} - LINE {linea}",
            'megafonia': f"Attention passengers. Incident on line {linea}. Please check information displays."
        }
        
        return {
            'cat': mensajes_cat,
            'cast': mensajes_cast,
            'eng': mensajes_eng
        }
    
    @staticmethod
    def generar_plataforma_embarcada(incidencia):
        """Generar mensajes para plataforma embarcada"""
        tipo = incidencia['tipo']
        linea = incidencia.get('linea', '')
        
        mensajes = {
            'cat': {
                'baliza_inicio': f"Incident línia {linea} - Retards",
                'baliza_interior': f"Línia {linea} afectada per {tipo}",
                'trenes_detenidos': "Trens amb parades prolongades - Disculpin les molèsties",
                'trenes_suprimidos': "Alguns trens podrien ser suprimits - Consultin alternatives"
            },
            'cast': {
                'baliza_inicio': f"Incidente línea {linea} - Retrasos",
                'baliza_interior': f"Línea {linea} afectada por {tipo}",
                'trenes_detenidos': "Trenes con paradas prolongadas - Disculpen las molestias",
                'trenes_suprimidos': "Algunos trenes podrían ser suprimidos - Consulten alternativas"
            },
            'eng': {
                'baliza_inicio': f"Incident line {linea} - Delays",
                'baliza_interior': f"Line {linea} affected by {tipo}",
                'trenes_detenidos': "Trains with extended stops - Sorry for the inconvenience",
                'trenes_suprimidos': "Some trains may be cancelled - Check alternatives"
            }
        }
        
        return mensajes
    
    @staticmethod
    def generar_redes_sociales(incidencia):
        """Generar mensajes para redes sociales"""
        tipo = incidencia['tipo']
        linea = incidencia.get('linea', '')
        repercusion = incidencia['repercusion']
        
        hashtags = "#Rodalies #Incident #Transport"
        
        mensajes = {
            'cat': {
                'mensaje': f"⚠️ Incident {tipo} línia {linea}. {repercusion}. {hashtags}"
            },
            'cast': {
                'mensaje': f"⚠️ Incidente {tipo} línea {linea}. {repercusion}. {hashtags}"
            },
            'eng': {
                'mensaje': f"⚠️ {tipo} incident line {linea}. {repercusion}. {hashtags}"
            }
        }
        
        return mensajes

class SistemaIncidencias:
    def __init__(self):
        self.incidencias = []
        self.estaciones_df, self.lineas = self.cargar_estaciones()
        self.sistema_ia = SistemaIA()
        self.tipos_incidencia = [
            "Avería Infraestructura",
            "Avería Tren", 
            "Meteorología adversa",
            "Orden público/Fuerza mayor",
            "Trabajos programados",
            "Operaciones"
        ]
        self.repercusiones = [
            "Afectación tren puntual",
            "Demoras leves en la línea", 
            "Demoras graves en la línea",
            "Interrupción parcial del Servicio en la línea",
            "Interrupción total del Servicio en la línea"
        ]
        
    def cargar_estaciones(self):
        """Cargar estaciones desde CSV con formato específico"""
        try:
            # Leer el archivo CSV con separador punto y coma
            df = pd.read_csv('Estaciones Catalunya.csv', sep=';', encoding='utf-8')
            
            # Procesar el formato especial del archivo
            # La primera fila contiene las líneas
            # Las siguientes filas contienen las estaciones por línea
            lineas = df.columns.tolist()
            
            # Crear un DataFrame limpio de estaciones
            estaciones_data = []
            
            for i, linea in enumerate(lineas):
                # Obtener todas las estaciones de esta línea (excluyendo NaN)
                estaciones_linea = df[linea].dropna().tolist()
                
                for estacion in estaciones_linea:
                    if estacion and estacion.strip():  # Excluir valores vacíos
                        estaciones_data.append({
                            'estacion': estacion.strip(),
                            'linea': linea
                        })
            
            estaciones_df = pd.DataFrame(estaciones_data)
            
            # Ordenar por nombre de estación
            estaciones_df = estaciones_df.sort_values('estacion')
            
            return estaciones_df, lineas
            
        except FileNotFoundError:
            st.error("No se encontró el archivo 'Estaciones Catalunya.csv'")
            # Datos de ejemplo como fallback
            estaciones_data = [
                {'estacion': 'Barcelona-Sants', 'linea': 'R1'},
                {'estacion': 'Barcelona-Passeig de Gràcia', 'linea': 'R2'},
                {'estacion': 'L’Hospitalet de Llobregat', 'linea': 'R1'},
                {'estacion': 'Mataró', 'linea': 'R1'},
                {'estacion': 'Granollers Centre', 'linea': 'R3'},
            ]
            estaciones_df = pd.DataFrame(estaciones_data)
            lineas = ['R1', 'R2', 'R3', 'R4']
            return estaciones_df, lineas
    
    def obtener_estaciones_por_linea(self, linea):
        """Obtener estaciones para una línea específica"""
        if linea and not self.estaciones_df.empty:
            return self.estaciones_df[self.estaciones_df['linea'] == linea]['estacion'].tolist()
        return []
    
    def obtener_todas_estaciones(self):
        """Obtener todas las estaciones únicas"""
        if not self.estaciones_df.empty:
            return sorted(self.estaciones_df['estacion'].unique())
        return []
    
    def generar_id_incidencia(self):
        """Generar ID alfanumérico de 6 cifras"""
        return f"INC{str(uuid.uuid4())[:3].upper()}"
    
    def agregar_incidencia(self, incidencia):
        """Agregar una nueva incidencia"""
        incidencia['id'] = self.generar_id_incidencia()
        incidencia['fecha_creacion'] = datetime.now()
        self.incidencias.append(incidencia)
        return incidencia['id']
    
    def cerrar_incidencia(self, id_incidencia):
        """Cerrar una incidencia"""
        for incidencia in self.incidencias:
            if incidencia['id'] == id_incidencia:
                incidencia['hora_final'] = datetime.now().strftime("%H:%M")
                incidencia['estado'] = 'Cerrada'
                break
    
    def obtener_incidencias_activas(self):
        """Obtener incidencias activas"""
        return [inc for inc in self.incidencias if inc.get('estado') != 'Cerrada']

def mostrar_dashboard(sistema):
    """Mostrar el dashboard principal con tabla de incidencias"""
    st.markdown('<div class="main-header">🚆 Gestión de Incidencias - Rodalies Catalunya</div>', unsafe_allow_html=True)
    
    # Botón para nueva incidencia
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Nueva Incidencia", use_container_width=True):
            st.session_state.crear_incidencia = True
            st.rerun()
    
    # Mostrar incidencias activas
    incidencias_activas = sistema.obtener_incidencias_activas()
    
    if not incidencias_activas:
        st.info("No hay incidencias activas en este momento.")
        return
    
    # Crear DataFrame para mostrar
    datos_tabla = []
    for inc in incidencias_activas:
        datos_tabla.append({
            'ID': inc['id'],
            'Tipo': inc['tipo'],
            'Afectación': f"{inc.get('estacion_a', '')} - {inc.get('estacion_b', '')}",
            'Repercusión': inc['repercusion'],
            'Descripción': inc.get('descripcion', '')[:50] + '...' if inc.get('descripcion') else '',
            'Previsión': inc.get('prevision', '')[:30] + '...' if inc.get('prevision') else '',
            'Estado': 'Activa'
        })
    
    if datos_tabla:
        df = pd.DataFrame(datos_tabla)
        
        # Aplicar estilos según la repercusión
        def color_por_repercusion(val):
            if 'grave' in val or 'total' in val:
                return 'background-color: #f8d7da'
            elif 'leve' in val or 'parcial' in val:
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #d4edda'
        
        styled_df = df.style.applymap(color_por_repercusion, subset=['Repercusión'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Permitir hacer click en una fila para ver detalles
        st.subheader("Detalles de Incidencia")
        selected_id = st.selectbox("Selecciona una incidencia para ver detalles:", 
                                 [inc['id'] for inc in incidencias_activas])
        
        if selected_id:
            mostrar_detalles_incidencia(sistema, selected_id)

def mostrar_detalles_incidencia(sistema, id_incidencia):
    """Mostrar detalles de una incidencia específica"""
    incidencia = next((inc for inc in sistema.incidencias if inc['id'] == id_incidencia), None)
    
    if not incidencia:
        st.error("Incidencia no encontrada")
        return
    
    with st.expander(f"Detalles de Incidencia {id_incidencia}", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**Tipo:** {incidencia['tipo']}")
            st.write(f"**Fecha inicio:** {incidencia.get('fecha_inicio', '')}")
            st.write(f"**Hora inicio:** {incidencia.get('hora_inicio', '')}")
        
        with col2:
            st.write(f"**Repercusión:** {incidencia['repercusion']}")
            st.write(f"**Línea:** {incidencia.get('linea', '')}")
            st.write(f"**Estado:** {incidencia.get('estado', 'Activa')}")
        
        with col3:
            if incidencia.get('estado') == 'Activa':
                if st.button("🔒 Cerrar Incidencia", key=f"cerrar_{id_incidencia}"):
                    sistema.cerrar_incidencia(id_incidencia)
                    st.success("Incidencia cerrada correctamente")
                    st.rerun()
        
        st.write(f"**Descripción:** {incidencia.get('descripcion', '')}")
        st.write(f"**Previsión de resolución:** {incidencia.get('prevision', '')}")
        
        # Mostrar información específica según el tipo
        if incidencia['tipo'] == 'Avería Infraestructura':
            st.write(f"**Dependencia:** {incidencia.get('dependencia', '')}")
        elif incidencia['tipo'] == 'Avería Tren':
            st.write(f"**Nº Tren:** {incidencia.get('numero_tren', '')}")

def mostrar_seccion_comunicaciones():
    """Mostrar las secciones de comunicaciones con IA funcional"""
    
    # Sección 3: Copernico Incidencia
    st.markdown('<div class="section-header">Sección 3. Copernico Incidencia</div>', unsafe_allow_html=True)
    
    col_num_ut, col_btn_copernico = st.columns([2, 1])
    with col_num_ut:
        num_ut = st.text_input("Nº UT afectada", key="num_ut")
    
    with col_btn_copernico:
        copernico_generado = st.form_submit_button("🤖 Generar IA Copernico", use_container_width=True)
        if copernico_generado:
            # Esta lógica se manejará después del submit
            pass
    
    # Mostrar campos de Copernico
    if 'copernico_generado' in st.session_state:
        st.markdown('<div class="ia-generated">', unsafe_allow_html=True)
        descripcion_copernico = st.text_area(
            "Descripción", 
            value=st.session_state.copernico_generado['descripcion'],
            key="descripcion_copernico"
        )
        consecuencias_copernico = st.text_area(
            "Consecuencias", 
            value=st.session_state.copernico_generado['consecuencias'],
            key="consecuencias_copernico"
        )
        accion_comercial_copernico = st.text_area(
            "Acción comercial", 
            value=st.session_state.copernico_generado['accion_comercial'],
            key="accion_comercial_copernico"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección 4: SIA Barcelona
    st.markdown('<div class="section-header">Sección 4. SIA Barcelona</div>', unsafe_allow_html=True)
    
    sia_generado = st.form_submit_button("🤖 Generar IA SIA Barcelona", use_container_width=True)
    if sia_generado:
        # Esta lógica se manejará después del submit
        pass
    
    if 'sia_generado' in st.session_state:
        st.markdown('<div class="ia-generated">', unsafe_allow_html=True)
        
        # Pestañas para diferentes idiomas
        tab1, tab2, tab3 = st.tabs(["CATALÁN", "CASTELLANO", "INGLÉS"])
        
        with tab1:
            st.subheader("Catalán")
            st.text_area("Mensaje Monitor", value=st.session_state.sia_generado['cat']['monitor'], key="monitor_cat")
            st.text_area("Mensaje Teleindicador", value=st.session_state.sia_generado['cat']['teleindicador'], key="teleindicador_cat")
            st.text_area("Mensaje Megafonía", value=st.session_state.sia_generado['cat']['megafonia'], key="megafonia_cat")
        
        with tab2:
            st.subheader("Castellano")
            st.text_area("Mensaje Monitor", value=st.session_state.sia_generado['cast']['monitor'], key="monitor_cast")
            st.text_area("Mensaje Teleindicador", value=st.session_state.sia_generado['cast']['teleindicador'], key="teleindicador_cast")
            st.text_area("Mensaje Megafonía", value=st.session_state.sia_generado['cast']['megafonia'], key="megafonia_cast")
        
        with tab3:
            st.subheader("Inglés")
            st.text_area("Mensaje Monitor", value=st.session_state.sia_generado['eng']['monitor'], key="monitor_eng")
            st.text_area("Mensaje Teleindicador", value=st.session_state.sia_generado['eng']['teleindicador'], key="teleindicador_eng")
            st.text_area("Mensaje Megafonía", value=st.session_state.sia_generado['eng']['megafonia'], key="megafonia_eng")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección 5: Plataforma embarcada
    st.markdown('<div class="section-header">Sección 5. Plataforma Embarcada</div>', unsafe_allow_html=True)
    
    plataforma_generado = st.form_submit_button("🤖 Generar IA Plataforma", use_container_width=True)
    if plataforma_generado:
        # Esta lógica se manejará después del submit
        pass
    
    if 'plataforma_generado' in st.session_state:
        st.markdown('<div class="ia-generated">', unsafe_allow_html=True)
        
        tab4, tab5, tab6 = st.tabs(["CATALÁN", "CASTELLANO", "INGLÉS"])
        
        with tab4:
            st.subheader("Catalán")
            st.text_area("Baliza estaciones inicio", value=st.session_state.plataforma_generado['cat']['baliza_inicio'], key="baliza_inicio_cat")
            st.text_area("Baliza estaciones interior", value=st.session_state.plataforma_generado['cat']['baliza_interior'], key="baliza_interior_cat")
            st.text_area("Trenes detenidos", value=st.session_state.plataforma_generado['cat']['trenes_detenidos'], key="trenes_detenidos_cat")
            st.text_area("Trenes suprimidos", value=st.session_state.plataforma_generado['cat']['trenes_suprimidos'], key="trenes_suprimidos_cat")
        
        with tab5:
            st.subheader("Castellano")
            st.text_area("Baliza estaciones inicio", value=st.session_state.plataforma_generado['cast']['baliza_inicio'], key="baliza_inicio_cast")
            st.text_area("Baliza estaciones interior", value=st.session_state.plataforma_generado['cast']['baliza_interior'], key="baliza_interior_cast")
            st.text_area("Trenes detenidos", value=st.session_state.plataforma_generado['cast']['trenes_detenidos'], key="trenes_detenidos_cast")
            st.text_area("Trenes suprimidos", value=st.session_state.plataforma_generado['cast']['trenes_suprimidos'], key="trenes_suprimidos_cast")
        
        with tab6:
            st.subheader("Inglés")
            st.text_area("Baliza estaciones inicio", value=st.session_state.plataforma_generado['eng']['baliza_inicio'], key="baliza_inicio_eng")
            st.text_area("Baliza estaciones interior", value=st.session_state.plataforma_generado['eng']['baliza_interior'], key="baliza_interior_eng")
            st.text_area("Trenes detenidos", value=st.session_state.plataforma_generado['eng']['trenes_detenidos'], key="trenes_detenidos_eng")
            st.text_area("Trenes suprimidos", value=st.session_state.plataforma_generado['eng']['trenes_suprimidos'], key="trenes_suprimidos_eng")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección 6: Redes Sociales
    st.markdown('<div class="section-header">Sección 6. Redes Sociales</div>', unsafe_allow_html=True)
    
    redes_generado = st.form_submit_button("🤖 Generar IA Redes Sociales", use_container_width=True)
    if redes_generado:
        # Esta lógica se manejará después del submit
        pass
    
    if 'redes_generado' in st.session_state:
        st.markdown('<div class="ia-generated">', unsafe_allow_html=True)
        
        col_redes1, col_redes2, col_redes3 = st.columns(3)
        
        with col_redes1:
            st.subheader("Catalán")
            st.text_area("Mensaje CAT", value=st.session_state.redes_generado['cat']['mensaje'], key="mensaje_cat", height=100)
        
        with col_redes2:
            st.subheader("Castellano")
            st.text_area("Mensaje CAST", value=st.session_state.redes_generado['cast']['mensaje'], key="mensaje_cast", height=100)
        
        with col_redes3:
            st.subheader("Inglés")
            st.text_area("Mensaje ENG", value=st.session_state.redes_generado['eng']['mensaje'], key="mensaje_eng", height=100)
        
        st.markdown('</div>', unsafe_allow_html=True)

def crear_incidencia(sistema):
    """Formulario para crear nueva incidencia"""
    st.markdown('<div class="main-header">📝 Nueva Incidencia</div>', unsafe_allow_html=True)
    
    # Inicializar session_state para trenes afectados si no existe
    if 'trenes_afectados' not in st.session_state:
        st.session_state.trenes_afectados = []
    
    # Formulario principal
    with st.form("nueva_incidencia_form"):
        st.markdown('<div class="section-header">Sección 1. Incidencia</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
            tipo_incidencia = st.selectbox("Tipo de Incidencia *", sistema.tipos_incidencia)
        
        with col2:
            hora_inicio = st.time_input("Hora de inicio", value=datetime.now().time())
            repercusion = st.selectbox("Repercusión *", sistema.repercusiones)
        
        with col3:
            linea = st.selectbox("Línea *", sistema.lineas)
        
        # Mostrar información de la línea seleccionada
        if linea:
            estaciones_linea = sistema.obtener_estaciones_por_linea(linea)
            if estaciones_linea:
                with st.expander(f"Estaciones de la línea {linea} ({len(estaciones_linea)} estaciones)"):
                    for estacion in estaciones_linea:
                        st.write(f"• {estacion}")
        
        # Campos específicos según tipo de incidencia
        if tipo_incidencia == "Avería Infraestructura":
            todas_estaciones = sistema.obtener_todas_estaciones()
            dependencia = st.selectbox("Dependencia *", todas_estaciones)
        elif tipo_incidencia == "Avería Tren":
            numero_tren = st.text_input("Nº Tren (5 cifras) *", max_chars=5)
        elif tipo_incidencia in ["Orden público/Fuerza mayor", "Operaciones"]:
            col_opt1, col_opt2 = st.columns(2)
            with col_opt1:
                numero_tren_opcional = st.text_input("Nº Tren (opcional)", max_chars=5)
            with col_opt2:
                todas_estaciones = sistema.obtener_todas_estaciones()
                dependencia_opcional = st.selectbox("Dependencia (opcional)", [""] + todas_estaciones)
        
        # Afectación al territorio
        st.subheader("Afectación al territorio")
        
        # Si hay una línea seleccionada, mostrar solo estaciones de esa línea
        if linea:
            estaciones_disponibles = sistema.obtener_estaciones_por_linea(linea)
        else:
            estaciones_disponibles = sistema.obtener_todas_estaciones()
        
        col_est1, col_est2 = st.columns(2)
        with col_est1:
            estacion_a = st.selectbox("Estación A", estaciones_disponibles)
        with col_est2:
            estacion_b = st.selectbox("Estación B", estaciones_disponibles)
        
        descripcion_larga = st.text_area("Descripción larga *", height=100, placeholder="Describa detalladamente la incidencia...")
        prevision_resolucion = st.text_area("Previsión de resolución *", height=80, placeholder="Indique la previsión de cuándo se resolverá...")
        
        st.markdown('<div class="section-header">Sección 2. Relación con ADIF</div>', unsafe_allow_html=True)
        
        col_gifo, col_sitra = st.columns(2)
        with col_gifo:
            opciones_gifo = [f"GIFO-{i:03d}" for i in range(1, 11)]
            gifo_seleccionados = st.multiselect("GIFO", opciones_gifo)
        
        with col_sitra:
            sitra = st.text_input("SITRA")
        
        # Trenes afectados - fuera del form para permitir interacción
        st.subheader("Trenes afectados")
        
        # Mostrar trenes actuales
        for i, tren in enumerate(st.session_state.trenes_afectados):
            col_show1, col_show2, col_show3 = st.columns([2, 2, 1])
            with col_show1:
                st.markdown(f'<div class="tren-item">Tren: {tren["tren"]}</div>', unsafe_allow_html=True)
            with col_show2:
                st.markdown(f'<div class="tren-item">Retraso: {tren["retraso"]} min</div>', unsafe_allow_html=True)
            with col_show3:
                # Usar form_submit_button para eliminar
                eliminar = st.form_submit_button("🗑️", key=f"eliminar_{i}")
                if eliminar:
                    st.session_state.trenes_afectados.pop(i)
                    st.rerun()
        
        # Preparar datos para las secciones de IA
        incidencia_data = {
            'tipo': tipo_incidencia,
            'repercusion': repercusion,
            'linea': linea,
            'estacion_a': estacion_a,
            'estacion_b': estacion_b,
            'descripcion': descripcion_larga
        }
        
        # Mostrar secciones de comunicaciones con IA
        mostrar_seccion_comunicaciones()
        
        # Botón de submit principal
        col_submit1, col_submit2, col_submit3 = st.columns(3)
        with col_submit2:
            submitted = st.form_submit_button("💾 Guardar Incidencia", use_container_width=True)
        
        # Procesar después del submit
        if submitted:
            if not descripcion_larga or not prevision_resolucion:
                st.error("Por favor, complete todos los campos obligatorios (*)")
            else:
                # Crear objeto incidencia
                nueva_incidencia = {
                    'tipo': tipo_incidencia,
                    'fecha_inicio': fecha_inicio.strftime("%Y-%m-%d"),
                    'hora_inicio': hora_inicio.strftime("%H:%M"),
                    'repercusion': repercusion,
                    'linea': linea,
                    'estacion_a': estacion_a,
                    'estacion_b': estacion_b,
                    'descripcion': descripcion_larga,
                    'prevision': prevision_resolucion,
                    'estado': 'Activa',
                    'gifo': gifo_seleccionados,
                    'sitra': sitra,
                    'trenes_afectados': st.session_state.trenes_afectados.copy()
                }
                
                # Agregar campos específicos según tipo
                if tipo_incidencia == "Avería Infraestructura":
                    nueva_incidencia['dependencia'] = dependencia
                elif tipo_incidencia == "Avería Tren":
                    nueva_incidencia['numero_tren'] = numero_tren
                elif tipo_incidencia in ["Orden público/Fuerza mayor", "Operaciones"]:
                    if numero_tren_opcional:
                        nueva_incidencia['numero_tren'] = numero_tren_opcional
                    if dependencia_opcional:
                        nueva_incidencia['dependencia'] = dependencia_opcional
                
                # Guardar incidencia
                id_incidencia = sistema.agregar_incidencia(nueva_incidencia)
                st.success(f"✅ Incidencia {id_incidencia} creada correctamente")
                
                # Limpiar formulario y estados de IA
                st.session_state.trenes_afectados = []
                if 'copernico_generado' in st.session_state:
                    del st.session_state.copernico_generado
                if 'sia_generado' in st.session_state:
                    del st.session_state.sia_generado
                if 'plataforma_generado' in st.session_state:
                    del st.session_state.plataforma_generado
                if 'redes_generado' in st.session_state:
                    del st.session_state.redes_generado
                
                st.session_state.crear_incidencia = False
                st.rerun()
    
    # Formulario separado para añadir trenes (fuera del form principal)
    st.markdown("---")
    st.subheader("Añadir Tren Afectado")
    
    with st.form("añadir_tren_form"):
        col_tren1, col_tren2, col_tren3 = st.columns([2, 2, 1])
        with col_tren1:
            nuevo_tren = st.text_input("Nº Tren", key="nuevo_tren")
        with col_tren2:
            nuevo_retraso = st.number_input("Retraso (minutos)", min_value=0, key="nuevo_retraso")
        with col_tren3:
            añadir_tren = st.form_submit_button("➕ Añadir", use_container_width=True)
        
        if añadir_tren and nuevo_tren:
            st.session_state.trenes_afectados.append({
                'tren': nuevo_tren,
                'retraso': nuevo_retraso
            })
            st.rerun()

def main():
    """Función principal de la aplicación"""
    
    # Inicializar sistema en session_state si no existe
    if 'sistema' not in st.session_state:
        st.session_state.sistema = SistemaIncidencias()
    
    sistema = st.session_state.sistema
    
    # Mostrar información del dataset cargado
    with st.sidebar:
        st.header("📊 Datos del Sistema")
        st.write(f"**Líneas cargadas:** {len(sistema.lineas)}")
        st.write(f"**Estaciones cargadas:** {len(sistema.estaciones_df)}")
        st.write(f"**Incidencias activas:** {len(sistema.obtener_incidencias_activas())}")
        
        if st.button("🔄 Recargar Estaciones"):
            sistema.estaciones_df, sistema.lineas = sistema.cargar_estaciones()
            st.rerun()
    
    # Navegación
    if st.session_state.get('crear_incidencia', False):
        crear_incidencia(sistema)
        
        # Botón para volver al dashboard
        if st.button("← Volver al Dashboard"):
            st.session_state.crear_incidencia = False
            st.rerun()
    else:
        mostrar_dashboard(sistema)

if __name__ == "__main__":
    main()
