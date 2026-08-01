from __future__ import annotations

from pathlib import Path
from typing import Callable, Any

import customtkinter as ctk

from utils.history_manager import llegir_partit


class ComparisonView(ctk.CTkFrame):
    """
    Pantalla de comparació entre dos partits guardats.
    """

    COLOR_FONS = "#061B15"
    COLOR_CAPCALERA = "#0B2A21"
    COLOR_PANELL = "#0D2A22"
    COLOR_TARGETA = "#12382E"

    COLOR_VERD = "#22C55E"
    COLOR_BLAU = "#38BDF8"
    COLOR_GROC = "#FACC15"
    COLOR_VERMELL = "#EF4444"
    COLOR_LILA = "#A78BFA"

    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"
    COLOR_LINIA = "#315B4D"

    def __init__(
        self,
        master,
        ruta_partit_1: str,
        ruta_partit_2: str,
        tornar_historial: Callable[[], None],
        tornar_inici: Callable[[], None],
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.ruta_partit_1 = Path(ruta_partit_1)
        self.ruta_partit_2 = Path(ruta_partit_2)

        self.tornar_historial = tornar_historial
        self.tornar_inici = tornar_inici

        self.dades_1 = llegir_partit(
            self.ruta_partit_1
        )

        self.dades_2 = llegir_partit(
            self.ruta_partit_2
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._crear_capcalera()
        self._crear_contingut()

    # =====================================================
    # CAPÇALERA
    # =====================================================

    def _crear_capcalera(self) -> None:
        capcalera = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_CAPCALERA,
            corner_radius=0,
            height=88,
        )
        capcalera.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        capcalera.grid_propagate(False)
        capcalera.grid_columnconfigure(0, weight=1)

        bloc_titol = ctk.CTkFrame(
            capcalera,
            fg_color="transparent",
        )
        bloc_titol.grid(
            row=0,
            column=0,
            sticky="w",
            padx=24,
            pady=14,
        )

        ctk.CTkLabel(
            bloc_titol,
            text="Comparació de partits",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            bloc_titol,
            text=(
                "Compara el rendiment col·lectiu "
                "i l'estructura de la xarxa"
            ),
            font=ctk.CTkFont(size=13),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(anchor="w", pady=(2, 0))

        boto_historial = ctk.CTkButton(
            capcalera,
            text="← HISTORIAL",
            command=self.tornar_historial,
            width=130,
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
        )
        boto_historial.grid(
            row=0,
            column=1,
            padx=(10, 6),
        )

        boto_inici = ctk.CTkButton(
            capcalera,
            text="INICI",
            command=self.tornar_inici,
            width=100,
            height=38,
            fg_color=self.COLOR_VERD,
            hover_color="#16A34A",
            text_color="#04130E",
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        )
        boto_inici.grid(
            row=0,
            column=2,
            padx=(6, 24),
        )

    # =====================================================
    # CONTINGUT PRINCIPAL
    # =====================================================

    def _crear_contingut(self) -> None:
        scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )
        scroll.grid(
            row=1,
            column=0,
            sticky="nsew",
        )
        scroll.grid_columnconfigure(0, weight=1)

        self._crear_presentacio_partits(
            scroll
        )

        self._crear_comparacio_global(
            scroll
        )

        self._crear_comparacio_jugadors(
            scroll
        )

        self._crear_conclusio(
            scroll
        )

    # =====================================================
    # PRESENTACIÓ DELS PARTITS
    # =====================================================

    def _crear_presentacio_partits(
        self,
        contenidor: ctk.CTkScrollableFrame,
    ) -> None:
        bloc = ctk.CTkFrame(
            contenidor,
            fg_color="transparent",
        )
        bloc.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(18, 10),
        )
        bloc.grid_columnconfigure(
            (0, 1),
            weight=1,
        )

        self._crear_targeta_partit(
            bloc,
            columna=0,
            titol="PARTIT 1",
            dades=self.dades_1,
            color=self.COLOR_BLAU,
        )

        self._crear_targeta_partit(
            bloc,
            columna=1,
            titol="PARTIT 2",
            dades=self.dades_2,
            color=self.COLOR_VERD,
        )

    def _crear_targeta_partit(
        self,
        contenidor: ctk.CTkFrame,
        columna: int,
        titol: str,
        dades: dict[str, Any],
        color: str,
    ) -> None:
        partit = dades.get("partit", {})

        equip = partit.get(
            "equip",
            "Equip",
        )

        rival = partit.get(
            "rival",
            "Rival",
        )

        data = partit.get(
            "data_partit",
            "Sense data",
        )

        competicio = partit.get(
            "competicio",
            "",
        )

        sistema = partit.get(
            "sistema",
            "",
        )

        targeta = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
            border_width=1,
            border_color=color,
        )
        targeta.grid(
            row=0,
            column=columna,
            sticky="nsew",
            padx=8,
        )

        ctk.CTkLabel(
            targeta,
            text=titol,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=color,
        ).pack(
            anchor="w",
            padx=20,
            pady=(16, 4),
        )

        ctk.CTkLabel(
            targeta,
            text=f"{equip}  —  {rival}",
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(
            anchor="w",
            padx=20,
        )

        detall = data

        if competicio:
            detall += f" · {competicio}"

        if sistema:
            detall += f" · {sistema}"

        ctk.CTkLabel(
            targeta,
            text=detall,
            font=ctk.CTkFont(size=13),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            padx=20,
            pady=(5, 17),
        )

    # =====================================================
    # COMPARACIÓ GLOBAL
    # =====================================================

    def _crear_comparacio_global(
        self,
        contenidor: ctk.CTkScrollableFrame,
    ) -> None:
        seccio = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        seccio.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=10,
        )
        seccio.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            seccio,
            text="COMPARACIÓ GLOBAL",
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
            pady=(16, 8),
        )

        taula = ctk.CTkFrame(
            seccio,
            fg_color="transparent",
        )
        taula.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=(0, 18),
        )

        taula.grid_columnconfigure(0, weight=2)
        taula.grid_columnconfigure(
            (1, 2, 3),
            weight=1,
        )

        self._crear_capcalera_taula(
            taula
        )

        resum_1 = self.dades_1.get(
            "resum",
            {},
        )

        resum_2 = self.dades_2.get(
            "resum",
            {},
        )

        files = [
            (
                "Passades totals",
                resum_1.get("total", 0),
                resum_2.get("total", 0),
                "enter",
            ),
            (
                "Passades bones",
                resum_1.get("bones", 0),
                resum_2.get("bones", 0),
                "enter",
            ),
            (
                "Passades dolentes",
                resum_1.get("dolentes", 0),
                resum_2.get("dolentes", 0),
                "enter_invers",
            ),
            (
                "Precisió",
                resum_1.get("precisio", 0.0),
                resum_2.get("precisio", 0.0),
                "percentatge",
            ),
            (
                "Jugadors participants",
                len(
                    self.dades_1
                    .get("alineacio", {})
                    .get("jugadors", [])
                ),
                len(
                    self.dades_2
                    .get("alineacio", {})
                    .get("jugadors", [])
                ),
                "enter",
            ),
        ]

        for index, fila in enumerate(
            files,
            start=1,
        ):
            self._crear_fila_comparacio(
                taula,
                fila=index,
                etiqueta=fila[0],
                valor_1=fila[1],
                valor_2=fila[2],
                tipus=fila[3],
            )

    def _crear_capcalera_taula(
        self,
        taula: ctk.CTkFrame,
    ) -> None:
        capcaleres = [
            "INDICADOR",
            "PARTIT 1",
            "PARTIT 2",
            "DIFERÈNCIA",
        ]

        for columna, text in enumerate(
            capcaleres
        ):
            ctk.CTkLabel(
                taula,
                text=text,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).grid(
                row=0,
                column=columna,
                sticky="w"
                if columna == 0
                else "",
                padx=10,
                pady=9,
            )

    def _crear_fila_comparacio(
        self,
        taula: ctk.CTkFrame,
        fila: int,
        etiqueta: str,
        valor_1: int | float,
        valor_2: int | float,
        tipus: str,
    ) -> None:
        color_fons = (
            "#103229"
            if fila % 2 == 0
            else "#0D2A22"
        )

        for columna in range(4):
            fons = ctk.CTkFrame(
                taula,
                fg_color=color_fons,
                corner_radius=0,
                height=44,
            )
            fons.grid(
                row=fila,
                column=columna,
                sticky="nsew",
                padx=1,
                pady=1,
            )
            fons.grid_propagate(False)

            if columna == 0:
                text = etiqueta
                color = self.COLOR_TEXT
                anchor = "w"

            elif columna == 1:
                text = self._formatar_valor(
                    valor_1,
                    tipus,
                )
                color = self.COLOR_BLAU
                anchor = "center"

            elif columna == 2:
                text = self._formatar_valor(
                    valor_2,
                    tipus,
                )
                color = self.COLOR_VERD
                anchor = "center"

            else:
                diferencia = (
                    float(valor_2)
                    - float(valor_1)
                )

                text = self._formatar_diferencia(
                    diferencia,
                    tipus,
                )

                color = self._color_diferencia(
                    diferencia,
                    tipus,
                )

                anchor = "center"

            ctk.CTkLabel(
                fons,
                text=text,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold"
                    if columna > 0
                    else "normal",
                ),
                text_color=color,
                anchor=anchor,
            ).pack(
                fill="both",
                expand=True,
                padx=10,
            )

    # =====================================================
    # COMPARACIÓ DE JUGADORS
    # =====================================================

    def _crear_comparacio_jugadors(
        self,
        contenidor: ctk.CTkScrollableFrame,
    ) -> None:
        seccio = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        seccio.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=10,
        )
        seccio.grid_columnconfigure(
            (0, 1),
            weight=1,
        )

        ctk.CTkLabel(
            seccio,
            text="JUGADORS DESTACATS",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=18,
            pady=(16, 10),
        )

        destacats_1 = (
            self._obtenir_jugadors_destacats(
                self.dades_1
            )
        )

        destacats_2 = (
            self._obtenir_jugadors_destacats(
                self.dades_2
            )
        )

        self._crear_panell_destacats(
            seccio,
            columna=0,
            titol="PARTIT 1",
            destacats=destacats_1,
            color=self.COLOR_BLAU,
        )

        self._crear_panell_destacats(
            seccio,
            columna=1,
            titol="PARTIT 2",
            destacats=destacats_2,
            color=self.COLOR_VERD,
        )

    def _crear_panell_destacats(
        self,
        contenidor: ctk.CTkFrame,
        columna: int,
        titol: str,
        destacats: dict[str, dict[str, Any]],
        color: str,
    ) -> None:
        panell = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_TARGETA,
            corner_radius=16,
        )
        panell.grid(
            row=1,
            column=columna,
            sticky="nsew",
            padx=12,
            pady=(0, 18),
        )

        ctk.CTkLabel(
            panell,
            text=titol,
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
            text_color=color,
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 8),
        )

        elements = [
            (
                "Més passades bones",
                destacats.get(
                    "mes_bones",
                    {},
                ),
                "bones",
            ),
            (
                "Més passades rebudes",
                destacats.get(
                    "mes_rebudes",
                    {},
                ),
                "rebudes",
            ),
            (
                "Més precisió",
                destacats.get(
                    "mes_precis",
                    {},
                ),
                "precisio",
            ),
            (
                "Més errors",
                destacats.get(
                    "mes_errors",
                    {},
                ),
                "dolentes",
            ),
        ]

        for etiqueta, jugador, camp in elements:
            nom = jugador.get(
                "jugador",
                "Sense dades",
            )

            valor = jugador.get(
                camp,
                0,
            )

            if camp == "precisio":
                valor_text = f"{valor:.1f} %"
            else:
                valor_text = str(valor)

            fila = ctk.CTkFrame(
                panell,
                fg_color="transparent",
            )
            fila.pack(
                fill="x",
                padx=16,
                pady=6,
            )

            ctk.CTkLabel(
                fila,
                text=etiqueta,
                font=ctk.CTkFont(size=12),
                text_color=self.COLOR_TEXT_SECUNDARI,
            ).pack(side="left")

            ctk.CTkLabel(
                fila,
                text=f"{nom} · {valor_text}",
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT,
            ).pack(side="right")

    # =====================================================
    # CONCLUSIÓ AUTOMÀTICA
    # =====================================================

    def _crear_conclusio(
        self,
        contenidor: ctk.CTkScrollableFrame,
    ) -> None:
        seccio = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        seccio.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(10, 22),
        )

        ctk.CTkLabel(
            seccio,
            text="INTERPRETACIÓ AUTOMÀTICA",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 8),
        )

        conclusio = self._generar_conclusio()

        ctk.CTkLabel(
            seccio,
            text=conclusio,
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

    # =====================================================
    # CÀLCULS
    # =====================================================

    def _obtenir_jugadors_destacats(
        self,
        dades: dict[str, Any],
    ) -> dict[str, dict[str, Any]]:
        estadistiques = dades.get(
            "estadistiques_jugadors",
            [],
        )

        if not estadistiques:
            return {
                "mes_bones": {},
                "mes_rebudes": {},
                "mes_precis": {},
                "mes_errors": {},
            }

        jugadors_amb_intents = [
            jugador
            for jugador in estadistiques
            if jugador.get("intentades", 0) > 0
        ]

        return {
            "mes_bones": max(
                estadistiques,
                key=lambda jugador: jugador.get(
                    "bones",
                    0,
                ),
            ),
            "mes_rebudes": max(
                estadistiques,
                key=lambda jugador: jugador.get(
                    "rebudes",
                    0,
                ),
            ),
            "mes_precis": max(
                jugadors_amb_intents
                if jugadors_amb_intents
                else estadistiques,
                key=lambda jugador: jugador.get(
                    "precisio",
                    0,
                ),
            ),
            "mes_errors": max(
                estadistiques,
                key=lambda jugador: jugador.get(
                    "dolentes",
                    0,
                ),
            ),
        }

    def _generar_conclusio(self) -> str:
        resum_1 = self.dades_1.get(
            "resum",
            {},
        )

        resum_2 = self.dades_2.get(
            "resum",
            {},
        )

        partit_1 = self.dades_1.get(
            "partit",
            {},
        )

        partit_2 = self.dades_2.get(
            "partit",
            {},
        )

        rival_1 = partit_1.get(
            "rival",
            "el rival del primer partit",
        )

        rival_2 = partit_2.get(
            "rival",
            "el rival del segon partit",
        )

        total_1 = resum_1.get("total", 0)
        total_2 = resum_2.get("total", 0)

        precisio_1 = resum_1.get(
            "precisio",
            0.0,
        )

        precisio_2 = resum_2.get(
            "precisio",
            0.0,
        )

        diferencia_passades = total_2 - total_1
        diferencia_precisio = precisio_2 - precisio_1

        frases = []

        if diferencia_passades > 0:
            frases.append(
                f"En el partit contra {rival_2}, "
                f"l'equip va registrar {diferencia_passades} "
                "passades més que en el partit anterior."
            )

        elif diferencia_passades < 0:
            frases.append(
                f"En el partit contra {rival_2}, "
                f"l'equip va registrar "
                f"{abs(diferencia_passades)} passades menys "
                f"que contra {rival_1}."
            )

        else:
            frases.append(
                "Els dos partits presenten el mateix nombre "
                "total de passades."
            )

        if diferencia_precisio > 0:
            frases.append(
                "La precisió també va millorar "
                f"{diferencia_precisio:.1f} punts percentuals."
            )

        elif diferencia_precisio < 0:
            frases.append(
                "Tot i això, la precisió va disminuir "
                f"{abs(diferencia_precisio):.1f} "
                "punts percentuals."
            )

        else:
            frases.append(
                "La precisió de passada es va mantenir igual."
            )

        destacats_1 = self._obtenir_jugadors_destacats(
            self.dades_1
        )

        destacats_2 = self._obtenir_jugadors_destacats(
            self.dades_2
        )

        jugador_1 = destacats_1.get(
            "mes_bones",
            {},
        ).get(
            "jugador",
            "cap jugador",
        )

        jugador_2 = destacats_2.get(
            "mes_bones",
            {},
        ).get(
            "jugador",
            "cap jugador",
        )

        if jugador_1 == jugador_2:
            frases.append(
                f"{jugador_1} va ser el jugador amb més "
                "passades bones en tots dos partits."
            )

        else:
            frases.append(
                f"El principal passador va canviar de "
                f"{jugador_1} a {jugador_2}, fet que pot "
                "indicar una modificació en l'organització "
                "del joc."
            )

        return " ".join(frases)

    # =====================================================
    # FORMAT
    # =====================================================

    def _formatar_valor(
        self,
        valor: int | float,
        tipus: str,
    ) -> str:
        if tipus == "percentatge":
            return f"{float(valor):.1f} %"

        return str(int(valor))

    def _formatar_diferencia(
        self,
        diferencia: float,
        tipus: str,
    ) -> str:
        signe = "+" if diferencia > 0 else ""

        if tipus == "percentatge":
            return f"{signe}{diferencia:.1f} %"

        return f"{signe}{int(diferencia)}"

    def _color_diferencia(
        self,
        diferencia: float,
        tipus: str,
    ) -> str:
        if diferencia == 0:
            return self.COLOR_TEXT_SECUNDARI

        if tipus == "enter_invers":
            return (
                self.COLOR_VERD
                if diferencia < 0
                else self.COLOR_VERMELL
            )

        return (
            self.COLOR_VERD
            if diferencia > 0
            else self.COLOR_VERMELL
        )
    