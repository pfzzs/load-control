from pathlib import Path

import pandas as pd
from dash import Dash, dash_table, dcc, html, Input, Output
import plotly.express as px

# =========================
# DADOS
# =========================
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_csv(BASE_DIR / "treinos.csv")


def parse_dates(col):
    # Formato padrão do export do Hevy; se o export vier em outro formato, tenta inferir
    try:
        return pd.to_datetime(col, format="%d %b %Y, %H:%M")
    except ValueError:
        return pd.to_datetime(col, dayfirst=True, format="mixed")


df["start_time"] = parse_dates(df["start_time"])
df = df[df["set_type"] != "warmup"]

muscle_map = {
    "Squat (Barbell)": "Quadríceps",
    "Squat (Smith Machine)": "Quadríceps",
    "Hack Squat (Machine)": "Quadríceps",
    "Leg Extension (Machine)": "Quadríceps",
    "Extensora Unilateral": "Quadríceps",
    "Seated Leg Curl (Machine)": "Posterior de Coxa",
    "Lying Leg Curl (Machine)": "Posterior de Coxa",
    "Straight Leg Deadlift": "Posterior de Coxa",
    "Romanian Deadlift (Barbell)": "Posterior de Coxa",
    "Standing Calf Raise (Machine)": "Panturrilha",
    "Single Leg Standing Calf Raise (Machine)": "Panturrilha",
    "Calf Extension (Machine)": "Panturrilha",
    "Chest Press (Machine)": "Peito",
    "Incline Chest Press (Machine)": "Peito",
    "Decline Bench Press (Machine)": "Peito",
    "Incline Bench Press (Smith Machine)": "Peito",
    "Incline Bench Press (Dumbbell)": "Peito",
    "Chest Fly (Machine)": "Peito",
    "Cable Fly Crossovers": "Peito",
    "Low Cable Fly Crossovers": "Peito",
    "Chest Dip": "Peito",
    "Lat Pulldown (Machine)": "Costas",
    "Lat Pulldown (Cable)": "Costas",
    "Lat Pulldown - Close Grip (Cable)": "Costas",
    "Rope Straight Arm Pulldown": "Costas",
    "T Bar Row": "Costas",
    "Landmine Row": "Costas",
    "Iso-Lateral Row (Machine)": "Costas",
    "Iso-Lateral High Row (Machine)": "Costas",
    "Seated Row (Machine)": "Costas",
    "Seated Cable Row - Bar Grip": "Costas",
    "Seated Cable Row - V Grip (Cable)": "Costas",
    "Seated Cable Row - Bar Wide Grip": "Costas",
    "Remada Nêutra Unilateral": "Costas",
    "Dumbbell Row": "Costas",
    "Shoulder Press (Dumbbell)": "Ombro Anterior",
    "Shoulder Press (Machine Plates)": "Ombro Anterior",
    "Overhead Press (Smith Machine)": "Ombro Anterior",
    "Lateral Raise (Machine)": "Ombro Lateral",
    "Elevação Lateral Unilateral (cabo)": "Ombro Lateral",
    "Rear Delt Reverse Fly (Machine)": "Ombro Posterior",
    "Curcifixo Inverso": "Ombro Posterior",
    "Adução Posterior De Ombro Unilateral": "Ombro Posterior",
    "Adução deltóide posterior (unilateral)": "Ombro Posterior",
    "Bicep Curl (Barbell)": "Bíceps",
    "Bicep Curl (Machine)": "Bíceps",
    "Preacher Curl (Machine)": "Bíceps",
    "Hammer Curl (Cable)": "Bíceps",
    "Triceps Pushdown": "Tríceps",
    "Triceps Rope Pushdown": "Tríceps",
    "Triceps Extension (Machine)": "Tríceps",
    "Tríceps Francês": "Tríceps",
    "Tríceps Testa Polia": "Tríceps",
    "Crunch (Machine)": "Abdômen",
    "Crunch (Weighted)": "Abdômen",
    "Lying Leg Raise": "Abdômen",
    "Knee Raise Parallel Bars": "Abdômen",
}

