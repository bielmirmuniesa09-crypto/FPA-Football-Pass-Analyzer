from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from models.match_data import MatchData


# =========================================================
# CARPETA DE L'HISTORIAL
# =========================================================

def obtenir_carpeta_historial() -> Path:
    """
    Retorna la carpeta exports/historial.

    Si la carpeta no existeix, es crea automàticament.
    """

    carpeta_projecte = Path(__file__).resolve().parent.parent
    carpeta_historial = carpeta_projecte / "exports" / "historial"

    carpeta_historial.mkdir(
        parents=True,
        exist_ok=True,
    )

    return carpeta_historial


# =========================================================
# NETEJA DEL NOM DEL FITXER
# =========================================================

def netejar_nom_fitxer(text: str) -> str:
    """
    Converteix un text en un nom segur per utilitzar-lo
    com a nom de fitxer.
    """

    text_net = str(text).strip().lower()

    substitucions = {
        "à": "a",
        "á": "a",
        "è": "e",
        "é": "e",
        "í": "i",
        "ï": "i",
        "ò": "o",
        "ó": "o",
        "ú": "u",
        "ü": "u",
        "ç": "c",
        " ": "_",
        "/": "-",
        "\\": "-",
        ":": "-",
        ";": "-",
        ",": "",
        ".": "",
        "'": "",
        '"': "",
    }

    for original, substitut in substitucions.items():
        text_net = text_net.replace(
            original,
            substitut,
        )

    text_net = "".join(
        caracter
        for caracter in text_net
        if caracter.isalnum()
        or caracter in {"_", "-"}
    )

    return text_net or "sense_dades"


# =========================================================
# CONVERSIÓ DEL PARTIT
# =========================================================

def convertir_partit_a_dict(
    dades_partit: MatchData,
) -> dict[str, Any]:
    """
    Converteix un partit en un diccionari compatible
    amb el format JSON.
    """

    return {
        "versio": "2.1",

        "guardat_el": datetime.now().isoformat(
            timespec="seconds"
        ),

        "partit": {
            "equip": dades_partit.equip,
            "rival": dades_partit.rival,
            "competicio": dades_partit.competicio,
            "data_partit": dades_partit.data_partit,
            "sistema": dades_partit.sistema,
            "local_visitant": dades_partit.local_visitant,
        },

        "alineacio": {
            "jugadors": dades_partit.jugadors.copy(),
            "dorsals": dades_partit.dorsals.copy(),
            "posicions": dades_partit.posicions.copy(),
        },

        "passades": [
            passada.to_dict()
            for passada in dades_partit.passades
        ],

        "resum": dades_partit.resum_partit(),

        "estadistiques_jugadors": (
            dades_partit.estadistiques_tots_jugadors()
        ),

        "historial_passades": (
            dades_partit.historial_passades()
        ),
    }


# =========================================================
# NOM DEL FITXER
# =========================================================

def crear_nom_fitxer(
    dades_partit: MatchData,
) -> str:
    """
    Crea un nom únic per al fitxer JSON del partit.
    """

    equip = netejar_nom_fitxer(
        dades_partit.equip
    )

    rival = netejar_nom_fitxer(
        dades_partit.rival
    )

    data_partit = netejar_nom_fitxer(
        dades_partit.data_partit
    )

    if data_partit == "sense_dades":
        data_partit = datetime.now().strftime(
            "%Y-%m-%d"
        )

    hora = datetime.now().strftime(
        "%H%M%S"
    )

    return (
        f"{data_partit}_"
        f"{equip}_vs_{rival}_"
        f"{hora}.json"
    )


def crear_nom_fitxer_des_de_dades(
    dades: dict[str, Any],
    ruta_anterior: Path | None = None,
) -> str:
    """
    Crea un nom de fitxer a partir de les dades d'un partit
    ja guardat a l'historial.
    """

    dades_partit = dades.get(
        "partit",
        {},
    )

    equip = netejar_nom_fitxer(
        dades_partit.get(
            "equip",
            "equip",
        )
    )

    rival = netejar_nom_fitxer(
        dades_partit.get(
            "rival",
            "rival",
        )
    )

    data_partit = netejar_nom_fitxer(
        dades_partit.get(
            "data_partit",
            "",
        )
    )

    if data_partit == "sense_dades":
        data_partit = datetime.now().strftime(
            "%Y-%m-%d"
        )

    # Intentem conservar el codi horari del fitxer anterior.
    codi_hora = datetime.now().strftime("%H%M%S")

    if ruta_anterior is not None:
        parts_nom = ruta_anterior.stem.split("_")

        if parts_nom:
            possible_hora = parts_nom[-1]

            if possible_hora.isdigit():
                codi_hora = possible_hora

    return (
        f"{data_partit}_"
        f"{equip}_vs_{rival}_"
        f"{codi_hora}.json"
    )


# =========================================================
# GUARDAR PARTIT
# =========================================================

def guardar_partit(
    dades_partit: MatchData,
) -> Path:
    """
    Guarda totes les dades del partit en format JSON.

    Retorna la ruta del fitxer creat.
    """

    if not isinstance(dades_partit, MatchData):
        raise TypeError(
            "Les dades rebudes no són un objecte MatchData."
        )

    if not dades_partit.equip.strip():
        raise ValueError(
            "No es pot guardar el partit perquè falta l'equip."
        )

    if not dades_partit.rival.strip():
        raise ValueError(
            "No es pot guardar el partit perquè falta el rival."
        )

    carpeta_historial = obtenir_carpeta_historial()

    nom_fitxer = crear_nom_fitxer(
        dades_partit
    )

    ruta_fitxer = carpeta_historial / nom_fitxer

    dades_json = convertir_partit_a_dict(
        dades_partit
    )

    escriure_json(
        ruta_fitxer,
        dades_json,
    )

    return ruta_fitxer


