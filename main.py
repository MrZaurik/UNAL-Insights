import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash

from dash import Dash, html, dcc, callback, Output, Input

# Cargar los datos
df = pd.read_csv('dataset.csv')
promediosCalificaciones = df['PAPA'].mean()
promediosPuntajesAdmision = df['PUNTAJE_ADMISION'].mean()
promediosPeriodosCursados = df['NUMERO_MATRICULAS'].mean()
promediosEstrado = df['ESTRATO'].mean()

# Crear la aplicación
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
paletaColores = ['#0a9396', '#94d2bd', '#e9d8a6',
                 '#ee9b00', '#ca6702', '#bb3e03', '#ae2012']

# Get the card component


def get_card_component(title, data):
    component = dbc.Col(
        dbc.Card(
            dbc.CardBody([
                html.H4(title),
                html.H4(data)
            ]),
            color="dark",
            outline=True,
            className='text-dark',
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    )
    return component


# Layout con Sidebar
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            children='DataUNAL', style={'textAlign': 'center', 'padding-bottom': '20px'}),
                        html.P('El siguiente dashboard muestra información descriptiva acerca de la población universitaria de la Universidad Nacional de Colombia Sede de La Paz. Utiliza el menú lateral para navegar entre las diferentes opciones y parámetros de visualización. '),
                        dcc.Markdown('''
                                     **Autores:** Juan G. Saurith M., Jose Miguel Gutierrez Mieles, Raúl Rafael Romero Arias, Marlon Felipe Durán Celis	
                                     '''),
                        html.Hr(),

                        # Botones para cambiar entre "Main" y "Custom"
                        html.Div(
                            [
                                dbc.Button("Main", id="btn-main",
                                           color="primary"),
                                dbc.Button(
                                    "Custom", id="btn-custom", color="info"),
                            ],
                            style={
                                'display': 'flex', 'justify-content': 'center', 'margin': '20px 0', 'gap': '10px'}
                        ),

                        # Nuevo componente para mostrar el texto o los checkboxes
                        html.Div(id='content-display')
                    ],
                    width=3,  # Ancho del Sidebar (30%)
                    style={'background-color': '#EEE', 'padding': '20px',
                           'border-right': '1px solid #dee2e6', 'height': '100vh'},
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                get_card_component(
                                    'Total Students', '{:,}'.format(len(df.index))),
                                get_card_component('Avg PAPA', str(
                                    promediosCalificaciones)),
                                get_card_component('Avg Admision Score', str(
                                    promediosPuntajesAdmision)),
                                get_card_component(
                                    'Avg Estrato', str(promediosEstrado)),
                            ]
                        ),
                        dbc.Row(
                            dbc.Col(
                                [
                                    html.H4("Score Distribution"),
                                    html.Div(
                                        dbc.RadioItems(
                                            id="score-distribution-radios",
                                            className="btn-group",
                                            inputClassName="btn-check",
                                            labelClassName="btn btn-outline-dark",
                                            labelCheckedClassName="active",
                                            options=[
                                                {'label': 'Periodos Cursados',
                                                    'value': 'NUMERO_MATRICULAS'},
                                                {'label': 'Puntajes de Admisión',
                                                    'value': 'PUNTAJE_ADMISION'},
                                                {'label': 'PAPA', 'value': 'PAPA'}
                                            ],
                                            value='PAPA',
                                        ),
                                        className="radio-group",
                                        style={'margin-top': '20px'}
                                    ),
                                    dcc.Graph(
                                        figure={}, id="score-distribution-histogram"),
                                ],
                            )
                        ),

                        # Nuevos gráficos para el panel de visualizaciones
                        dbc.Row(
                            [
                                dbc.Col(
                                    dcc.Graph(
                                        figure={}, id="violin-estrato-papa")
                                ),
                                dbc.Col(
                                    dcc.Graph(
                                        figure={}, id="pie-chart-genero")
                                ),
                            ],
                            style={'margin-top': '20px'}
                        ),


                    ],
                    width=9,  # Ancho de la sección de gráficos (70%)
                    style={'padding': '40px'}
                ),
            ]
        )
    ],
    fluid=True,  # Utiliza el 100% del ancho de la página
    style={'background': '#FBFBFB', 'height': '100vh'}
)

