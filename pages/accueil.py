
import dash
import dash_bootstrap_components as dbc

from dash import html, dcc

dash.register_page(
    __name__,
    path="/",
    name="Accueil",
    title="Accueil | Dashboard Multi-Sectoriel Kaffrine"
)


# =====================================================
# CARTE D'ACCÈS
# =====================================================

def access_card(icon, title, description, href):
    return dbc.Col(
        dcc.Link(
            dbc.Card(
                dbc.CardBody([
                    html.Div(
                        html.I(className=f"bi {icon}"),
                        className="home-card-icon"
                    ),
                    html.H5(
                        title,
                        className="home-card-title"
                    ),
                    html.P(
                        description,
                        className="home-card-description"
                    ),
                    html.Div(
                        [
                            "Accéder à la page ",
                            html.I(className="bi bi-arrow-right")
                        ],
                        className="home-card-link"
                    )
                ]),
                className="home-card h-100"
            ),
            href=href,
            className="home-card-anchor"
        ),
        xs=12,
        sm=6,
        md=4,
        lg=2,
        className="home-card-column"
    )


# =====================================================
# PAGE D'ACCUEIL
# =====================================================

layout = html.Div([

    # -------------------------------------------------
    # 1. BANNIÈRE INSTITUTIONNELLE COMPACTE
    # -------------------------------------------------

    html.Div([

        html.Div([
            html.Div(
                html.I(className="bi bi-bar-chart-line-fill"),
                className="home-logo"
            ),

            html.Div([
                html.Div(
                    "RÉGION DE KAFFRINE",
                    className="home-eyebrow"
                ),
                html.Div(
                    "Dashboard Multi-Sectoriel",
                    className="home-brand"
                )
            ])
        ], className="home-brand-row"),

        html.H1(
            "Bienvenue sur votre espace statistique",
            className="home-title"
        ),

        html.P(
            "Explorez les indicateurs de développement territorial, "
            "analysez leur évolution et comparez les résultats "
            "entre secteurs et territoires.",
            className="home-description"
        ),

        html.Div([
            html.I(className="bi bi-shield-check me-2"),
            "Plateforme de consultation et d'analyse statistique"
        ], className="home-status")

    ], className="home-hero"),


    # -------------------------------------------------
    # 2. PRÉSENTATION DE LA RÉGION
    # -------------------------------------------------

    html.Div([

        html.Div([
            html.I(className="bi bi-geo-alt-fill me-2"),
            html.Span(
                "Présentation de la région",
                className="region-intro-title"
            )
        ], className="region-intro-heading"),

        html.P(
            "Anciennement rattachée à la région de Kaolack, Kaffrine "
            "a été érigée en région par la loi n° 2008-14 du "
            "18 mars 2008. Elle comprend quatre départements : "
            "Birkelane, Kaffrine, Koungheul et Malem Hodar. "
            "Koungheul est le département le plus vaste avec "
            "4 237 km² (37,9 % du territoire régional), suivi de "
            "Malem Hodar avec 3 106 km² (27,8 %), de Kaffrine "
            "avec 2 716 km² (24,3 %) et de Birkelane avec "
            "1 122 km² (10,0 %).",
            className="region-intro-text"
        )

    ], className="region-intro"),


    # -------------------------------------------------
    # 3. NAVIGATION PRINCIPALE
    # -------------------------------------------------

    html.Div([

        html.H3(
            "Explorer les données",
            className="home-section-title"
        ),

        html.P(
            "Choisissez un espace pour commencer votre analyse.",
            className="home-section-description"
        ),

        dbc.Row([

            access_card(
                "bi-clipboard-data-fill",
                "Statistiques",
                "Consultez les statistiques clés de la région.",
                "/statistiques"
            ),

            access_card(
                "bi-grid-1x2-fill",
                "Indicateurs sectoriels",
                "Consultez les KPI par secteur, année et territoire.",
                "/secteurs"
            ),

            access_card(
                "bi-graph-up-arrow",
                "Analyse graphique",
                "Visualisez les tendances et les évolutions.",
                "/graphiques"
            ),

            access_card(
                "bi-arrow-left-right",
                "Comparaison",
                "Comparez les indicateurs entre deux années.",
                "/comparaison"
            ),

            access_card(
                "bi-geo-alt-fill",
                "Cartographie",
                "Explorez les indicateurs sur une carte du territoire.",
                "/cartographie"
            )

        ], className="home-cards-row g-3")

    ], className="home-explore"),


    # -------------------------------------------------
    # 4. PIED DE PAGE
    # -------------------------------------------------

    html.Div([

        html.Span(
            "Dashboard Multi-Sectoriel de Kaffrine",
            className="home-footer-brand"
        ),

        html.Span(
            "Suivi · Analyse · Comparaison",
            className="home-footer-text"
        )

    ], className="home-footer")

], className="home-page")
