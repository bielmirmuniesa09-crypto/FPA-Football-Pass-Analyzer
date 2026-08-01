from __future__ import annotations

from collections import defaultdict
from typing import Any

import networkx as nx

from models.match_data import MatchData


# =========================================================
# CREACIÓ DEL GRAF
# =========================================================

def crear_graf_passades(
    dades_partit: MatchData,
) -> nx.DiGraph:
    """
    Crea un graf dirigit i ponderat a partir de les passades bones.

    Cada jugador és un node.

    Cada passada bona genera una aresta dirigida:
        origen -> destí

    El pes de l'aresta representa el nombre de passades bones
    entre els dos jugadors.
    """

    graf = nx.DiGraph()

    # Afegim tots els jugadors com a nodes,
    # encara que no hagin participat en cap passada.
    for index, nom in enumerate(dades_partit.jugadors):
        dorsal = (
            dades_partit.dorsals[index]
            if index < len(dades_partit.dorsals)
            else str(index + 1)
        )

        posicio = (
            dades_partit.posicions[index]
            if index < len(dades_partit.posicions)
            else ""
        )

        graf.add_node(
            index,
            nom=nom,
            dorsal=dorsal,
            posicio=posicio,
            etiqueta=f"{dorsal}. {nom}",
        )

    # Comptem només les passades bones.
    pesos_aresta: dict[tuple[int, int], int] = defaultdict(int)

    for passada in dades_partit.passades:
        if passada.resultat != "bona":
            continue

        if passada.desti is None:
            continue

        clau = (
            passada.origen,
            passada.desti,
        )

        pesos_aresta[clau] += 1

    # Creem les arestes ponderades.
    for (origen, desti), pes in pesos_aresta.items():
        graf.add_edge(
            origen,
            desti,
            weight=pes,
        )

    return graf


# =========================================================
# MATRIU DE PASSADES
# =========================================================

def crear_matriu_passades(
    dades_partit: MatchData,
) -> list[list[int]]:
    """
    Crea una matriu d'adjacència amb el nombre de passades bones.

    matriu[i][j] indica quantes passades bones ha fet
    el jugador i al jugador j.
    """

    nombre_jugadors = len(dades_partit.jugadors)

    matriu = [
        [0 for _ in range(nombre_jugadors)]
        for _ in range(nombre_jugadors)
    ]

    for passada in dades_partit.passades:
        if passada.resultat != "bona":
            continue

        if passada.desti is None:
            continue

        matriu[passada.origen][passada.desti] += 1

    return matriu


# =========================================================
# CENTRALITATS
# =========================================================

def calcular_centralitats(
    dades_partit: MatchData,
) -> dict[int, dict[str, float]]:
    """
    Calcula les principals mesures de centralitat.

    Mesures incloses:
    - degree;
    - in-degree;
    - out-degree;
    - betweenness;
    - closeness;
    - PageRank.

    Retorna un diccionari indexat per l'índex del jugador.
    """

    graf = crear_graf_passades(dades_partit)

    nombre_nodes = graf.number_of_nodes()

    if nombre_nodes == 0:
        return {}

    degree = nx.degree_centrality(graf)
    in_degree = nx.in_degree_centrality(graf)
    out_degree = nx.out_degree_centrality(graf)

    betweenness = nx.betweenness_centrality(
        graf,
        weight=None,
        normalized=True,
    )

    closeness = nx.closeness_centrality(
        graf,
    )

    if graf.number_of_edges() > 0:
        pagerank = nx.pagerank(
            graf,
            weight="weight",
        )
    else:
        valor_uniforme = 1 / nombre_nodes

        pagerank = {
            node: valor_uniforme
            for node in graf.nodes
        }

    resultats: dict[int, dict[str, float]] = {}

    for node in graf.nodes:
        resultats[node] = {
            "degree": float(
                degree.get(node, 0.0)
            ),
            "in_degree": float(
                in_degree.get(node, 0.0)
            ),
            "out_degree": float(
                out_degree.get(node, 0.0)
            ),
            "betweenness": float(
                betweenness.get(node, 0.0)
            ),
            "closeness": float(
                closeness.get(node, 0.0)
            ),
            "pagerank": float(
                pagerank.get(node, 0.0)
            ),
        }

    return resultats


# =========================================================
# ESTADÍSTIQUES COMPLETES PER JUGADOR
# =========================================================

def obtenir_estadistiques_completes(
    dades_partit: MatchData,
) -> list[dict[str, Any]]:
    """
    Combina les estadístiques de passades amb les centralitats.
    """

    estadistiques_basiques = (
        dades_partit.estadistiques_tots_jugadors()
    )

    centralitats = calcular_centralitats(
        dades_partit
    )

    resultats: list[dict[str, Any]] = []

    for estadistica in estadistiques_basiques:
        index = int(
            estadistica["index"]
        )

        dades_centralitat = centralitats.get(
            index,
            {
                "degree": 0.0,
                "in_degree": 0.0,
                "out_degree": 0.0,
                "betweenness": 0.0,
                "closeness": 0.0,
                "pagerank": 0.0,
            },
        )

        fila = {
            **estadistica,
            **dades_centralitat,
        }

        resultats.append(
            fila
        )

    return resultats


# =========================================================
# RÀNQUINGS
# =========================================================

