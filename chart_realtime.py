"""
chart_realtime.py
-----------------
Gráfico EN VIVO del precio bid en el navegador, usando Dash (Plotly).

Cómo encaja con main_realtime.py:
  1. main_realtime arranca el dashboard con start_dashboard(symbol).
  2. Cada vez que el WebSocket recibe un quote, llama a add_bid(timestamp, bid).
  3. El navegador se refresca solo (cada segundo) y dibuja los últimos bids.

El servidor web corre en un hilo aparte (daemon) para no bloquear el stream.
"""

from collections import deque
from threading import Thread
import webbrowser

from dash import Dash, dcc, html, Output, Input
import plotly.graph_objects as go

# Buffer compartido de puntos (timestamp, bid). maxlen limita la memoria.
# deque.append es thread-safe en CPython, así el hilo del stream y el del
# servidor web pueden usarlo sin candados explícitos.
_BIDS = deque(maxlen=2000)
_SYMBOL = "—"


def add_bid(timestamp, bid):
    """Lo llama main_realtime en cada quote recibido por el WebSocket."""
    _BIDS.append((timestamp, bid))


def _crear_app():
    app = Dash(__name__)

    app.layout = html.Div(
        style={
            "fontFamily": "sans-serif",
            "margin": "0",
            "padding": "20px",
            "minHeight": "100vh",
            "backgroundColor": "#0d1117",   # fondo dark night
            "color": "#c9d1d9",             # texto claro
            "boxSizing": "border-box",
        },
        children=[
            html.H2(id="titulo", style={"color": "#58a6ff"}),
            html.Div(id="ultimo", style={"fontSize": "20px", "marginBottom": "10px",
                                         "color": "#3fb950"}),
            # El gráfico ocupa casi toda la altura de la ventana.
            dcc.Graph(id="grafico", style={"height": "82vh"}),
            # Dispara el callback de refresco cada 1000 ms.
            dcc.Interval(id="tick", interval=1000, n_intervals=0),
        ],
    )

    @app.callback(
        Output("titulo", "children"),
        Output("ultimo", "children"),
        Output("grafico", "figure"),
        Input("tick", "n_intervals"),
    )
    def _actualizar(_):
        datos = list(_BIDS)  # snapshot del buffer
        titulo = f"📈 Bid en tiempo real — {_SYMBOL}"

        if not datos:
            fig_vacia = go.Figure()
            fig_vacia.update_layout(template="plotly_dark",
                                    paper_bgcolor="#0d1117", plot_bgcolor="#0d1117")
            return titulo, "Esperando datos del WebSocket…", fig_vacia

        tiempos = [t for t, _ in datos]
        precios = [b for _, b in datos]

        fig = go.Figure(
            go.Scatter(x=tiempos, y=precios, mode="lines", name="bid",
                       line=dict(color="#58a6ff", width=2))
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            xaxis_title="Hora",
            yaxis_title="Precio bid",
            margin=dict(l=40, r=20, t=20, b=40),
            uirevision="keep",  # no resetea el zoom en cada refresco
        )
        return titulo, f"Último bid: {precios[-1]}", fig

    return app


def start_dashboard(symbol, host="127.0.0.1", port=8050, abrir_navegador=True):
    """Arranca el servidor web en un hilo aparte y abre el navegador."""
    global _SYMBOL
    _SYMBOL = symbol

    app = _crear_app()

    def _run():
        # use_reloader=False es obligatorio al correr fuera del hilo principal.
        app.run(host=host, port=port, debug=False, use_reloader=False)

    Thread(target=_run, daemon=True).start()

    url = f"http://{host}:{port}"
    print(f"🌐 Dashboard en vivo: {url}")
    if abrir_navegador:
        webbrowser.open(url)