# Callback para cambiar entre las secciones "Main" y "Custom"


@app.callback(
    Output("score-distribution-histogram", "figure"),
    Output("content-display", "children"),
    Output("btn-main", "color"),
    Output("btn-custom", "color"),
    Input("btn-main", "n_clicks"),
    Input("btn-custom", "n_clicks")
)
def update_section(btn_main_clicks, btn_custom_clicks):
    ctx = dash.callback_context
    if not ctx.triggered_id:
        button_id = "btn-main"
    else:
        button_id = ctx.triggered_id

    if button_id == "btn-main":
        # Lógica para la sección "Main"
        figure = px.scatter()  # Figura vacía para "Main"
        content = html.P("Texto aleatorio para la sección 'Main'")
        btn_main_color = "primary"
        btn_custom_color = "info"
    else:
        # Lógica para la sección "Custom"
        figure = px.histogram(
            df, x='PAPA', color_discrete_sequence=['#0a9396'])

        # Nuevo contenido con checkboxes para la sección 'Custom'
        content = html.Div(
            [
                html.H3("Programa Curricular"),
                dbc.Row(
                    [
                        dbc.Col(dbc.Checkbox(
                            label='Biología', id='checkbox-1')),
                        dbc.Col(dbc.Checkbox(
                            label='Estadística', id='checkbox-2')),
                        dbc.Col(dbc.Checkbox(
                            label='Ing. Mecatrónica', id='checkbox-3')),
                        dbc.Col(dbc.Checkbox(
                            label='Ing. Biológica', id='checkbox-4')),
                        dbc.Col(dbc.Checkbox(
                            label='Geografía', id='checkbox-5')),
                        dbc.Col(dbc.Checkbox(
                            label='Gestión Cultural', id='checkbox-6')),
                    ],
                    style={'margin-bottom': '10px'}
                ),

                html.H3("Género"),
                dcc.Dropdown(
                    id='dropdown-genero',
                    options=[
                        {'label': 'Hombres', 'value': 'hombres'},
                        {'label': 'Mujeres', 'value': 'mujeres'},
                    ],
                    multi=True,
                    value=[]
                ),

                html.H3("Periodo de Ingreso"),
                dcc.Dropdown(
                    id='dropdown-periodo-ingreso',
                    options=[
                        {'label': '2019-2S', 'value': 'opcion1'},
                        {'label': '2020-1S', 'value': 'opcion2'},
                        {'label': '2020-2S', 'value': 'opcion3'},
                        {'label': '2021-1S', 'value': 'opcion4'},
                        {'label': '2021-2S', 'value': 'opcion5'},
                        {'label': '2022-1S', 'value': 'opcion6'},
                        {'label': '2022-2S', 'value': 'opcion7'},
                        {'label': '2023-1S', 'value': 'opcion8'},
                        {'label': '2023-2S', 'value': 'opcion9'},
                        {'label': '2024-1S', 'value': 'opcion10'}
                    ],
                    multi=True,
                    value=['opcion10']
                ),
            ],
            style={'padding': '20px'}
        )

        btn_main_color = "info"
        btn_custom_color = "primary"

    return figure, content, btn_main_color, btn_custom_color

# Callback para el gráfico de Violin entre Estrato Socioeconómico y PAPA


@app.callback(
    Output("violin-estrato-papa", "figure"),
    Input("btn-custom", "n_clicks")
)
def update_violin_estrato_papa(btn_custom_clicks):
    if btn_custom_clicks:
        figure = px.violin(
            df, y="PAPA", x="ESTRATO",
            color_discrete_sequence=['#0a9396'],
            box=True, points="all"
        )
        figure.update_layout(
            title="Violin Plot: Estrato Socioeconómico vs PAPA",
            xaxis_title="Estrato Socioeconómico",
            yaxis_title="PAPA"
        )
        return figure
    else:
        return px.scatter()

# Callback para el gráfico de Diagrama Circular con información de género


@app.callback(
    Output("pie-chart-genero", "figure"),
    Input("btn-custom", "n_clicks")
)
def update_pie_chart_genero(btn_custom_clicks):
    if btn_custom_clicks:
        figure = px.pie(
            df, names='GENERO', title='Distribución de Género')
        return figure
    else:
        return px.scatter()


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
