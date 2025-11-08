# dashboard.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Datos de ejemplo (puedes reemplazarlos por tus propios datos)
df = px.data.gapminder()

# Inicializar la app Dash
app = dash.Dash(__name__)
app.title = "Tablero Interactivo con Dash"

# Layout de la app
app.layout = html.Div([
    html.H1("🌍 Dashboard Interactivo - Gapminder", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Selecciona un continente:"),
        dcc.Dropdown(
            id='dropdown-continent',
            options=[{'label': c, 'value': c} for c in df['continent'].unique()],
            value='Europe',
            clearable=False,
            style={'width': '50%'}
        )
    ], style={'textAlign': 'center', 'padding': '10px'}),

    dcc.Graph(id='grafico-vida'),

    html.Div([
        html.Label("Selecciona un año:"),
        dcc.Slider(
            id='slider-year',
            min=df['year'].min(),
            max=df['year'].max(),
            step=5,
            marks={str(year): str(year) for year in df['year'].unique()},
            value=df['year'].min()
        )
    ], style={'padding': '30px'}),

    dcc.Graph(id='grafico-poblacion')
])

# Callbacks para interactividad
@app.callback(
    Output('grafico-vida', 'figure'),
    Input('dropdown-continent', 'value')
)
def actualizar_grafico_continente(continent):
    dff = df[df['continent'] == continent]
    fig = px.line(dff, x='year', y='lifeExp', color='country',
                  title=f'Esperanza de vida en {continent}')
    return fig

@app.callback(
    Output('grafico-poblacion', 'figure'),
    Input('slider-year', 'value')
)
def actualizar_grafico_anio(year):
    dff = df[df['year'] == year]
    fig = px.scatter(dff, x='gdpPercap', y='lifeExp',
                     size='pop', color='continent', hover_name='country',
                     log_x=True, size_max=60,
                     title=f'Distribución de países en el año {year}')
    return fig

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
