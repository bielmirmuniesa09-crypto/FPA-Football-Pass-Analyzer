from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# =========================================================
# ESDEVENIMENT DE PASSADA
# =========================================================

@dataclass
class PassEvent:
    """
    Representa una passada registrada durant el partit.
    """

    origen: int
    desti: int | None
    resultat: str

    def to_dict(self) -> dict[str, Any]:
        """
        Converteix la passada en un diccionari.
        """

        return {
            "origen": self.origen,
            "desti": self.desti,
            "resultat": self.resultat,
        }


# =========================================================
# MODEL PRINCIPAL DEL PARTIT
# =========================================================

@dataclass
class MatchData:
    """
    Emmagatzema tota la informació del partit.

    Inclou:
    - dades generals;
    - jugadors;
    - passades bones;
    - passades dolentes;
    - estadístiques individuals;
    - estadístiques globals.
    """

    equip: str = ""
    rival: str = ""
    competicio: str = "Lliga"
    data_partit: str = ""
    sistema: str = "4-3-3"
    local_visitant: str = "Local"

    jugadors: list[str] = field(default_factory=list)
    dorsals: list[str] = field(default_factory=list)
    posicions: list[str] = field(default_factory=list)

    passades: list[PassEvent] = field(default_factory=list)

    # =====================================================
    # CONFIGURACIÓ DEL PARTIT
    # =====================================================

    def configurar_partit(
        self,
        equip: str,
        rival: str,
        competicio: str,
        data_partit: str,
        sistema: str,
        local_visitant: str,
        jugadors: list[str],
        dorsals: list[str],
        posicions: list[str],
    ) -> None:
        """
        Guarda la configuració inicial del partit.
        """

        self.equip = equip.strip()
        self.rival = rival.strip()
        self.competicio = competicio.strip()
        self.data_partit = data_partit.strip()
        self.sistema = sistema.strip()
        self.local_visitant = local_visitant.strip()

        self.jugadors = [
            jugador.strip()
            for jugador in jugadors
        ]

        self.dorsals = [
            dorsal.strip()
            for dorsal in dorsals
        ]

        self.posicions = [
            posicio.strip()
            for posicio in posicions
        ]

        # Cada vegada que es configura un partit nou,
        # es reinicien les passades.
        self.passades.clear()

    # =====================================================
    # VALIDACIÓ
    # =====================================================

    def configuracio_valida(self) -> tuple[bool, str]:
        """
        Comprova que la configuració sigui correcta.
        """

        if not self.equip:
            return False, "Has d'introduir el nom de l'equip."

        if not self.rival:
            return False, "Has d'introduir el nom del rival."

        if len(self.jugadors) != 11:
            return False, "Has d'introduir exactament 11 jugadors."

        for index, jugador in enumerate(self.jugadors, start=1):
            if not jugador:
                return False, f"Falta el nom del jugador {index}."

        if len(set(self.jugadors)) != len(self.jugadors):
            return False, "No es poden repetir noms de jugadors."

        return True, ""

    # =====================================================
    # REGISTRE DE PASSADES
    # =====================================================

    def registrar_passada_bona(
        self,
        origen: int,
        desti: int,
    ) -> None:
        """
        Registra una passada completada correctament.
        """

        self._validar_index_jugador(origen)
        self._validar_index_jugador(desti)

        if origen == desti:
            raise ValueError(
                "El jugador d'origen i el destinatari no poden ser el mateix."
            )

        self.passades.append(
            PassEvent(
                origen=origen,
                desti=desti,
                resultat="bona",
            )
        )

    def registrar_passada_dolenta(
        self,
        origen: int,
        desti: int | None = None,
    ) -> None:
        """
        Registra una passada fallada.

        El destí pot ser:
        - un jugador concret;
        - None, si la pilota surt fora o és interceptada.
        """

        self._validar_index_jugador(origen)

        if desti is not None:
            self._validar_index_jugador(desti)

            if origen == desti:
                raise ValueError(
                    "El jugador d'origen i el destinatari no poden ser el mateix."
                )

        self.passades.append(
            PassEvent(
                origen=origen,
                desti=desti,
                resultat="dolenta",
            )
        )

    def desfer_ultima_passada(self) -> PassEvent | None:
        """
        Elimina l'última passada registrada.
        """

        if not self.passades:
            return None

        return self.passades.pop()

    def reiniciar_passades(self) -> None:
        """
        Elimina totes les passades del partit.
        """

        self.passades.clear()

    # =====================================================
    # ESTADÍSTIQUES GLOBALS
    # =====================================================

    def total_passades(self) -> int:
        return len(self.passades)

    def total_passades_bones(self) -> int:
        return sum(
            1
            for passada in self.passades
            if passada.resultat == "bona"
        )

    def total_passades_dolentes(self) -> int:
        return sum(
            1
            for passada in self.passades
            if passada.resultat == "dolenta"
        )

    def percentatge_encert_global(self) -> float:
        """
        Calcula la precisió global de l'equip.
        """

        total = self.total_passades()

        if total == 0:
            return 0.0

        return (
            self.total_passades_bones()
            / total
            * 100
        )

    # =====================================================
    # ESTADÍSTIQUES PER JUGADOR
    # =====================================================

    def estadistiques_jugador(
        self,
        jugador_index: int,
    ) -> dict[str, int | float | str]:
        """
        Calcula les estadístiques d'un jugador.
        """

        self._validar_index_jugador(jugador_index)

        bones = 0
        dolentes = 0
        rebudes = 0

        for passada in self.passades:

            if passada.origen == jugador_index:

                if passada.resultat == "bona":
                    bones += 1
                else:
                    dolentes += 1

            if (
                passada.resultat == "bona"
                and passada.desti == jugador_index
            ):
                rebudes += 1

        intentades = bones + dolentes

        if intentades == 0:
            precisio = 0.0
        else:
            precisio = bones / intentades * 100

        return {
            "index": jugador_index,
            "jugador": self.jugadors[jugador_index],
            "dorsal": self.dorsals[jugador_index]
            if jugador_index < len(self.dorsals)
            else "",
            "posicio": self.posicions[jugador_index]
            if jugador_index < len(self.posicions)
            else "",
            "intentades": intentades,
            "bones": bones,
            "dolentes": dolentes,
            "rebudes": rebudes,
            "precisio": precisio,
        }

    def estadistiques_tots_jugadors(
        self,
    ) -> list[dict[str, int | float | str]]:
        """
        Retorna les estadístiques de tots els jugadors.
        """

        return [
            self.estadistiques_jugador(index)
            for index in range(len(self.jugadors))
        ]

    # =====================================================
    # HISTORIAL
    # =====================================================

    def historial_passades(self) -> list[dict[str, Any]]:
        """
        Retorna l'historial en format llegible.
        """

        historial = []

        for numero, passada in enumerate(
            self.passades,
            start=1,
        ):

            nom_origen = self.jugadors[passada.origen]

            if passada.desti is None:
                nom_desti = "Sense destinatari"
            else:
                nom_desti = self.jugadors[passada.desti]

            historial.append(
                {
                    "numero": numero,
                    "origen": nom_origen,
                    "desti": nom_desti,
                    "resultat": passada.resultat,
                }
            )

        return historial

    # =====================================================
    # RESUM GENERAL
    # =====================================================

    def resum_partit(self) -> dict[str, Any]:
        """
        Retorna un resum general del partit.
        """

        return {
            "equip": self.equip,
            "rival": self.rival,
            "competicio": self.competicio,
            "data_partit": self.data_partit,
            "sistema": self.sistema,
            "local_visitant": self.local_visitant,
            "jugadors": self.jugadors.copy(),
            "dorsals": self.dorsals.copy(),
            "posicions": self.posicions.copy(),
            "total": self.total_passades(),
            "bones": self.total_passades_bones(),
            "dolentes": self.total_passades_dolentes(),
            "precisio": self.percentatge_encert_global(),
        }

    # =====================================================
    # VALIDACIÓ INTERNA
    # =====================================================

    def _validar_index_jugador(
        self,
        index: int,
    ) -> None:
        """
        Comprova que l'índex del jugador existeixi.
        """

        if not isinstance(index, int):
            raise TypeError(
                "L'índex del jugador ha de ser un nombre enter."
            )

        if index < 0 or index >= len(self.jugadors):
            raise IndexError(
                f"No existeix cap jugador amb l'índex {index}."
            )