from __future__ import annotations

from tkinter import messagebox
from typing import Any, Callable

import customtkinter as ctk
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from models.match_data import MatchData
from utils.exporters import (
    exportar_excel,
    exportar_graf_png,
    exportar_historial_csv,
    exportar_tots_els_formats,
)
from utils.graph_utils import (
    calcular_mides_nodes,
    crear_graf_passades,
    obtenir_estadistiques_completes,
    obtenir_etiquetes_nodes,
    obtenir_jugador_amb_mes_errors,
    obtenir_jugador_amb_mes_passades_bones,
    obtenir_jugador_amb_mes_passades_rebudes,
    obtenir_jugador_mes_influent,
    obtenir_pesos_arestes,
    obtenir_posicions_graf,
    obtenir_resum_xarxa,
)
from views.tactical import TacticalView


class ResultsView(ctk.CTkFrame):
    """
    Pantalla de resultats organitzada en pestanyes.

    Inclou:
    - resum general;
    - graf relacional;
    - vista tàctica;
    - estadístiques i centralitats;
    - interpretació automàtica;
    - exportació dels resultats.
    """

    COLOR_FONS = "#061B15"
    COLOR_CAPCALERA = "#0A241C"
    COLOR_PANELL = "#0D2A22"
    COLOR_PANELL_CLAR = "#12372D"
    COLOR_TARGETA = "#143C31"

    COLOR_VERD = "#22C55E"
    COLOR_VERD_FOSC = "#15803D"
    COLOR_VERMELL = "#EF4444"
    COLOR_GROC = "#FACC15"
    COLOR_BLAU = "#38BDF8"
    COLOR_LILA = "#A78BFA"

    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"
    COLOR_LINIA = "#315B4D"

    def __init__(
        self,
        master,
        dades_partit: MatchData,
        tornar_partit: Callable[[], None],
        nou_partit: Callable[[], None],
        tornar_inici: Callable[[], None],
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.dades_partit = dades_partit
        self.tornar_partit = tornar_partit
        self.nou_partit = nou_partit
        self.tornar_inici = tornar_inici

        # Es calculen una sola vegada.
        self.estadistiques = obtenir_estadistiques_completes(
            self.dades_partit
        )

        self.resum_xarxa = obtenir_resum_xarxa(
            self.dades_partit
        )

        self.pagines: dict[str, ctk.CTkFrame] = {}
        self.botons_pestanyes: dict[str, ctk.CTkButton] = {}

        self.pestanya_actual = "Resum"

        self.figura_graf = None
        self.canvas_matplotlib = None
        self.graf_creat = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._crear_capcalera()
        self._crear_barra_pestanyes()
        self._crear_contenidor_pagines()
        self._crear_pagines()

        self.mostrar_pestanya("Resum")

    # =====================================================
    # CAPÇALERA
    # =====================================================

    def _crear_capcalera(self) -> None:
        capcalera = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_CAPCALERA,
            corner_radius=0,
            height=86,
        )
        capcalera.grid(
            row=0,
            column=0,
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
            text="Resultats del partit",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(anchor="w")

        detall = (
            f"{self.dades_partit.equip}  —  "
            f"{self.dades_partit.rival}"
        )

        if self.dades_partit.data_partit:
            detall += f" · {self.dades_partit.data_partit}"

        if self.dades_partit.sistema:
            detall += f" · {self.dades_partit.sistema}"

        ctk.CTkLabel(
            bloc_text,
            text=detall,
            font=ctk.CTkFont(size=13),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            pady=(3, 0),
        )

        bloc_botons = ctk.CTkFrame(
            capcalera,
            fg_color="transparent",
        )
        bloc_botons.grid(
            row=0,
            column=1,
            padx=24,
        )

        ctk.CTkButton(
            bloc_botons,
            text="← TORNAR AL PARTIT",
            command=self.tornar_partit,
            width=165,
            height=39,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color=self.COLOR_LINIA,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=0,
            padx=(0, 7),
        )

        ctk.CTkButton(
            bloc_botons,
            text="INICI",
            command=self.tornar_inici,
            width=90,
            height=39,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color=self.COLOR_LINIA,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            padx=7,
        )

        ctk.CTkButton(
            bloc_botons,
            text="NOU PARTIT",
            command=self.confirmar_nou_partit,
            width=125,
            height=39,
            fg_color=self.COLOR_VERD,
            hover_color=self.COLOR_VERD_FOSC,
            text_color="#04130E",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            padx=(7, 0),
        )

    # =====================================================
    # BARRA DE PESTANYES
    # =====================================================

    def _crear_barra_pestanyes(self) -> None:
        barra = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_PANELL,
            corner_radius=0,
            height=62,
        )
        barra.grid(
            row=1,
            column=0,
            sticky="ew",
        )
        barra.grid_propagate(False)

        pestanyes = [
            ("Resum", "⚽"),
            ("Graf", "◉"),
            ("Vista tàctica", "▱"),
            ("Estadístiques", "▦"),
            ("Anàlisi", "✦"),
            ("Exportar", "⇩"),
        ]

        for columna, (nom, icona) in enumerate(pestanyes):
            barra.grid_columnconfigure(
                columna,
                weight=1,
            )

            boto = ctk.CTkButton(
                barra,
                text=f"{icona}  {nom.upper()}",
                command=lambda n=nom: self.mostrar_pestanya(n),
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color=self.COLOR_PANELL_CLAR,
                text_color=self.COLOR_TEXT_SECUNDARI,
                font=ctk.CTkFont(
                    size=11,
                    weight="bold",
                ),
            )
            boto.grid(
                row=0,
                column=columna,
                sticky="ew",
                padx=5,
                pady=10,
            )

            self.botons_pestanyes[nom] = boto

    # =====================================================
    # CONTENIDOR I PÀGINES
    # =====================================================

    def _crear_contenidor_pagines(self) -> None:
        self.contenidor_pagines = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )
        self.contenidor_pagines.grid(
            row=2,
            column=0,
            sticky="nsew",
        )
        self.contenidor_pagines.grid_columnconfigure(0, weight=1)
        self.contenidor_pagines.grid_rowconfigure(0, weight=1)

    def _crear_pagines(self) -> None:
        self._crear_pagina_resum()
        self._crear_pagina_graf()
        self._crear_pagina_tactica()
        self._crear_pagina_estadistiques()
        self._crear_pagina_analisi()
        self._crear_pagina_exportar()

    def _crear_pagina_base(
        self,
        nom: str,
    ) -> ctk.CTkFrame:
        pagina = ctk.CTkFrame(
            self.contenidor_pagines,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )
        pagina.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        pagina.grid_columnconfigure(0, weight=1)
        pagina.grid_rowconfigure(0, weight=1)

        self.pagines[nom] = pagina

        return pagina

    def mostrar_pestanya(
        self,
        nom: str,
    ) -> None:
        if nom not in self.pagines:
            return

        self.pestanya_actual = nom

        self.pagines[nom].tkraise()

        for nom_boto, boto in self.botons_pestanyes.items():
            if nom_boto == nom:
                boto.configure(
                    fg_color=self.COLOR_VERD,
                    hover_color=self.COLOR_VERD_FOSC,
                    text_color="#04130E",
                )
            else:
                boto.configure(
                    fg_color="transparent",
                    hover_color=self.COLOR_PANELL_CLAR,
                    text_color=self.COLOR_TEXT_SECUNDARI,
                )

        # El graf només es dibuixa la primera vegada que s'obre.
        if nom == "Graf" and not self.graf_creat:
            self.after(
                30,
                self._dibuixar_graf,
            )

    # =====================================================
    # PÀGINA RESUM
    # =====================================================

    def _crear_pagina_resum(self) -> None:
        pagina = self._crear_pagina_base("Resum")

        scroll = self._crear_scroll(
            pagina
        )

        self._crear_targetes_resum(
            scroll
        )

        self._crear_jugadors_destacats(
            scroll
        )

        self._crear_lectura_general(
            scroll
        )

    def _crear_targetes_resum(
        self,
        pare,
    ) -> None:
        seccio = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        seccio.pack(
            fill="x",
            pady=(0, 16),
        )

        for columna in range(6):
            seccio.grid_columnconfigure(
                columna,
                weight=1,
            )

        resum = self.dades_partit.resum_partit()

        targetes = [
            (
                "PASSADES TOTALS",
                resum.get("total", 0),
                self.COLOR_TEXT,
            ),
            (
                "BONES",
                resum.get("bones", 0),
                self.COLOR_VERD,
            ),
            (
                "DOLENTES",
                resum.get("dolentes", 0),
                self.COLOR_VERMELL,
            ),
            (
                "PRECISIÓ",
                f"{resum.get('precisio', 0.0):.1f} %",
                self.COLOR_GROC,
            ),
            (
                "CONNEXIONS",
                self.resum_xarxa.get("arestes", 0),
                self.COLOR_BLAU,
            ),
            (
                "DENSITAT",
                f"{self.resum_xarxa.get('densitat', 0.0):.3f}",
                self.COLOR_LILA,
            ),
        ]

        for columna, (titol, valor, color) in enumerate(targetes):
            targeta = ctk.CTkFrame(
                seccio,
                fg_color=self.COLOR_PANELL,
                corner_radius=15,
            )
            targeta.grid(
                row=0,
                column=columna,
                sticky="ew",
                padx=5,
            )

            ctk.CTkLabel(
                targeta,
                text=titol,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).pack(
                pady=(14, 4),
            )

            ctk.CTkLabel(
                targeta,
                text=str(valor).replace(".", ","),
                font=ctk.CTkFont(
                    size=22,
                    weight="bold",
                ),
                text_color=color,
            ).pack(
                pady=(0, 14),
            )

    def _crear_jugadors_destacats(
        self,
        pare,
    ) -> None:
        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="JUGADORS DESTACATS",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 10),
        )

        graella = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        graella.pack(
            fill="x",
            padx=12,
            pady=(0, 16),
        )

        for columna in range(4):
            graella.grid_columnconfigure(
                columna,
                weight=1,
            )

        elements = [
            (
                "MÉS INFLUENT",
                obtenir_jugador_mes_influent(
                    self.dades_partit
                ),
                "pagerank",
                self.COLOR_LILA,
            ),
            (
                "MÉS PASSADES BONES",
                obtenir_jugador_amb_mes_passades_bones(
                    self.dades_partit
                ),
                "bones",
                self.COLOR_VERD,
            ),
            (
                "MÉS PASSADES REBUDES",
                obtenir_jugador_amb_mes_passades_rebudes(
                    self.dades_partit
                ),
                "rebudes",
                self.COLOR_BLAU,
            ),
            (
                "MÉS ERRORS",
                obtenir_jugador_amb_mes_errors(
                    self.dades_partit
                ),
                "dolentes",
                self.COLOR_VERMELL,
            ),
        ]

        for columna, (titol, jugador, camp, color) in enumerate(
            elements
        ):
            targeta = ctk.CTkFrame(
                graella,
                fg_color=self.COLOR_TARGETA,
                corner_radius=14,
            )
            targeta.grid(
                row=0,
                column=columna,
                sticky="nsew",
                padx=5,
            )

            ctk.CTkLabel(
                targeta,
                text=titol,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).pack(
                pady=(13, 5),
            )

            if jugador:
                dorsal = jugador.get("dorsal", "")
                nom = jugador.get("jugador", "")

                nom_complet = (
                    f"{dorsal}. {nom}"
                    if dorsal
                    else nom
                )

                valor_original = jugador.get(
                    camp,
                    0,
                )

                if camp == "pagerank":
                    valor = f"{float(valor_original):.4f}"
                else:
                    valor = str(valor_original)

            else:
                nom_complet = "Sense dades"
                valor = "—"

            ctk.CTkLabel(
                targeta,
                text=nom_complet,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT,
                wraplength=210,
            ).pack(
                pady=(0, 4),
            )

            ctk.CTkLabel(
                targeta,
                text=valor.replace(".", ","),
                font=ctk.CTkFont(
                    size=19,
                    weight="bold",
                ),
                text_color=color,
            ).pack(
                pady=(0, 13),
            )

    def _crear_lectura_general(
        self,
        pare,
    ) -> None:
        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="LECTURA GENERAL DEL PARTIT",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 7),
        )

        ctk.CTkLabel(
            panell,
            text=self._generar_analisi_automatica(),
            font=ctk.CTkFont(size=14),
            text_color=self.COLOR_TEXT,
            justify="left",
            anchor="w",
            wraplength=1200,
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 16),
        )

    # =====================================================
    # PÀGINA GRAF
    # =====================================================

    def _crear_pagina_graf(self) -> None:
        pagina = self._crear_pagina_base("Graf")

        contenidor = ctk.CTkFrame(
            pagina,
            fg_color="transparent",
        )
        contenidor.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=16,
        )
        contenidor.grid_columnconfigure(0, weight=1)
        contenidor.grid_rowconfigure(1, weight=1)

        informacio = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=16,
        )
        informacio.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 10),
        )

        ctk.CTkLabel(
            informacio,
            text="GRAF RELACIONAL DE PASSADES",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 3),
        )

        ctk.CTkLabel(
            informacio,
            text=(
                "La distribució dels nodes mostra les relacions "
                "entre jugadors, no la seva ubicació física al camp."
            ),
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 13),
        )

        self.panell_graf = ctk.CTkFrame(
            contenidor,
            fg_color="#F3F4F6",
            corner_radius=16,
        )
        self.panell_graf.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

    def _dibuixar_graf(self) -> None:
        if self.graf_creat:
            return

        graf = crear_graf_passades(
            self.dades_partit
        )

        posicions = obtenir_posicions_graf(
            self.dades_partit
        )

        etiquetes = obtenir_etiquetes_nodes(
            self.dades_partit
        )

        pesos = obtenir_pesos_arestes(
            self.dades_partit
        )

        mides = calcular_mides_nodes(
            self.dades_partit
        )

        self.figura_graf = plt.Figure(
            figsize=(10, 6.5),
            dpi=100,
        )

        eix = self.figura_graf.add_subplot(111)

        self.figura_graf.patch.set_facecolor("#F3F4F6")
        eix.set_facecolor("#F3F4F6")

        if graf.number_of_nodes() == 0:
            eix.text(
                0.5,
                0.5,
                "No hi ha dades per construir el graf.",
                ha="center",
                va="center",
                fontsize=14,
            )

        else:
            nx.draw_networkx_nodes(
                graf,
                posicions,
                node_size=[
                    mides.get(node, 1200)
                    for node in graf.nodes
                ],
                node_color=self.COLOR_VERD,
                edgecolors="#071E17",
                linewidths=2,
                ax=eix,
            )

            if graf.number_of_edges() > 0:
                amplades = [
                    max(
                        1.0,
                        graf[origen][desti].get(
                            "weight",
                            1,
                        )
                        * 0.65,
                    )
                    for origen, desti in graf.edges
                ]

                nx.draw_networkx_edges(
                    graf,
                    posicions,
                    width=amplades,
                    arrows=True,
                    arrowsize=17,
                    edge_color="#475569",
                    connectionstyle="arc3,rad=0.08",
                    ax=eix,
                )

                nx.draw_networkx_edge_labels(
                    graf,
                    posicions,
                    edge_labels=pesos,
                    font_size=8,
                    rotate=False,
                    ax=eix,
                )

            nx.draw_networkx_labels(
                graf,
                posicions,
                labels=etiquetes,
                font_size=9,
                font_weight="bold",
                ax=eix,
            )

        eix.axis("off")
        self.figura_graf.tight_layout()

        self.canvas_matplotlib = FigureCanvasTkAgg(
            self.figura_graf,
            master=self.panell_graf,
        )

        self.canvas_matplotlib.draw()

        self.canvas_matplotlib.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8,
        )

        self.graf_creat = True

    # =====================================================
    # PÀGINA VISTA TÀCTICA
    # =====================================================

    def _crear_pagina_tactica(self) -> None:
        pagina = self._crear_pagina_base(
            "Vista tàctica"
        )

        vista = TacticalView(
            master=pagina,
            dades_partit=self.dades_partit,
            tornar_resultats=None,
        )
        vista.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

    # =====================================================
    # PÀGINA ESTADÍSTIQUES
    # =====================================================

    def _crear_pagina_estadistiques(self) -> None:
        pagina = self._crear_pagina_base(
            "Estadístiques"
        )

        scroll = self._crear_scroll(
            pagina
        )

        panell = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="ESTADÍSTIQUES INDIVIDUALS I CENTRALITATS",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=16,
            pady=(16, 4),
        )

        ctk.CTkLabel(
            panell,
            text=(
                "PB: passades bones · PD: passades dolentes · "
                "PR: passades rebudes"
            ),
            font=ctk.CTkFont(size=11),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12),
        )

        taula = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        taula.pack(
            fill="x",
            padx=12,
            pady=(0, 16),
        )

        capcaleres = [
            "Jugador",
            "PB",
            "PD",
            "PR",
            "Precisió",
            "Degree",
            "In-Deg",
            "Out-Deg",
            "Bet",
            "Clos",
            "PageRank",
        ]

        for columna, text in enumerate(capcaleres):
            taula.grid_columnconfigure(
                columna,
                weight=2 if columna == 0 else 1,
            )

            ctk.CTkLabel(
                taula,
                text=text,
                font=ctk.CTkFont(
                    size=9,
                    weight="bold",
                ),
                text_color=self.COLOR_GROC,
            ).grid(
                row=0,
                column=columna,
                sticky="ew",
                padx=2,
                pady=7,
            )

        for fila, jugador in enumerate(
            self.estadistiques,
            start=1,
        ):
            color_fons = (
                "#103229"
                if fila % 2 == 0
                else "#12372D"
            )

            dorsal = jugador.get("dorsal", "")
            nom = jugador.get("jugador", "")

            valors = [
                f"{dorsal}. {nom}" if dorsal else nom,
                str(jugador.get("bones", 0)),
                str(jugador.get("dolentes", 0)),
                str(jugador.get("rebudes", 0)),
                f"{jugador.get('precisio', 0.0):.1f} %",
                f"{jugador.get('degree', 0.0):.3f}",
                f"{jugador.get('in_degree', 0.0):.3f}",
                f"{jugador.get('out_degree', 0.0):.3f}",
                f"{jugador.get('betweenness', 0.0):.3f}",
                f"{jugador.get('closeness', 0.0):.3f}",
                f"{jugador.get('pagerank', 0.0):.3f}",
            ]

            for columna, valor in enumerate(valors):
                cella = ctk.CTkFrame(
                    taula,
                    fg_color=color_fons,
                    corner_radius=0,
                    height=40,
                )
                cella.grid(
                    row=fila,
                    column=columna,
                    sticky="nsew",
                    padx=1,
                    pady=1,
                )
                cella.grid_propagate(False)

                ctk.CTkLabel(
                    cella,
                    text=valor.replace(".", ","),
                    font=ctk.CTkFont(
                        size=10,
                        weight="bold"
                        if columna == 0
                        else "normal",
                    ),
                    text_color=self.COLOR_TEXT,
                ).pack(
                    fill="both",
                    expand=True,
                    padx=4,
                )

    # =====================================================
    # PÀGINA ANÀLISI
    # =====================================================

    def _crear_pagina_analisi(self) -> None:
        pagina = self._crear_pagina_base("Anàlisi")

        scroll = self._crear_scroll(
            pagina
        )

        panell = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="INTERPRETACIÓ AUTOMÀTICA",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(18, 7),
        )

        ctk.CTkLabel(
            panell,
            text=self._generar_analisi_automatica(),
            font=ctk.CTkFont(size=14),
            text_color=self.COLOR_TEXT,
            justify="left",
            anchor="w",
            wraplength=1200,
        ).pack(
            fill="x",
            padx=18,
            pady=(0, 18),
        )

        self._crear_liders_xarxa(
            scroll
        )

        self._crear_explicacio_metriques(
            scroll
        )

    def _crear_liders_xarxa(
        self,
        pare,
    ) -> None:
        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="LÍDERS DE LA XARXA",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 10),
        )

        graella = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        graella.pack(
            fill="x",
            padx=12,
            pady=(0, 16),
        )

        camps = [
            ("Degree", "degree", self.COLOR_BLAU),
            (
                "Betweenness",
                "betweenness",
                self.COLOR_LILA,
            ),
            (
                "Closeness",
                "closeness",
                self.COLOR_GROC,
            ),
            (
                "PageRank",
                "pagerank",
                self.COLOR_VERD,
            ),
        ]

        for columna, (titol, camp, color) in enumerate(camps):
            graella.grid_columnconfigure(
                columna,
                weight=1,
            )

            jugador = max(
                self.estadistiques,
                key=lambda element: element.get(
                    camp,
                    0.0,
                ),
                default=None,
            )

            targeta = ctk.CTkFrame(
                graella,
                fg_color=self.COLOR_TARGETA,
                corner_radius=14,
            )
            targeta.grid(
                row=0,
                column=columna,
                sticky="ew",
                padx=5,
            )

            ctk.CTkLabel(
                targeta,
                text=titol.upper(),
                font=ctk.CTkFont(
                    size=9,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).pack(
                pady=(13, 5),
            )

            if jugador:
                nom = jugador.get(
                    "jugador",
                    "Sense dades",
                )
                valor = (
                    f"{jugador.get(camp, 0.0):.4f}"
                )
            else:
                nom = "Sense dades"
                valor = "—"

            ctk.CTkLabel(
                targeta,
                text=nom,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT,
            ).pack()

            ctk.CTkLabel(
                targeta,
                text=valor.replace(".", ","),
                font=ctk.CTkFont(
                    size=19,
                    weight="bold",
                ),
                text_color=color,
            ).pack(
                pady=(4, 13),
            )

    def _crear_explicacio_metriques(
        self,
        pare,
    ) -> None:
        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="COM INTERPRETAR LES MÈTRIQUES",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 9),
        )

        explicacions = [
            (
                "Degree",
                "Nombre de connexions directes del jugador.",
            ),
            (
                "Betweenness",
                "Capacitat del jugador per actuar com a pont.",
            ),
            (
                "Closeness",
                "Facilitat per connectar amb tota la xarxa.",
            ),
            (
                "PageRank",
                "Influència segons la importància de les connexions.",
            ),
            (
                "Densitat",
                "Proporció de connexions utilitzades respecte de totes les possibles.",
            ),
        ]

        for titol, text in explicacions:
            fila = ctk.CTkFrame(
                panell,
                fg_color="transparent",
            )
            fila.pack(
                fill="x",
                padx=18,
                pady=5,
            )

            ctk.CTkLabel(
                fila,
                text=f"{titol}:",
                width=120,
                anchor="w",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                text_color=self.COLOR_GROC,
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=text,
                anchor="w",
                font=ctk.CTkFont(size=12),
                text_color=self.COLOR_TEXT,
            ).pack(
                side="left",
                fill="x",
                expand=True,
            )

        ctk.CTkLabel(
            panell,
            text="",
            height=6,
        ).pack()

    # =====================================================
    # PÀGINA EXPORTAR
    # =====================================================

    def _crear_pagina_exportar(self) -> None:
        pagina = self._crear_pagina_base("Exportar")

        scroll = self._crear_scroll(
            pagina
        )

        panell = ctk.CTkFrame(
            scroll,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        panell.pack(
            fill="x",
            pady=(0, 16),
        )

        ctk.CTkLabel(
            panell,
            text="EXPORTACIÓ DELS RESULTATS",
            font=ctk.CTkFont(
                size=15,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5),
        )

        ctk.CTkLabel(
            panell,
            text=(
                "Desa les estadístiques, l'historial "
                "i el graf del partit."
            ),
            font=ctk.CTkFont(size=12),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 15),
        )

        graella = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        graella.pack(
            fill="x",
            padx=14,
            pady=(0, 20),
        )

        for columna in range(2):
            graella.grid_columnconfigure(
                columna,
                weight=1,
            )

        botons = [
            (
                "EXPORTAR EXCEL",
                "Estadístiques generals i centralitats",
                self.COLOR_VERD,
                self.COLOR_VERD_FOSC,
                self.exportar_excel,
            ),
            (
                "EXPORTAR CSV",
                "Historial complet de les passades",
                self.COLOR_BLAU,
                "#0284C7",
                self.exportar_csv,
            ),
            (
                "EXPORTAR GRAF PNG",
                "Imatge del graf relacional",
                self.COLOR_LILA,
                "#7C3AED",
                self.exportar_png,
            ),
            (
                "EXPORTAR-HO TOT",
                "Excel, CSV i PNG",
                self.COLOR_GROC,
                "#EAB308",
                self.exportar_tot,
            ),
        ]

        for index, (
            titol,
            descripcio,
            color,
            hover,
            ordre,
        ) in enumerate(botons):
            targeta = ctk.CTkFrame(
                graella,
                fg_color=self.COLOR_TARGETA,
                corner_radius=15,
            )
            targeta.grid(
                row=index // 2,
                column=index % 2,
                sticky="nsew",
                padx=6,
                pady=6,
            )

            ctk.CTkLabel(
                targeta,
                text=titol,
                font=ctk.CTkFont(
                    size=13,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT,
            ).pack(
                anchor="w",
                padx=16,
                pady=(16, 4),
            )

            ctk.CTkLabel(
                targeta,
                text=descripcio,
                font=ctk.CTkFont(size=11),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).pack(
                anchor="w",
                padx=16,
                pady=(0, 12),
            )

            ctk.CTkButton(
                targeta,
                text=titol,
                command=ordre,
                height=41,
                fg_color=color,
                hover_color=hover,
                text_color="#04130E",
                font=ctk.CTkFont(
                    size=11,
                    weight="bold",
                ),
            ).pack(
                fill="x",
                padx=16,
                pady=(0, 16),
            )

    # =====================================================
    # ANÀLISI AUTOMÀTICA
    # =====================================================

    def _generar_analisi_automatica(self) -> str:
        resum = self.dades_partit.resum_partit()

        total = resum.get("total", 0)
        bones = resum.get("bones", 0)
        dolentes = resum.get("dolentes", 0)
        precisio = resum.get("precisio", 0.0)

        densitat = self.resum_xarxa.get(
            "densitat",
            0.0,
        )

        connexions = self.resum_xarxa.get(
            "arestes",
            0,
        )

        influent = obtenir_jugador_mes_influent(
            self.dades_partit
        )

        mes_bones = obtenir_jugador_amb_mes_passades_bones(
            self.dades_partit
        )

        mes_rebudes = (
            obtenir_jugador_amb_mes_passades_rebudes(
                self.dades_partit
            )
        )

        frases = [
            (
                f"L'equip ha registrat {total} passades: "
                f"{bones} de correctes i {dolentes} d'errònies."
            )
        ]

        if precisio >= 90:
            frases.append(
                f"La precisió del {precisio:.1f} % indica "
                "una circulació de pilota molt segura."
            )
        elif precisio >= 80:
            frases.append(
                f"La precisió del {precisio:.1f} % reflecteix "
                "una circulació generalment fiable."
            )
        elif precisio >= 70:
            frases.append(
                f"La precisió del {precisio:.1f} % és moderada "
                "i mostra marge de millora."
            )
        else:
            frases.append(
                f"La precisió del {precisio:.1f} % és baixa "
                "i evidencia dificultats per conservar la pilota."
            )

        frases.append(
            f"La xarxa conté {connexions} connexions diferents "
            f"i presenta una densitat de {densitat:.3f}."
        )

        if influent:
            frases.append(
                f"{influent.get('jugador', '')} és el jugador "
                "més influent segons el PageRank."
            )

        if mes_bones:
            frases.append(
                f"{mes_bones.get('jugador', '')} és qui ha "
                "completat més passades bones."
            )

        if mes_rebudes:
            frases.append(
                f"{mes_rebudes.get('jugador', '')} és qui "
                "ha rebut més passades."
            )

        return " ".join(frases)

    # =====================================================
    # EXPORTACIONS
    # =====================================================

    def exportar_excel(self) -> None:
        try:
            ruta = exportar_excel(
                self.dades_partit
            )

            messagebox.showinfo(
                "Exportació completada",
                f"Excel guardat a:\n\n{ruta}",
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No s'ha pogut exportar l'Excel:\n\n{error}",
            )

    def exportar_csv(self) -> None:
        try:
            ruta = exportar_historial_csv(
                self.dades_partit
            )

            messagebox.showinfo(
                "Exportació completada",
                f"CSV guardat a:\n\n{ruta}",
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No s'ha pogut exportar el CSV:\n\n{error}",
            )

    def exportar_png(self) -> None:
        try:
            ruta = exportar_graf_png(
                self.dades_partit
            )

            messagebox.showinfo(
                "Exportació completada",
                f"Graf PNG guardat a:\n\n{ruta}",
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No s'ha pogut exportar el graf:\n\n{error}",
            )

    def exportar_tot(self) -> None:
        try:
            resultats = exportar_tots_els_formats(
                self.dades_partit
            )

            text = "\n\n".join(
                f"{format_exportat.upper()}:\n{ruta}"
                for format_exportat, ruta in resultats.items()
            )

            messagebox.showinfo(
                "Exportació completada",
                text,
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                (
                    "No s'han pogut exportar "
                    f"tots els resultats:\n\n{error}"
                ),
            )

    # =====================================================
    # UTILITATS
    # =====================================================

    def _crear_scroll(
        self,
        pagina: ctk.CTkFrame,
    ) -> ctk.CTkScrollableFrame:
        scroll = ctk.CTkScrollableFrame(
            pagina,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=self.COLOR_VERD_FOSC,
            scrollbar_button_hover_color=self.COLOR_VERD,
        )
        scroll.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=20,
            pady=16,
        )

        return scroll

    def confirmar_nou_partit(self) -> None:
        resposta = messagebox.askyesno(
            "Nou partit",
            (
                "Vols començar un nou partit?\n\n"
                "El partit actual ja està guardat "
                "automàticament a l'historial."
            ),
        )

        if resposta:
            self.nou_partit()

    def netejar_figura(self) -> None:
        if self.canvas_matplotlib is not None:
            try:
                widget = (
                    self.canvas_matplotlib.get_tk_widget()
                )

                if widget.winfo_exists():
                    widget.destroy()

            except Exception:
                pass

            self.canvas_matplotlib = None

        if self.figura_graf is not None:
            plt.close(
                self.figura_graf
            )

            self.figura_graf = None

        self.graf_creat = False

    def destroy(self) -> None:
        self.netejar_figura()
        super().destroy()
        