def obtenir_ranquing(
    dades_partit: MatchData,
    camp: str,
    descendent: bool = True,
) -> list[dict[str, Any]]:
    """
    Ordena els jugadors segons una estadística concreta.

    Exemples de camp:
    - bones
    - dolentes
    - rebudes
    - precisio
    - degree
    - betweenness
    - closeness
    - pagerank
    """

    estadistiques = obtenir_estadistiques_completes(
        dades_partit
    )

    if not estadistiques:
        return []

    if camp not in estadistiques[0]:
        raise ValueError(
            f"El camp de rànquing '{camp}' no existeix."
        )

    return sorted(
        estadistiques,
        key=lambda fila: fila.get(camp, 0),
        reverse=descendent,
    )


def obtenir_jugador_mes_influent(
    dades_partit: MatchData,
) -> dict[str, Any] | None:
    """
    Retorna el jugador amb PageRank més alt.
    """

    ranquing = obtenir_ranquing(
        dades_partit,
        camp="pagerank",
    )

    if not ranquing:
        return None

    return ranquing[0]


def obtenir_jugador_amb_mes_passades_bones(
    dades_partit: MatchData,
) -> dict[str, Any] | None:
    """
    Retorna el jugador que ha completat més passades.
    """

    ranquing = obtenir_ranquing(
        dades_partit,
        camp="bones",
    )

    if not ranquing:
        return None

    return ranquing[0]


def obtenir_jugador_amb_mes_passades_rebudes(
    dades_partit: MatchData,
) -> dict[str, Any] | None:
    """
    Retorna el jugador que ha rebut més passades bones.
    """

    ranquing = obtenir_ranquing(
        dades_partit,
        camp="rebudes",
    )

    if not ranquing:
        return None

    return ranquing[0]


def obtenir_jugador_amb_mes_errors(
    dades_partit: MatchData,
) -> dict[str, Any] | None:
    """
    Retorna el jugador amb més passades dolentes.
    """

    ranquing = obtenir_ranquing(
        dades_partit,
        camp="dolentes",
    )

    if not ranquing:
        return None

    return ranquing[0]


# =========================================================
# RESUM DE LA XARXA
# =========================================================

def obtenir_resum_xarxa(
    dades_partit: MatchData,
) -> dict[str, Any]:
    """
    Retorna un resum general del graf de passades.
    """

    graf = crear_graf_passades(
        dades_partit
    )

    nombre_nodes = graf.number_of_nodes()
    nombre_arestes = graf.number_of_edges()

    if nombre_nodes <= 1:
        densitat = 0.0
    else:
        densitat = nx.density(
            graf
        )

    components_febles = list(
        nx.weakly_connected_components(graf)
    )

    nombre_components = len(
        components_febles
    )

    node_mes_influent = obtenir_jugador_mes_influent(
        dades_partit
    )

    jugador_mes_passades = (
        obtenir_jugador_amb_mes_passades_bones(
            dades_partit
        )
    )

    jugador_mes_rebut = (
        obtenir_jugador_amb_mes_passades_rebudes(
            dades_partit
        )
    )

    return {
        "nodes": nombre_nodes,
        "arestes": nombre_arestes,
        "densitat": densitat,
        "components": nombre_components,
        "jugador_mes_influent": node_mes_influent,
        "jugador_mes_passades": jugador_mes_passades,
        "jugador_mes_rebut": jugador_mes_rebut,
    }


# =========================================================
# POSICIONS DEL GRAF
# =========================================================

def obtenir_posicions_graf(
    dades_partit: MatchData,
) -> dict[int, tuple[float, float]]:
    """
    Calcula unes posicions estables per dibuixar el graf.

    Utilitza una disposició spring, adequada per visualitzar
    les connexions entre jugadors.
    """

    graf = crear_graf_passades(
        dades_partit
    )

    if graf.number_of_nodes() == 0:
        return {}

    if graf.number_of_edges() == 0:
        return nx.circular_layout(
            graf
        )

    return nx.spring_layout(
        graf,
        weight="weight",
        seed=42,
        k=0.9,
        iterations=100,
    )


# =========================================================
# ETIQUETES I PESOS
# =========================================================

def obtenir_etiquetes_nodes(
    dades_partit: MatchData,
) -> dict[int, str]:
    """
    Retorna les etiquetes dels nodes.
    """

    graf = crear_graf_passades(
        dades_partit
    )

    return {
        node: dades.get(
            "etiqueta",
            str(node),
        )
        for node, dades in graf.nodes(data=True)
    }


def obtenir_pesos_arestes(
    dades_partit: MatchData,
) -> dict[tuple[int, int], int]:
    """
    Retorna un diccionari amb el pes de cada aresta.
    """

    graf = crear_graf_passades(
        dades_partit
    )

    return {
        (
            origen,
            desti,
        ): int(
            dades.get(
                "weight",
                1,
            )
        )
        for origen, desti, dades in graf.edges(data=True)
    }


# =========================================================
# MIDA DELS NODES
# =========================================================

def calcular_mides_nodes(
    dades_partit: MatchData,
    mida_minima: float = 800.0,
    mida_maxima: float = 2600.0,
) -> dict[int, float]:
    """
    Calcula la mida visual de cada node segons PageRank.
    """

    centralitats = calcular_centralitats(
        dades_partit
    )

    if not centralitats:
        return {}

    valors = [
        dades["pagerank"]
        for dades in centralitats.values()
    ]

    minim = min(valors)
    maxim = max(valors)

    mides: dict[int, float] = {}

    for node, dades in centralitats.items():
        valor = dades["pagerank"]

        if maxim == minim:
            mida = (
                mida_minima
                + mida_maxima
            ) / 2

        else:
            proporcio = (
                valor - minim
            ) / (
                maxim - minim
            )

            mida = (
                mida_minima
                + proporcio
                * (
                    mida_maxima
                    - mida_minima
                )
            )

        mides[node] = mida

    return mides
