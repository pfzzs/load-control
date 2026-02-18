import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# =========================
# DADOS
# =========================
df = pd.read_csv("treinos.csv")
df["start_time"] = pd.to_datetime(df["start_time"], format="%d %b %Y, %H:%M")
df = df[df["set_type"] != "warmup"]

muscle_map = {
    "Squat (Barbell)": "Quadríceps",
    "Leg Extension (Machine)": "Quadríceps",
    "Seated Leg Curl (Machine)": "Posterior de Coxa",
    "Lying Leg Curl (Machine)": "Posterior de Coxa",
    "Straight Leg Deadlift": "Posterior de Coxa",
    "Standing Calf Raise (Machine)": "Panturrilha",
    "Calf Extension (Machine)": "Panturrilha",
    "Chest Press (Machine)": "Peito",
    "Chest Fly (Machine)": "Peito",
    "Lat Pulldown - Close Grip (Cable)": "Costas",
    "T Bar Row": "Costas",
    "Iso-Lateral Row (Machine)": "Costas",
    "Lateral Raise (Machine)": "Ombro Lateral",
    "Crunch (Machine)": "Abdômen",
}

gif_map = {
    "Squat (Barbell)": "/assets/videos/squat_barbell.mp4",
    "Seated Leg Curl (Machine)": "/assets/videos/Lever-Seated-Leg-Curl.mp4",
}

df["muscle"] = df["exercise_title"].map(muscle_map)

app = Dash(__name__)

# =========================
# ESTILOS
# =========================
card_style = {
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.06)",
    "textAlign": "center",
    "flex": "1",
    "minWidth": "160px"
}

gif_card_style = {
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "textAlign": "center",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.06)",
    "flexBasis": "280px",
    "flexGrow": "0"
}

graph_style = {
    "backgroundColor": "white",
    "padding": "10px",
    "borderRadius": "14px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.06)",
    "flex": "1",
    "minWidth": "300px"
}

# =========================
# LAYOUT
# =========================
app.layout = html.Div([

    html.H1(
        "Controle de cargas",
        style={
            "textAlign": "center",
            "margin": "10px 0 20px 0",
            "fontSize": "clamp(22px, 2.5vw, 32px)"
        }
    ),

    # TOPO
    html.Div([

        # EXECUÇÃO
        html.Div([
            html.H4("Execução"),
            html.Video(
                id="exercise-gif",
                autoPlay=True,
                muted=True,
                loop=True,
                style={
                    "width": "100%",
                    "maxHeight": "200px",
                    "objectFit": "contain"
                }
            )
        ], style=gif_card_style),

        # COLUNA DIREITA
        html.Div([

            # FILTROS
            html.Div([
                dcc.Dropdown(
                    id="exercise-dropdown",
                    options=[{"label": ex, "value": ex} for ex in df["exercise_title"].unique()],
                    value=df["exercise_title"].unique()[0],
                    style={"flex": "1"}
                ),
                dcc.DatePickerRange(
                    id="date-picker",
                    start_date=df["start_time"].min(),
                    end_date=df["start_time"].max(),
                    style={"flex": "1"}
                )
            ], style={
                "display": "flex",
                "gap": "10px",
                "flexWrap": "wrap",
                "marginBottom": "10px"
            }),

            # CARDS
            html.Div([
                html.Div([
                    html.H4("Total de Séries"),
                    html.H2(id="total-series")
                ], style=card_style),

                html.Div([
                    html.H4("Máx. Repetições"),
                    html.H2(id="max-reps")
                ], style=card_style),
            ], style={
                "display": "flex",
                "gap": "10px",
                "flexWrap": "wrap"
            })

        ], style={
            "flex": "1",
            "display": "flex",
            "flexDirection": "column"
        })

    ], style={
        "display": "flex",
        "gap": "15px",
        "flexWrap": "wrap",
        "marginBottom": "15px"
    }),

    # GRÁFICOS
    html.Div([
        html.Div(
            dcc.Graph(
                id="progress-graph",
                config={"displayModeBar": False},
                style={"height": "38vh"}
            ),
            style=graph_style
        ),

        html.Div(
            dcc.Graph(
                id="muscle-graph",
                config={"displayModeBar": False},
                style={"height": "38vh"}
            ),
            style=graph_style
        ),
    ], style={
        "display": "flex",
        "gap": "15px",
        "flexWrap": "wrap"
    })

], style={
    "backgroundColor": "#f5f7fb",
    "minHeight": "100vh",
    "padding": "10px"
})

# =========================
# CALLBACK
# =========================
@app.callback(
    Output("progress-graph", "figure"),
    Output("muscle-graph", "figure"),
    Output("total-series", "children"),
    Output("max-reps", "children"),
    Output("exercise-gif", "src"),
    Input("exercise-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_graphs(exercise, start_date, end_date):

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    filtered = df[
        (df["start_time"] >= start_date) &
        (df["start_time"] <= end_date)
    ]

    df_ex = filtered[filtered["exercise_title"] == exercise]

    total_series = len(df_ex)
    max_reps = df_ex["reps"].max() if not df_ex.empty else 0
    gif_url = gif_map.get(exercise, "")

    # Evolução
    grouped = (
        df_ex.groupby("start_time")["weight_kg"]
        .max()
        .reset_index()
    )

    fig_progress = px.line(
        grouped,
        x="start_time",
        y="weight_kg",
        markers=True,
        title="Evolução de Carga"
    )

    fig_progress.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Frequência muscular
    muscle_freq = (
        filtered.dropna(subset=["muscle"])
        .groupby("muscle")["start_time"]
        .nunique()
        .reset_index(name="frequencia")
    )

    fig_muscle = px.pie(
        muscle_freq,
        names="muscle",
        values="frequencia",
        hole=0.5,
        title="Frequência Muscular"
    )

    fig_muscle.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig_progress, fig_muscle, total_series, max_reps, gif_url


if __name__ == "__main__":
    app.run(debug=True)