# =========================================================
# ESCRIURE JSON
# =========================================================

def escriure_json(
    ruta_fitxer: str | Path,
    dades: dict[str, Any],
) -> None:
    """
    Escriu un diccionari en un fitxer JSON.
    """

    ruta = Path(ruta_fitxer)

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ruta.open(
        mode="w",
        encoding="utf-8",
    ) as fitxer:

        json.dump(
            dades,
            fitxer,
            ensure_ascii=False,
            indent=4,
        )


# =========================================================
# LLEGIR UN PARTIT
# =========================================================

def llegir_partit(
    ruta_fitxer: str | Path,
) -> dict[str, Any]:
    """
    Llegeix un partit guardat en format JSON.
    """

    ruta = Path(ruta_fitxer)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No existeix el fitxer: {ruta}"
        )

    if not ruta.is_file():
        raise ValueError(
            f"La ruta indicada no és un fitxer: {ruta}"
        )

    with ruta.open(
        mode="r",
        encoding="utf-8",
    ) as fitxer:

        dades = json.load(fitxer)

    if not isinstance(dades, dict):
        raise ValueError(
            "El fitxer no conté un partit vàlid."
        )

    return dades


# =========================================================
# EDITAR PARTIT
# =========================================================

def editar_partit(
    ruta_fitxer: str | Path,
    equip: str,
    rival: str,
    competicio: str = "",
    data_partit: str = "",
) -> Path:
    """
    Modifica les dades generals d'un partit guardat.

    També modifica el nom del fitxer JSON perquè coincideixi
    amb el nou equip, rival i data.

    Retorna la nova ruta del fitxer.
    """

    ruta_anterior = Path(ruta_fitxer)

    if not ruta_anterior.exists():
        raise FileNotFoundError(
            "No s'ha trobat el partit que vols editar."
        )

    equip_net = str(equip).strip()
    rival_net = str(rival).strip()
    competicio_neta = str(competicio).strip()
    data_neta = str(data_partit).strip()

    if not equip_net:
        raise ValueError(
            "El nom de l'equip no pot estar buit."
        )

    if not rival_net:
        raise ValueError(
            "El nom del rival no pot estar buit."
        )

    dades = llegir_partit(
        ruta_anterior
    )

    dades_partit = dades.setdefault(
        "partit",
        {},
    )

    dades_partit["equip"] = equip_net
    dades_partit["rival"] = rival_net
    dades_partit["competicio"] = competicio_neta
    dades_partit["data_partit"] = data_neta

    dades["modificat_el"] = datetime.now().isoformat(
        timespec="seconds"
    )

    nou_nom = crear_nom_fitxer_des_de_dades(
        dades=dades,
        ruta_anterior=ruta_anterior,
    )

    nova_ruta = ruta_anterior.parent / nou_nom

    # Evitem sobreescriure un altre partit.
    if (
        nova_ruta.exists()
        and nova_ruta.resolve() != ruta_anterior.resolve()
    ):
        numero = 2
        nom_base = nova_ruta.stem
        extensio = nova_ruta.suffix

        while nova_ruta.exists():
            nova_ruta = (
                ruta_anterior.parent
                / f"{nom_base}_{numero}{extensio}"
            )
            numero += 1

    # Primer escrivim les dades noves.
    escriure_json(
        nova_ruta,
        dades,
    )

    # Si ha canviat el nom, eliminem l'antic fitxer.
    if nova_ruta.resolve() != ruta_anterior.resolve():
        ruta_anterior.unlink()

    return nova_ruta


# =========================================================
# ELIMINAR PARTIT
# =========================================================

def eliminar_partit(
    ruta_fitxer: str | Path,
) -> None:
    """
    Elimina definitivament un partit de l'historial.
    """

    ruta = Path(ruta_fitxer)

    if not ruta.exists():
        raise FileNotFoundError(
            "El partit seleccionat ja no existeix."
        )

    if not ruta.is_file():
        raise ValueError(
            "La ruta seleccionada no correspon a un fitxer."
        )

    if ruta.suffix.lower() != ".json":
        raise ValueError(
            "Només es poden eliminar fitxers JSON de l'historial."
        )

    carpeta_historial = obtenir_carpeta_historial().resolve()

    try:
        ruta_resolta = ruta.resolve()
    except OSError as error:
        raise OSError(
            "No s'ha pogut comprovar la ruta del partit."
        ) from error

    if ruta_resolta.parent != carpeta_historial:
        raise ValueError(
            "El fitxer no pertany a la carpeta de l'historial."
        )

    ruta.unlink()


# =========================================================
# LLISTA DE PARTITS GUARDATS
# =========================================================

def obtenir_partits_guardats() -> list[dict[str, Any]]:
    """
    Retorna tots els partits guardats, ordenats
    del més recent al més antic.
    """

    carpeta_historial = obtenir_carpeta_historial()

    fitxers_json = sorted(
        carpeta_historial.glob("*.json"),
        key=lambda ruta: ruta.stat().st_mtime,
        reverse=True,
    )

    partits_guardats: list[dict[str, Any]] = []

    for ruta_fitxer in fitxers_json:

        try:
            dades = llegir_partit(
                ruta_fitxer
            )

            partits_guardats.append(
                {
                    "ruta": str(ruta_fitxer),
                    "nom_fitxer": ruta_fitxer.name,
                    "dades": dades,
                }
            )

        except (
            OSError,
            ValueError,
            json.JSONDecodeError,
        ) as error:

            print(
                f"No s'ha pogut llegir "
                f"{ruta_fitxer.name}: {error}"
            )

    return partits_guardats