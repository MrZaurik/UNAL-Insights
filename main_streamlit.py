import streamlit as st
import pandas as pd
import plotly.express as px

px.defaults.template = 'seaborn'


# Cargar los datos
df = pd.read_csv('dataset.csv')
promediosCalificaciones = df['PAPA'].mean()
promediosPuntajesAdmision = df['PUNTAJE_ADMISION'].mean()
promediosEstrado = df['ESTRATO'].mean()

# Barra lateral
st.sidebar.title('UNAL Insights')
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
    st.sidebar.markdown('UNAL Insights es una propuesta desarrollada en el marco de la asignatura _Programación en Lenguajes Estadísticos_ con el objetivo principal de hacer clara algunas de las características de la población estudiantil de la Universidad Nacional de Colombia Sede de La Paz. El dashboard cuenta con dos secciones: **Main** y **Custom**. En la sección **Main** se presenta información descriptiva de la población estudiantil, mientras que en la sección **Custom** se permite al usuario interactuar con los datos y visualizar información específica según sus necesidades. Para cambiar de sección, haga clic en el botón **Cambiar Sección** en la barra lateral.')
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

        df_grouped = df.groupby(
            ['PLAN', 'GENERO']).size().reset_index(name='Count')

        # Gráfico de barras por programa
        st.plotly_chart(
            px.bar(
                df_grouped,
                x='PLAN',
                y='Count',
                title='Cantidad de Estudiantes por Programa y Género',
                color='GENERO',
                barmode='group'
            ))

        # Gráfico de barras por género
        df_grouped_gender = df.groupby(
            'GENERO').size().reset_index(name='Count')
        st.plotly_chart(
            px.bar(
                df_grouped_gender,
                x='GENERO',
                y='Count',
                title='Cantidad de Estudiantes por Género'
            )
        )

        # Gráfico de barras por estrato
        st.plotly_chart(
            px.histogram(df, x='ESTRATO', title='Cantidad de Estudiantes por Estrato'))

        # Gráfico de barras por convocatoria
        df_grouped_convocatoria = df.groupby(
            'CONVOCATORIA').size().reset_index(name='Count')
        st.plotly_chart(
            px.bar(df_grouped_convocatoria, x='CONVOCATORIA', y='Count', title='Cantidad de Estudiantes por Convocatoria'))

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
        df_provincia = df.groupby(
            ['PROVINCIA_NACIMIENTO', 'GENERO']).size().reset_index(name='Count')
        st.plotly_chart(
            px.bar(df_provincia, x='PROVINCIA_NACIMIENTO', y='Count', title='Cantidad de Estudiantes por Provincia de Nacimiento', color="GENERO", barmode="group"))

# Sección "Custom"
elif current_section == 'Custom':
    st.title('Custom')

    # Filtros y controles interactivos en el aside
    programas = st.sidebar.multiselect(
        'Programas Curriculares', df['PLAN'].unique())
    generos = st.sidebar.multiselect('Género', df['GENERO'].unique())
    periodos_ingreso = st.sidebar.multiselect(
        'Periodo de Ingreso', ['2019-2S', '2020-1S', '2020-2S', '2021-1S', '2021-2S', '2022-1S', '2022-2S', '2023-1S', '2023-2S', '2024-1S'])

    # Filtrar el DataFrame según las selecciones del usuario
    filtered_df = df[df['PLAN'].isin(programas) & df['GENERO'].isin(
        generos) & df['CONVOCATORIA'].isin(periodos_ingreso)]

    # Visualizaciones basadas en las selecciones del usuario
    if not filtered_df.empty:

        # Histograma de Edades por Programa, Género y Periodo de Ingreso
        st.plotly_chart(px.histogram(filtered_df, x='EDAD', color='GENERO', facet_col='PLAN', facet_row='CONVOCATORIA', title='Histograma de Edades por Programa, Género y Periodo de Ingreso')
                        )

        # Histograma de Promedios por Plan y Genero Seleccionado
        st.plotly_chart(px.histogram(filtered_df, x='PAPA', color='GENERO', facet_col='PLAN', title='Histograma de Promedios por Plan y Genero Seleccionado')
                        )

        # Dispersión de Puntajes de Admisión por Edad, Genero y Programa (Tamaño de Punto por Estrato Socioeconómico)
        st.plotly_chart(px.scatter(filtered_df, x='EDAD', y='PUNTAJE_ADMISION', color='GENERO', size='ESTRATO', facet_col='PLAN', title='Dispersión de Puntajes de Admisión por Edad, Genero y Programa (Estrato Socioeconómico)')
                        )

        # Gráfico de Violín de Puntaje de Admisión por Carrera y Género
        st.plotly_chart(
            px.violin(filtered_df, y="PUNTAJE_ADMISION", x="PLAN",
                      color="GENERO", title='Puntaje de Admisión por Carrera y Género')
        )

        # Grafico de Caja de Bigotes de PAPA por Carrera y Género
        st.plotly_chart(
            px.box(filtered_df, x='PLAN', y='PAPA', color='GENERO',
                   title='PAPA por Carrera y Género')
        )

    else:
        st.warning('No hay datos que coincidan con las selecciones.')

# Agregar aquí cualquier otra sección o visualización según tus necesidades