gif_map = {
    "Squat (Barbell)": "/assets/videos/squat_barbell.mp4",
    "Seated Leg Curl (Machine)": "/assets/videos/Lever-Seated-Leg-Curl.mp4",
    "Chest Press (Machine)": "/assets/videos/Lever-Chest-Press.mp4",
    "Incline Chest Press (Machine)": "/assets/videos/Lever-Incline-Chest-Press.mp4",
    "Elevação Lateral Unilateral (cabo)": "/assets/videos/Cable-One-Arm-Lateral-Raise.mp4",
    "Leg Extension (Machine)": "/assets/videos/Lever-Leg-Extension.mp4",
    "Lying Leg Curl (Machine)": "/assets/videos/Lever-Lying-Leg-Curl.mp4",
    "Straight Leg Deadlift": "/assets/videos/Barbell-Straight-Leg-Deadlift.mp4",
    "Chest Fly (Machine)": "/assets/videos/Lever-Seated-Fly.mp4",
    "T Bar Row": "/assets/videos/Lever-T-bar-Row-plate-loaded.mp4",
    "Lat Pulldown (Machine)": "/assets/videos/Lever-Front-Pulldown.mp4",
    "Shoulder Press (Dumbbell)": "/assets/videos/Dumbbell-Seated-Shoulder-Press.mp4",
    "Lat Pulldown - Close Grip (Cable)": "/assets/videos/Cable-Bar-Lateral-Pulldown.mp4",
    "Bicep Curl (Barbell)": "/assets/videos/Barbell-Curl.mp4",
    "Triceps Pushdown": "/assets/videos/Cable-Pushdown.mp4",
    "Lat Pulldown (Cable)": "/assets/videos/Cable-Bar-Lateral-Pulldown.mp4",
    "Romanian Deadlift (Barbell)": "/assets/videos/Barbell-Romanian-Deadlift-female.mp4",
    "Single Leg Standing Calf Raise (Machine)": "/assets/videos/Lever-Standing-Calf-Raise.mp4",
    "Dumbbell Row": "/assets/videos/Dumbbell-Bent-Over-Row.mp4",
    "Rope Straight Arm Pulldown": "/assets/videos/Cable-Straight-Arm-Pulldown.mp4",
    "Seated Cable Row - Bar Grip": "/assets/videos/Cable-Low-Seated-Row.mp4",
    "Cable Fly Crossovers": "/assets/videos/Cable-Standing-Up-Straight-Crossovers.mp4",
    "Incline Bench Press (Smith Machine)": "/assets/videos/Smith-Incline-Bench-Press.mp4",
    "Adução Posterior De Ombro Unilateral": "/assets/videos/Lever-Seated-Reverse-Fly.mp4",
    "Tríceps Francês": "/assets/videos/Dumbbell-Standing-Triceps-Extension.mp4",
    "Preacher Curl (Machine)": "/assets/videos/Lever-Preacher-Curl.mp4",
    "Standing Calf Raise (Machine)": "/assets/videos/Lever-Standing-Calf-Raise.mp4",
    "Low Cable Fly Crossovers": "/assets/videos/Cable-Low-Fly.mp4",
    "Rear Delt Reverse Fly (Machine)": "/assets/videos/Lever-Seated-Reverse-Fly.mp4",
    "Hack Squat (Machine)": "/assets/videos/Sled-Hack-Squat.mp4",
    "Incline Bench Press (Dumbbell)": "/assets/videos/Dumbbell-Incline-Bench-Press.mp4",
    "Extensora Unilateral": "/assets/videos/Lever-Leg-Extension.mp4",
    "Landmine Row": "/assets/videos/Lever-T-bar-Row-plate-loaded.mp4",
    "Adução deltóide posterior (unilateral)": "/assets/videos/Lever-Seated-Reverse-Fly.mp4",
    "Seated Cable Row - V Grip (Cable)": "/assets/videos/Cable-Low-Seated-Row.mp4",
    "Chest Dip": "/assets/videos/Chest-Dip.mp4",
    "Curcifixo Inverso": "/assets/videos/Lever-Seated-Reverse-Fly.mp4",
    "Seated Cable Row - Bar Wide Grip": "/assets/videos/Cable-Seated-Wide-grip-Row.mp4",
    "Triceps Rope Pushdown": "/assets/videos/Cable-Pushdown.mp4",
}

