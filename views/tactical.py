from __future__ import annotations

import tkinter as tk
from typing import Any, Callable

import customtkinter as ctk

from models.match_data import MatchData
from utils.graph_utils import obtenir_estadistiques_completes


class TacticalView(ctk.CTkFrame):
    """
    Vista tàctica de l'alineació inicial.

    Important:
    La posició dels jugadors representa la disposició inicial
    indicada a la configuració del partit, no la posició real
    que han ocupat durant tots els minuts del joc.
    """

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_TARGETA = "#12382E"

    COLOR_CAMP = "#168447"
    COLOR_CAMP_ALTERNATIU = "#11783E"
    COLOR_LINIES = "#E7F7ED"

    COLOR_VERD = "#22C55E"
    COLOR_GROC = "#FACC15"
    COLOR_BLAU = "#38BDF8"
    COLOR_LILA = "#A78BFA"
    COLOR_VERMELL = "#EF4444"

    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"
    COLOR_LINIA = "#315B4D"

    def __init__(
        self,
        master,
        dades_partit: MatchData,
        tornar_resultats: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.dades_partit = dades_partit
        self.tornar_resultats = tornar_resultats

        self.estadistiques = obtenir_estadistiques_completes(
            self.dades_partit
        )

        self.jugador_seleccionat: int | None = None
        self.elements_jugadors: dict[int, dict[str, int]] = {}

        self.canvas: tk.Canvas | None = None
        self.panell_jugador: ctk.CTkFrame | None = None

        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self._crear_capcalera()
        self._crear_contingut()

    # =====================================================
    # CAPÇALERA
    # =====================================================

    def _crear_capcalera(self) -> None:
        capcalera = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_PANELL,
            corner_radius=0,
            height=82,
        )
        capcalera.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
        )
        capcalera.grid_propagate(False)
        capcalera.grid_columnconfigure(0, weight=1)

        bloc_text = ctk.CTkFrame(
            capcalera,
            fg_color="transparent",
        )
        bloc_text.grid(
            row=0,
            column=0,
            sticky="w",
            padx=24,
            pady=13,
        )

        ctk.CTkLabel(
            bloc_text,
            text="Disposició tàctica",
            font=ctk.CTkFont(
                size=25,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            bloc_text,
            text=(
                "Alineació inicial del partit. "
                "No representa la posició real dels jugadors "
                "durant tot el joc."
            ),
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        if self.tornar_resultats is not None:
            ctk.CTkButton(
                capcalera,
                text="← RESULTATS",
                command=self.tornar_resultats,
                width=135,
                height=38,
                fg_color="transparent",
                hover_color="#17483A",
                border_width=1,
                border_color=self.COLOR_LINIA,
                text_color=self.COLOR_TEXT,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
            ).grid(
                row=0,
                column=1,
                padx=24,
            )

    # =====================================================
    # CONTINGUT
    # =====================================================

    def _crear_contingut(self) -> None:
        bloc_camp = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        bloc_camp.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20, 10),
            pady=20,
        )
        bloc_camp.grid_columnconfigure(0, weight=1)
        bloc_camp.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            bloc_camp,
            text=(
                f"{self.dades_partit.sistema} · "
                f"{self.dades_partit.equip}"
            ),
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=18,
            pady=(14, 8),
        )

        self.canvas = tk.Canvas(
            bloc_camp,
            background=self.COLOR_CAMP,
            highlightthickness=0,
        )
        self.canvas.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14),
        )

        self.canvas.bind(
            "<Configure>",
            self._redibuixar_camp,
        )

        self.panell_jugador = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        self.panell_jugador.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10, 20),
            pady=20,
        )

        self._mostrar_panell_inicial()

    # =====================================================
    # DIBUIX DEL CAMP
    # =====================================================

    def _redibuixar_camp(
        self,
        event=None,
    ) -> None:
        if self.canvas is None:
            return

        amplada = max(
            self.canvas.winfo_width(),
            600,
        )

        alcada = max(
            self.canvas.winfo_height(),
            650,
        )

        self.canvas.delete("all")
        self.elements_jugadors.clear()

        self._dibuixar_terreny(
            amplada,
            alcada,
        )

        self._dibuixar_jugadors(
            amplada,
            alcada,
        )

    def _dibuixar_terreny(
        self,
        amplada: int,
        alcada: int,
    ) -> None:
        if self.canvas is None:
            return

        marge = 28

        amplada_util = amplada - 2 * marge
        alcada_util = alcada - 2 * marge

        # Franges verticals de gespa.
        nombre_franges = 8

        for index in range(nombre_franges):
            x1 = marge + (
                amplada_util
                / nombre_franges
                * index
            )

            x2 = marge + (
                amplada_util
                / nombre_franges
                * (index + 1)
            )

            color = (
                self.COLOR_CAMP
                if index % 2 == 0
                else self.COLOR_CAMP_ALTERNATIU
            )

            self.canvas.create_rectangle(
                x1,
                marge,
                x2,
                alcada - marge,
                fill=color,
                outline=color,
            )

        # Límits del camp.
        self.canvas.create_rectangle(
            marge,
            marge,
            amplada - marge,
            alcada - marge,
            outline=self.COLOR_LINIES,
            width=3,
        )

        # Línia central.
        centre_y = alcada / 2

        self.canvas.create_line(
            marge,
            centre_y,
            amplada - marge,
            centre_y,
            fill=self.COLOR_LINIES,
            width=3,
        )

        # Cercle central.
        radi = min(
            amplada,
            alcada,
        ) * 0.09

        self.canvas.create_oval(
            amplada / 2 - radi,
            centre_y - radi,
            amplada / 2 + radi,
            centre_y + radi,
            outline=self.COLOR_LINIES,
            width=3,
        )

        self.canvas.create_oval(
            amplada / 2 - 4,
            centre_y - 4,
            amplada / 2 + 4,
            centre_y + 4,
            fill=self.COLOR_LINIES,
            outline=self.COLOR_LINIES,
        )

        # Àrees de penal.
        ample_area = amplada_util * 0.46
        alt_area = alcada_util * 0.16

        x_area_1 = amplada / 2 - ample_area / 2
        x_area_2 = amplada / 2 + ample_area / 2

        self.canvas.create_rectangle(
            x_area_1,
            marge,
            x_area_2,
            marge + alt_area,
            outline=self.COLOR_LINIES,
            width=3,
        )

        self.canvas.create_rectangle(
            x_area_1,
            alcada - marge - alt_area,
            x_area_2,
            alcada - marge,
            outline=self.COLOR_LINIES,
            width=3,
        )

        # Àrees petites.
        ample_area_petita = amplada_util * 0.22
        alt_area_petita = alcada_util * 0.07

        x_petita_1 = (
            amplada / 2
            - ample_area_petita / 2
        )

        x_petita_2 = (
            amplada / 2
            + ample_area_petita / 2
        )

        self.canvas.create_rectangle(
            x_petita_1,
            marge,
            x_petita_2,
            marge + alt_area_petita,
            outline=self.COLOR_LINIES,
            width=3,
        )

        self.canvas.create_rectangle(
            x_petita_1,
            alcada - marge - alt_area_petita,
            x_petita_2,
            alcada - marge,
            outline=self.COLOR_LINIES,
            width=3,
        )

    # =====================================================
    # POSICIONS DELS JUGADORS
    # =====================================================

    def _obtenir_coordenades_posicio(
        self,
        posicio: str,
        index: int,
    ) -> tuple[float, float]:
        """
        Retorna coordenades normalitzades entre 0 i 1.

        El camp s'interpreta verticalment:
        - porter a la zona inferior;
        - davanters a la zona superior.
        """

        posicio_neta = (
            posicio.strip()
            .upper()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

        mapa = {
            # Porter
            "POR": (0.50, 0.91),
            "PORTER": (0.50, 0.91),
            "GK": (0.50, 0.91),

            # Defensa
            "LD": (0.82, 0.75),
            "LATERDRET": (0.82, 0.75),
            "RB": (0.82, 0.75),

            "LE": (0.18, 0.75),
            "LATERESQUERRE": (0.18, 0.75),
            "LB": (0.18, 0.75),

            "CD": (0.62, 0.78),
            "DFC": (0.62, 0.78),
            "CENTRALDRET": (0.62, 0.78),

            "CE": (0.38, 0.78),
            "CENTRALESQUERRE": (0.38, 0.78),

            # Migcamp
            "MCD": (0.50, 0.60),
            "PIVOT": (0.50, 0.60),

            "MC1": (0.28, 0.49),
            "MC2": (0.50, 0.52),
            "MC3": (0.72, 0.49),

            "MC": (0.50, 0.52),
            "MIGCAMPISTA": (0.50, 0.52),

            "MCE": (0.30, 0.49),
            "MCDRET": (0.70, 0.49),

            "MCO": (0.50, 0.39),
            "MITJAPUNTA": (0.50, 0.39),

            # Atac
            "EE": (0.18, 0.23),
            "EXTREMESQUERRE": (0.18, 0.23),
            "EI": (0.18, 0.23),
            "LW": (0.18, 0.23),

            "ED": (0.82, 0.23),
            "EXTREMDRET": (0.82, 0.23),
            "RW": (0.82, 0.23),

            "DC": (0.50, 0.16),
            "DAVANTERCENTRE": (0.50, 0.16),
            "ST": (0.50, 0.16),
        }

        if posicio_neta in mapa:
            return mapa[posicio_neta]

        # Posicions alternatives perquè cap jugador
        # quedi fora del camp.
        posicions_reserva = [
            (0.50, 0.91),
            (0.18, 0.76),
            (0.38, 0.78),
            (0.62, 0.78),
            (0.82, 0.76),
            (0.28, 0.53),
            (0.50, 0.57),
            (0.72, 0.53),
            (0.18, 0.25),
            (0.50, 0.16),
            (0.82, 0.25),
        ]

        return posicions_reserva[
            index % len(posicions_reserva)
        ]

    def _dibuixar_jugadors(
        self,
        amplada: int,
        alcada: int,
    ) -> None:
        if self.canvas is None:
            return

        marge = 38
        amplada_util = amplada - 2 * marge
        alcada_util = alcada - 2 * marge

        for index, jugador in enumerate(
            self.dades_partit.jugadors
        ):
            posicio = (
                self.dades_partit.posicions[index]
                if index < len(
                    self.dades_partit.posicions
                )
                else ""
            )

            dorsal = (
                self.dades_partit.dorsals[index]
                if index < len(
                    self.dades_partit.dorsals
                )
                else str(index + 1)
            )

            x_normal, y_normal = self._obtenir_coordenades_posicio(
                posicio,
                index,
            )

            x = marge + amplada_util * x_normal
            y = marge + alcada_util * y_normal

            radi = 25

            seleccionat = (
                index == self.jugador_seleccionat
            )

            color_node = (
                self.COLOR_GROC
                if seleccionat
                else self.COLOR_VERD
            )

            contorn = (
                "#FFFFFF"
                if seleccionat
                else "#062219"
            )

            cercle = self.canvas.create_oval(
                x - radi,
                y - radi,
                x + radi,
                y + radi,
                fill=color_node,
                outline=contorn,
                width=4 if seleccionat else 3,
                tags=(
                    "jugador",
                    f"jugador_{index}",
                ),
            )

            text_dorsal = self.canvas.create_text(
                x,
                y,
                text=dorsal,
                fill="#04130E",
                font=(
                    "Arial",
                    12,
                    "bold",
                ),
                tags=(
                    "jugador",
                    f"jugador_{index}",
                ),
            )

            nom_curta = (
                jugador
                if len(jugador) <= 16
                else jugador[:14] + "…"
            )

            text_nom = self.canvas.create_text(
                x,
                y + 37,
                text=nom_curta,
                fill="#FFFFFF",
                font=(
                    "Arial",
                    10,
                    "bold",
                ),
                tags=(
                    "jugador",
                    f"jugador_{index}",
                ),
            )

            self.elements_jugadors[index] = {
                "cercle": cercle,
                "dorsal": text_dorsal,
                "nom": text_nom,
            }

            self.canvas.tag_bind(
                f"jugador_{index}",
                "<Button-1>",
                lambda event,
                i=index: self._seleccionar_jugador(i),
            )

            self.canvas.tag_bind(
                f"jugador_{index}",
                "<Enter>",
                lambda event: self.canvas.configure(
                    cursor="hand2"
                ),
            )

            self.canvas.tag_bind(
                f"jugador_{index}",
                "<Leave>",
                lambda event: self.canvas.configure(
                    cursor=""
                ),
            )

    # =====================================================
    # SELECCIÓ DEL JUGADOR
    # =====================================================

    def _seleccionar_jugador(
        self,
        index: int,
    ) -> None:
        self.jugador_seleccionat = index
        self._redibuixar_camp()
        self._mostrar_dades_jugador(index)

    # =====================================================
    # PANELL LATERAL
    # =====================================================

    def _netejar_panell_jugador(self) -> None:
        if self.panell_jugador is None:
            return

        for widget in self.panell_jugador.winfo_children():
            widget.destroy()

    def _mostrar_panell_inicial(self) -> None:
        self._netejar_panell_jugador()

        if self.panell_jugador is None:
            return

        ctk.CTkLabel(
            self.panell_jugador,
            text="⚽",
            font=ctk.CTkFont(size=54),
            text_color=self.COLOR_VERD,
        ).pack(
            pady=(75, 14),
        )

        ctk.CTkLabel(
            self.panell_jugador,
            text="Selecciona un jugador",
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack()

        ctk.CTkLabel(
            self.panell_jugador,
            text=(
                "Clica qualsevol node del camp per consultar "
                "les seves dades individuals i centralitats."
            ),
            font=ctk.CTkFont(size=13),
            text_color=self.COLOR_TEXT_SECUNDARI,
            justify="center",
            wraplength=310,
        ).pack(
            padx=25,
            pady=(8, 0),
        )

    def _mostrar_dades_jugador(
        self,
        index: int,
    ) -> None:
        self._netejar_panell_jugador()

        if self.panell_jugador is None:
            return

        estadistica = self._estadistica_jugador(
            index
        )

        if estadistica is None:
            self._mostrar_panell_inicial()
            return

        nom = estadistica.get(
            "jugador",
            "Jugador",
        )

        dorsal = estadistica.get(
            "dorsal",
            "",
        )

        posicio = estadistica.get(
            "posicio",
            "",
        )

        ctk.CTkLabel(
            self.panell_jugador,
            text=f"{dorsal}",
            width=64,
            height=64,
            corner_radius=32,
            fg_color=self.COLOR_GROC,
            text_color="#04130E",
            font=ctk.CTkFont(
                size=24,
                weight="bold",
            ),
        ).pack(
            pady=(22, 8),
        )

        ctk.CTkLabel(
            self.panell_jugador,
            text=nom,
            font=ctk.CTkFont(
                size=23,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack()

        ctk.CTkLabel(
            self.panell_jugador,
            text=posicio or "Posició no indicada",
            font=ctk.CTkFont(size=13),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            pady=(3, 16),
        )

        resum = ctk.CTkFrame(
            self.panell_jugador,
            fg_color=self.COLOR_TARGETA,
            corner_radius=16,
        )
        resum.pack(
            fill="x",
            padx=16,
            pady=(0, 12),
        )

        self._crear_fila_dada(
            resum,
            "Passades intentades",
            estadistica.get("intentades", 0),
            self.COLOR_TEXT,
        )

        self._crear_fila_dada(
            resum,
            "Passades bones",
            estadistica.get("bones", 0),
            self.COLOR_VERD,
        )

        self._crear_fila_dada(
            resum,
            "Passades dolentes",
            estadistica.get("dolentes", 0),
            self.COLOR_VERMELL,
        )

        self._crear_fila_dada(
            resum,
            "Passades rebudes",
            estadistica.get("rebudes", 0),
            self.COLOR_BLAU,
        )

        self._crear_fila_dada(
            resum,
            "Precisió",
            (
                f"{estadistica.get('precisio', 0.0):.1f} %"
            ),
            self.COLOR_GROC,
        )

        centralitats = ctk.CTkFrame(
            self.panell_jugador,
            fg_color=self.COLOR_TARGETA,
            corner_radius=16,
        )
        centralitats.pack(
            fill="x",
            padx=16,
            pady=(0, 12),
        )

        ctk.CTkLabel(
            centralitats,
            text="CENTRALITATS",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            padx=14,
            pady=(13, 5),
        )

        self._crear_fila_dada(
            centralitats,
            "Degree",
            f"{estadistica.get('degree', 0.0):.3f}",
            self.COLOR_BLAU,
        )

        self._crear_fila_dada(
            centralitats,
            "Betweenness",
            (
                f"{estadistica.get('betweenness', 0.0):.3f}"
            ),
            self.COLOR_LILA,
        )

        self._crear_fila_dada(
            centralitats,
            "Closeness",
            (
                f"{estadistica.get('closeness', 0.0):.3f}"
            ),
            self.COLOR_GROC,
        )

        self._crear_fila_dada(
            centralitats,
            "PageRank",
            (
                f"{estadistica.get('pagerank', 0.0):.3f}"
            ),
            self.COLOR_VERD,
        )

        jugador_connectat = (
            self._obtenir_jugador_mes_connectat(index)
        )

        connexio = ctk.CTkFrame(
            self.panell_jugador,
            fg_color=self.COLOR_TARGETA,
            corner_radius=16,
        )
        connexio.pack(
            fill="x",
            padx=16,
            pady=(0, 16),
        )

        ctk.CTkLabel(
            connexio,
            text="CONNEXIÓ PRINCIPAL",
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            pady=(13, 5),
        )

        ctk.CTkLabel(
            connexio,
            text=jugador_connectat,
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            pady=(0, 13),
        )

    def _crear_fila_dada(
        self,
        pare: ctk.CTkFrame,
        etiqueta: str,
        valor: Any,
        color: str,
    ) -> None:
        fila = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        fila.pack(
            fill="x",
            padx=14,
            pady=5,
        )

        ctk.CTkLabel(
            fila,
            text=etiqueta,
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(side="left")

        ctk.CTkLabel(
            fila,
            text=str(valor).replace(".", ","),
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
            text_color=color,
        ).pack(side="right")

    # =====================================================
    # CÀLCULS AUXILIARS
    # =====================================================

    def _estadistica_jugador(
        self,
        index: int,
    ) -> dict[str, Any] | None:
        for estadistica in self.estadistiques:
            if estadistica.get("index") == index:
                return estadistica

        if 0 <= index < len(self.estadistiques):
            return self.estadistiques[index]

        return None

    def _obtenir_jugador_mes_connectat(
        self,
        index: int,
    ) -> str:
        connexions: dict[int, int] = {}

        for passada in self.dades_partit.passades:
            if passada.resultat != "bona":
                continue

            if passada.desti is None:
                continue

            if passada.origen == index:
                connexions[passada.desti] = (
                    connexions.get(
                        passada.desti,
                        0,
                    )
                    + 1
                )

            elif passada.desti == index:
                connexions[passada.origen] = (
                    connexions.get(
                        passada.origen,
                        0,
                    )
                    + 1
                )

        if not connexions:
            return "Sense connexions registrades"

        index_connectat = max(
            connexions,
            key=connexions.get,
        )

        nombre_passades = connexions[index_connectat]

        if (
            index_connectat < 0
            or index_connectat
            >= len(self.dades_partit.jugadors)
        ):
            return "Sense dades"

        nom = self.dades_partit.jugadors[
            index_connectat
        ]

        return (
            f"{nom} · {nombre_passades} passades"
        )