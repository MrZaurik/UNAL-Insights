import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar los datos
df = pd.read_csv('dataset.csv')
promediosCalificaciones = df['PAPA'].mean()
promediosPuntajesAdmision = df['PUNTAJE_ADMISION'].mean()
promediosEstrado = df['ESTRATO'].mean()

# Barra lateral
st.sidebar.title('DataUNAL')
btn_switch_section = st.sidebar.button('Cambiar Sección')
st.sidebar.markdown(
    '**Autores:** Juan G. Saurith M., Jose Miguel Gutierrez Mieles, Raúl Rafael Romero Arias, Marlon Felipe Durán Celis')

# Verificar el estado actual de la sección
current_section = st.session_state.get('current_section', 'Main')

# Lógica para cambiar de sección
if btn_switch_section:
    current_section = 'Custom' if current_section == 'Main' else 'Main'

# Guardar el estado actual de la sección en la sesión
st.session_state['current_section'] = current_section

# Sección "Main"
if current_section == 'Main':
    st.markdown("""
        <style>
            .st-emotion-cache-uf99v8 {
                align-items: start;
                margin-left: 7.5rem
            }
        </style>
    """, unsafe_allow_html=True)

    st.title('DataUNAL')
    st.write('El siguiente dashboard muestra información descriptiva acerca de la población universitaria de la Universidad Nacional de Colombia Sede de La Paz.')

    # Información resumida en dos columnas
    col = st.columns((2, 2), gap='large')

    # Columna 1: Información almacenada en variables
    with col[0]:
        st.subheader('Promedios')
        st.write(f'Numero de Estudiantes: {df.shape[0]}')
        st.write(f'Promedio PAPA: {promediosCalificaciones:.2f}')
        st.write(
            f'Promedio Puntajes de Admisión: {promediosPuntajesAdmision:.2f}')
        st.write(f'Promedio Estrato Socioeconómico: {promediosEstrado:.2f}')

    # Columna 2: Visualizaciones
    with col[1]:
        st.subheader('Visualizaciones')

        # Gráfico de barras por programa
        st.plotly_chart(
            px.bar(df, x='PLAN', title='Cantidad de Estudiantes por Programa', color="GENERO", barmode="group"))

        # Gráfico de barras por género
        st.plotly_chart(
            px.bar(df, x='GENERO', title='Cantidad de Estudiantes por Género'))

        # Gráfico de barras por estrato
        # st.plotly_chart(
        # px.histogram(df, x='ESTRATO', title='Cantidad de Estudiantes por Estrato'))

        # Gráfico de barras por convocatoria
        # st.plotly_chart(
        # px.bar(df, x='CONVOCATORIA', title='Cantidad de Estudiantes por Convocatoria'))

        # Gráfico histograma de Edad
        st.plotly_chart(
            px.histogram(df, x='EDAD', title='Histograma de Edades'))

        # Grafico caja de bigotes de PAPA por Carrera
        st.plotly_chart(
            px.box(df, x='PLAN', y='PAPA', title='PAPA por Programa'))

        # Grafico de Violín de Puntaje de Admisión por Carrera
        st.plotly_chart(
            px.violin(df, y="PUNTAJE_ADMISION", x="PLAN", title='Puntaje de Admisión'))

        # Grafico de Paster para Caracteristicas Especiales (víctimas, discapacidad, etc)
        victimasConflicto = df[df['VICTIMAS_DEL_CONFLICTO'] == 'SI'].shape[0]
        discapacidad = df[df['DISCAPACIDAD'] != 'NO'].shape[0]
        estudiantesExceptos = df.shape[0] - (victimasConflicto + discapacidad)
        st.plotly_chart(
            px.pie(names=['Victimas del Conflicto', 'Discapacidad', 'Estudiantes Exceptos'], values=[
                   victimasConflicto, discapacidad, estudiantesExceptos], title='Caracteristicas Sociodemograficas Especiales', hole=0.4)
        )

        # Gráfico de Barras Apiladas para Provincias de Nacimiento:
        st.plotly_chart(
            px.bar(df, x='PROVINCIA_NACIMIENTO', title='Cantidad de Estudiantes por Provincia de Nacimiento', color="GENERO", barmode="group")) 

# Sección "Custom"
elif current_section == 'Custom':
    st.title('Custom')

    # Filtros y controles interactivos en el aside
    programas = st.sidebar.multiselect(
        'Programas Curriculares', df['PLAN'].unique())
    generos = st.sidebar.multiselect('Género', df['GENERO'].unique())
    periodos_ingreso = st.sidebar.multiselect(
        'Periodo de Ingreso', df['CONVOCATORIA'].unique())

    # Filtrar el DataFrame según las selecciones del usuario
    filtered_df = df[df['PLAN'].isin(programas) & df['GENERO'].isin(
        generos) & df['CONVOCATORIA'].isin(periodos_ingreso)]

    # Visualizaciones basadas en las selecciones del usuario
    if not filtered_df.empty:
        # Histograma, gráfico de violín, etc.
        st.plotly_chart(px.histogram(filtered_df, x='PAPA',
                        color_discrete_sequence=['#0a9396']))
        st.plotly_chart(px.violin(filtered_df, y="PAPA", x="ESTRATO",
                        color_discrete_sequence=['#0a9396'], box=True, points="all"))
    else:
        st.warning('No hay datos que coincidan con las selecciones.')

# Agregar aquí cualquier otra sección o visualización según tus necesidades