df["muscle"] = df["exercise_title"].map(muscle_map)

# =========================
# MÉTRICAS (LOW VOLUME)
# =========================
EFFECTIVE_SET_TYPES = {"failure", "dropset"}  # séries que contam como estímulo efetivo
PROGRESS_TOLERANCE = 0.01                    # variação de até 1% no 1RM conta como "manteve"
STAGNATION_SESSIONS = 3                      # sessões sem PR para acender o alerta

df["weight_kg"] = df["weight_kg"].fillna(0)
df["reps"] = df["reps"].fillna(0)
# 1RM estimado (Epley). Exercícios sem carga (peso corporal) são comparados pelas repetições.
df["score"] = (df["weight_kg"] * (1 + df["reps"] / 30)).where(df["weight_kg"] > 0, df["reps"])


def top_sets(data):
    # Melhor série (maior 1RM estimado) de cada exercício em cada sessão
    idx = data.groupby(["exercise_title", "start_time"])["score"].idxmax()
    return data.loc[idx].sort_values("start_time")


def format_set(weight, reps):
    return f"{weight:g} kg × {reps:g}" if weight > 0 else f"{reps:g} reps"


def progression_status(scores):
    # Compara a melhor série da última sessão com a da sessão anterior
    if len(scores) < 2 or not scores[-2]:
        return "–"
    diff = (scores[-1] - scores[-2]) / scores[-2]
    if diff > PROGRESS_TOLERANCE:
        return "↑"
    if diff < -PROGRESS_TOLERANCE:
        return "↓"
    return "="


def sessions_since_pr(scores):
    return len(scores) - 1 - scores.index(max(scores))


def progression_table(data):
    rows = []
    for exercise, g in top_sets(data).groupby("exercise_title"):
        scores = g["score"].tolist()
        last = g.iloc[-1]
        rows.append({
            "exercicio": exercise,
            "ultima": last["start_time"].strftime("%d/%m/%Y"),
            "serie": format_set(last["weight_kg"], last["reps"]),
            "e1rm": round(float(last["score"]), 1) if last["weight_kg"] > 0 else None,
            "status": progression_status(scores),
            "sem_pr": sessions_since_pr(scores),
        })
    rows.sort(key=lambda r: (-r["sem_pr"], r["exercicio"]))
    return rows


