import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

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
# create reusable card component


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

                        # Aquí puedes agregar componentes adicionales para el Sidebar
                        dbc.Checkbox(id='checkbox1', label='Opción 1'),
                        dbc.Checkbox(id='checkbox2', label='Opción 2'),
                        dbc.Checkbox(id='checkbox3', label='Opción 3'),
                        # ...otros componentes del Sidebar...
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
                                        figure={}, id="score-distribution-histogram")
                                ],
                            )
                        ),
                    ],
                    width=9  # Ancho de la sección de gráficos (70%)
                ),
            ]
        )
    ],
    fluid=True,  # Utiliza el 100% del ancho de la página
    style={'background': '#FBFBFB', 'height': '100vh'}
)


@callback(
    Output("score-distribution-histogram", "figure"),
    Input("score-distribution-radios", "value")
)
def update_histogram(value):
    figure = px.histogram(df, x=value, color_discrete_sequence=['#0a9396'])
    return figure


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