app = Dash(__name__)
server = app.server  # usado pelo gunicorn: gunicorn dashboard:server

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
                    start_date=df["start_time"].min().date(),
                    end_date=df["start_time"].max().date(),
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
                    html.H4("Melhor Série (última)"),
                    html.H2(id="last-top-set")
                ], style=card_style),

                html.Div([
                    html.H4("1RM Estimado (máx.)"),
                    html.H2(id="best-e1rm")
                ], style=card_style),

                html.Div([
                    html.H4("Sessões sem PR"),
                    html.H2(id="sessions-no-pr")
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
        "flexWrap": "wrap",
        "marginBottom": "15px"
    }),

    # PROGRESSÃO POR EXERCÍCIO
    html.Div([
        html.H4("Progressão por Exercício", style={"marginTop": "0"}),
        dash_table.DataTable(
            id="progress-table",
            columns=[
                {"name": "Exercício", "id": "exercicio"},
                {"name": "Última sessão", "id": "ultima"},
                {"name": "Melhor série", "id": "serie"},
                {"name": "1RM est. (kg)", "id": "e1rm", "type": "numeric"},
                {"name": "vs anterior", "id": "status"},
                {"name": "Sessões sem PR", "id": "sem_pr", "type": "numeric"},
            ],
            sort_action="native",
            page_size=15,
            style_as_list_view=True,
            style_header={"fontWeight": "600", "backgroundColor": "white"},
            style_cell={
                "fontFamily": "inherit",
                "padding": "8px",
                "textAlign": "left",
                "border": "none",
                "borderBottom": "1px solid #eef0f4"
            },
            style_cell_conditional=[
                {"if": {"column_id": c}, "textAlign": "center"}
                for c in ["status", "sem_pr", "e1rm"]
            ],
            style_data_conditional=[
                {"if": {"filter_query": '{status} = "↑"', "column_id": "status"},
                 "color": "#1a7f37", "fontWeight": "700"},
                {"if": {"filter_query": '{status} = "↓"', "column_id": "status"},
                 "color": "#cf222e", "fontWeight": "700"},
                {"if": {"filter_query": f"{{sem_pr}} >= {STAGNATION_SESSIONS}", "column_id": "sem_pr"},
                 "backgroundColor": "#fff4e5", "color": "#9a6700", "fontWeight": "700"},
            ],
        )
    ], style={**graph_style, "minWidth": "unset"})

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
    Output("last-top-set", "children"),
    Output("best-e1rm", "children"),
    Output("sessions-no-pr", "children"),
    Output("progress-table", "data"),
    Output("exercise-gif", "src"),
    Input("exercise-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date"),
)
def update_graphs(exercise, start_date, end_date):

    # Datas do seletor chegam sem hora: inclui o dia final inteiro
    start_date = pd.to_datetime(start_date).normalize()
    end_date = pd.to_datetime(end_date).normalize() + pd.Timedelta(days=1)

    filtered = df[
        (df["start_time"] >= start_date) &
        (df["start_time"] < end_date)
    ]

    df_ex = filtered[filtered["exercise_title"] == exercise]
    gif_url = gif_map.get(exercise, "")

    # Melhor série de cada sessão do exercício
    ex_top = top_sets(df_ex)
    scores = ex_top["score"].tolist()
    bodyweight = not (ex_top["weight_kg"] > 0).any()

    total_series = len(df_ex)
    if ex_top.empty:
        last_top_set, best_e1rm, no_pr = "–", "–", "–"
    else:
        last = ex_top.iloc[-1]
        last_top_set = f"{format_set(last['weight_kg'], last['reps'])} {progression_status(scores)}"
        best_e1rm = "–" if bodyweight else f"{max(scores):.1f} kg"
        no_pr = sessions_since_pr(scores)

    # Evolução do 1RM estimado
    fig_progress = px.line(
        ex_top.assign(serie=[format_set(w, r) for w, r in zip(ex_top["weight_kg"], ex_top["reps"])]),
        x="start_time",
        y="score",
        markers=True,
        hover_data={"serie": True, "score": ":.1f"},
        labels={
            "start_time": "Data",
            "score": "Repetições" if bodyweight else "1RM estimado (kg)",
            "serie": "Melhor série",
        },
        title="Evolução de Repetições" if bodyweight else "Evolução do 1RM Estimado"
    )

    fig_progress.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Séries por músculo por semana: efetivas (até a falha) x normais
    weeks = max((end_date - start_date).days / 7, 1)
    muscle_sets = (
        filtered.dropna(subset=["muscle"])
        .assign(tipo=lambda d: d["set_type"].isin(EFFECTIVE_SET_TYPES).map({True: "Até a falha", False: "Normal"}))
        .groupby(["muscle", "tipo"])
        .size()
        .div(weeks)
        .round(1)
        .reset_index(name="series")
    )

    fig_muscle = px.bar(
        muscle_sets,
        x="series",
        y="muscle",
        color="tipo",
        orientation="h",
        category_orders={"tipo": ["Até a falha", "Normal"]},
        color_discrete_map={"Até a falha": "#2f6fed", "Normal": "#b8c7e8"},
        labels={"series": "Séries / semana", "muscle": "", "tipo": ""},
        title="Séries por Músculo / Semana"
    )

    fig_muscle.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=-0.15),
        yaxis={"categoryorder": "total ascending"}
    )

    return (
        fig_progress, fig_muscle, total_series, last_top_set, best_e1rm, no_pr,
        progression_table(filtered), gif_url
    )


if __name__ == "__main__":
    app.run(debug=True)
