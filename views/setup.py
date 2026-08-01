from __future__ import annotations

from datetime import date
from tkinter import messagebox

import customtkinter as ctk

from models.match_data import MatchData


# =========================================================
# PANTALLA DE CONFIGURACIÓ DEL PARTIT
# =========================================================

class SetupView(ctk.CTkFrame):
    """
    Pantalla destinada a configurar un partit abans de començar.

    Permet introduir:
    - equip;
    - rival;
    - competició;
    - data;
    - condició de local o visitant;
    - sistema tàctic;
    - dorsals;
    - noms dels onze jugadors;
    - posicions dels jugadors.

    També mostra una previsualització de l'alineació.
    """

    # =====================================================
    # COLORS GENERALS
    # =====================================================

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_PANELL_CLAR = "#12372D"
    COLOR_VERD = "#22C55E"
    COLOR_VERD_FOSC = "#15803D"
    COLOR_VERMELL = "#EF4444"
    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"
    COLOR_CAMP = "#167447"
    COLOR_LINIES = "#EAF7EF"

    # =====================================================
    # OPCIONS DISPONIBLES
    # =====================================================

    COMPETICIONS = [
        "Lliga",
        "Copa",
        "Amistós",
        "Torneig",
        "Champions",
        "Europa League",
        "Altres",
    ]

    SISTEMES = [
        "4-3-3",
        "4-4-2",
        "4-2-3-1",
        "3-5-2",
        "3-4-3",
        "5-3-2",
        "5-4-1",
    ]

    LOCAL_VISITANT = [
        "Local",
        "Visitant",
    ]

    POSICIONS = [
        "Porter",
        "Lateral dret",
        "Central dret",
        "Central esquerre",
        "Lateral esquerre",
        "Migcampista defensiu",
        "Migcampista centre",
        "Migcampista ofensiu",
        "Extrem dret",
        "Davanter centre",
        "Extrem esquerre",
        "Carriler dret",
        "Carriler esquerre",
        "Segon davanter",
    ]

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        master,
        dades_partit: MatchData,
        tornar_inici,
        començar_partit,
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.dades_partit = dades_partit
        self.tornar_inici = tornar_inici
        self.començar_partit = començar_partit

        # Variables generals del partit.
        self.variable_equip = ctk.StringVar(
            value=self.dades_partit.equip
        )

        self.variable_rival = ctk.StringVar(
            value=self.dades_partit.rival
        )

        self.variable_competicio = ctk.StringVar(
            value=(
                self.dades_partit.competicio
                if self.dades_partit.competicio
                else "Lliga"
            )
        )

        self.variable_data = ctk.StringVar(
            value=(
                self.dades_partit.data_partit
                if self.dades_partit.data_partit
                else date.today().strftime("%d/%m/%Y")
            )
        )

        self.variable_sistema = ctk.StringVar(
            value=(
                self.dades_partit.sistema
                if self.dades_partit.sistema
                else "4-3-3"
            )
        )

        self.variable_local_visitant = ctk.StringVar(
            value=(
                self.dades_partit.local_visitant
                if self.dades_partit.local_visitant
                else "Local"
            )
        )

        # Llistes d'elements corresponents als jugadors.
        self.entrades_dorsals: list[ctk.CTkEntry] = []
        self.entrades_jugadors: list[ctk.CTkEntry] = []
        self.menus_posicions: list[ctk.CTkOptionMenu] = []
        self.variables_posicions: list[ctk.StringVar] = []

        # Canvas de previsualització.
        self.canvas_camp = None

        self.crear_interficie()

    # =====================================================
    # CREACIÓ GENERAL DE LA INTERFÍCIE
    # =====================================================

    def crear_interficie(self) -> None:
        """
        Construeix l'estructura principal de la pantalla.
        """

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.crear_capçalera()

        cos = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        cos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(10, 25),
        )

        cos.grid_columnconfigure(0, weight=3)
        cos.grid_columnconfigure(1, weight=2)
        cos.grid_rowconfigure(0, weight=1)

        self.crear_panell_formulari(cos)
        self.crear_panell_previsualitzacio(cos)

    # =====================================================
    # CAPÇALERA
    # =====================================================

    def crear_capçalera(self) -> None:
        """
        Crea la part superior amb el títol i la descripció.
        """

        capçalera = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        capçalera.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=35,
            pady=(25, 10),
        )

        capçalera.grid_columnconfigure(0, weight=1)
        capçalera.grid_columnconfigure(1, weight=0)

        bloc_text = ctk.CTkFrame(
            capçalera,
            fg_color="transparent",
        )
        bloc_text.grid(
            row=0,
            column=0,
            sticky="w",
        )

        titol = ctk.CTkLabel(
            bloc_text,
            text="Configuració del partit",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=34,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        titol.pack(
            anchor="w",
        )

        subtitol = ctk.CTkLabel(
            bloc_text,
            text=(
                "Introdueix les dades generals i defineix "
                "l'alineació inicial de l'equip."
            ),
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=15,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol.pack(
            anchor="w",
            pady=(6, 0),
        )

        etiqueta_pas = ctk.CTkLabel(
            capçalera,
            text="PAS 1 DE 3",
            width=120,
            height=38,
            corner_radius=12,
            fg_color=self.COLOR_PANELL,
            text_color=self.COLOR_VERD,
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        etiqueta_pas.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # =====================================================
    # PANELL ESQUERRE: FORMULARI
    # =====================================================

    def crear_panell_formulari(self, pare) -> None:
        """
        Crea el formulari desplaçable amb totes les dades.
        """

        panell = ctk.CTkScrollableFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=22,
            scrollbar_button_color=self.COLOR_VERD_FOSC,
            scrollbar_button_hover_color=self.COLOR_VERD,
        )
        panell.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 14),
        )

        panell.grid_columnconfigure(0, weight=1)

        self.crear_dades_generals(panell)
        self.crear_separador(panell)
        self.crear_taula_jugadors(panell)
        self.crear_botons_inferiors(panell)

    # =====================================================
    # DADES GENERALS
    # =====================================================

    def crear_dades_generals(self, pare) -> None:
        """
        Crea els camps de dades generals del partit.
        """

        titol_seccio = ctk.CTkLabel(
            pare,
            text="DADES GENERALS",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        titol_seccio.pack(
            fill="x",
            padx=26,
            pady=(24, 16),
        )

        contenidor = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        contenidor.pack(
            fill="x",
            padx=26,
        )

        contenidor.grid_columnconfigure(0, weight=1)
        contenidor.grid_columnconfigure(1, weight=1)

        # Equip.
        bloc_equip = self.crear_bloc_camp(
            contenidor,
            titol="Nom de l'equip",
            fila=0,
            columna=0,
            padx=(0, 10),
        )

        entrada_equip = ctk.CTkEntry(
            bloc_equip,
            textvariable=self.variable_equip,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#245445",
            text_color=self.COLOR_TEXT,
            placeholder_text="Ex.: FC Barcelona",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        entrada_equip.pack(
            fill="x",
        )

        # Rival.
        bloc_rival = self.crear_bloc_camp(
            contenidor,
            titol="Rival",
            fila=0,
            columna=1,
            padx=(10, 0),
        )

        entrada_rival = ctk.CTkEntry(
            bloc_rival,
            textvariable=self.variable_rival,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#245445",
            text_color=self.COLOR_TEXT,
            placeholder_text="Ex.: Girona FC",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        entrada_rival.pack(
            fill="x",
        )

        # Competició.
        bloc_competicio = self.crear_bloc_camp(
            contenidor,
            titol="Competició",
            fila=1,
            columna=0,
            padx=(0, 10),
        )

        menu_competicio = ctk.CTkOptionMenu(
            bloc_competicio,
            variable=self.variable_competicio,
            values=self.COMPETICIONS,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            button_color=self.COLOR_VERD_FOSC,
            button_hover_color=self.COLOR_VERD,
            dropdown_fg_color=self.COLOR_PANELL,
            dropdown_hover_color=self.COLOR_PANELL_CLAR,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        menu_competicio.pack(
            fill="x",
        )

        # Data.
        bloc_data = self.crear_bloc_camp(
            contenidor,
            titol="Data del partit",
            fila=1,
            columna=1,
            padx=(10, 0),
        )

        entrada_data = ctk.CTkEntry(
            bloc_data,
            textvariable=self.variable_data,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#245445",
            text_color=self.COLOR_TEXT,
            placeholder_text="DD/MM/AAAA",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        entrada_data.pack(
            fill="x",
        )

        # Sistema.
        bloc_sistema = self.crear_bloc_camp(
            contenidor,
            titol="Sistema tàctic",
            fila=2,
            columna=0,
            padx=(0, 10),
        )

        menu_sistema = ctk.CTkOptionMenu(
            bloc_sistema,
            variable=self.variable_sistema,
            values=self.SISTEMES,
            command=self.actualitzar_previsualitzacio,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            button_color=self.COLOR_VERD_FOSC,
            button_hover_color=self.COLOR_VERD,
            dropdown_fg_color=self.COLOR_PANELL,
            dropdown_hover_color=self.COLOR_PANELL_CLAR,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        menu_sistema.pack(
            fill="x",
        )

        # Local o visitant.
        bloc_local_visitant = self.crear_bloc_camp(
            contenidor,
            titol="Condició",
            fila=2,
            columna=1,
            padx=(10, 0),
        )

        menu_local_visitant = ctk.CTkOptionMenu(
            bloc_local_visitant,
            variable=self.variable_local_visitant,
            values=self.LOCAL_VISITANT,
            height=44,
            corner_radius=11,
            fg_color=self.COLOR_PANELL_CLAR,
            button_color=self.COLOR_VERD_FOSC,
            button_hover_color=self.COLOR_VERD,
            dropdown_fg_color=self.COLOR_PANELL,
            dropdown_hover_color=self.COLOR_PANELL_CLAR,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
        )
        menu_local_visitant.pack(
            fill="x",
        )

    def crear_bloc_camp(
        self,
        pare,
        titol: str,
        fila: int,
        columna: int,
        padx,
    ):
        """
        Crea un bloc amb etiqueta i espai per a un camp.
        """

        bloc = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        bloc.grid(
            row=fila,
            column=columna,
            sticky="ew",
            padx=padx,
            pady=(0, 18),
        )

        etiqueta = ctk.CTkLabel(
            bloc,
            text=titol,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta.pack(
            fill="x",
            pady=(0, 7),
        )

        return bloc

    # =====================================================
    # SEPARADOR
    # =====================================================

    def crear_separador(self, pare) -> None:
        separador = ctk.CTkFrame(
            pare,
            height=2,
            fg_color="#20483D",
        )
        separador.pack(
            fill="x",
            padx=26,
            pady=(8, 20),
        )

    # =====================================================
    # TAULA DE JUGADORS
    # =====================================================

    def crear_taula_jugadors(self, pare) -> None:
        """
        Crea els camps dels onze jugadors titulars.
        """

        capçalera_seccio = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        capçalera_seccio.pack(
            fill="x",
            padx=26,
            pady=(0, 14),
        )

        capçalera_seccio.grid_columnconfigure(0, weight=1)
        capçalera_seccio.grid_columnconfigure(1, weight=0)

        bloc_titol = ctk.CTkFrame(
            capçalera_seccio,
            fg_color="transparent",
        )
        bloc_titol.grid(
            row=0,
            column=0,
            sticky="w",
        )

        titol = ctk.CTkLabel(
            bloc_titol,
            text="ALINEACIÓ TITULAR",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        titol.pack(
            anchor="w",
        )

        descripcio = ctk.CTkLabel(
            bloc_titol,
            text="Introdueix els onze jugadors que iniciaran el partit.",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        descripcio.pack(
            anchor="w",
            pady=(4, 0),
        )

        boto_numerar = ctk.CTkButton(
            capçalera_seccio,
            text="Numeració automàtica",
            command=self.assignar_dorsals_automatics,
            width=160,
            height=36,
            corner_radius=10,
            fg_color=self.COLOR_PANELL_CLAR,
            hover_color="#1B4A3D",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_numerar.grid(
            row=0,
            column=1,
            sticky="e",
        )

        taula = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        taula.pack(
            fill="x",
            padx=26,
        )

        taula.grid_columnconfigure(0, weight=0)
        taula.grid_columnconfigure(1, weight=0)
        taula.grid_columnconfigure(2, weight=1)
        taula.grid_columnconfigure(3, weight=1)

        self.crear_capçalera_taula(taula)

        posicions_inicials = self.obtenir_posicions_inicials(
            self.variable_sistema.get()
        )

        for index in range(11):
            self.crear_fila_jugador(
                taula,
                index=index,
                posicio_inicial=posicions_inicials[index],
            )

    def crear_capçalera_taula(self, pare) -> None:
        """
        Crea la capçalera de la taula de jugadors.
        """

        textos = [
            ("ORDRE", 0),
            ("DORSAL", 1),
            ("NOM DEL JUGADOR", 2),
            ("POSICIÓ", 3),
        ]

        for text, columna in textos:
            etiqueta = ctk.CTkLabel(
                pare,
                text=text,
                anchor="w",
                font=ctk.CTkFont(
                    family="Arial",
                    size=11,
                    weight="bold",
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            )
            etiqueta.grid(
                row=0,
                column=columna,
                sticky="ew",
                padx=6,
                pady=(0, 8),
            )

    def crear_fila_jugador(
        self,
        pare,
        index: int,
        posicio_inicial: str,
    ) -> None:
        """
        Crea una fila individual de jugador.
        """

        fila = index + 1

        etiqueta_numero = ctk.CTkLabel(
            pare,
            text=f"{index + 1:02d}",
            width=48,
            height=42,
            corner_radius=10,
            fg_color="#102F27",
            text_color=self.COLOR_VERD,
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        etiqueta_numero.grid(
            row=fila,
            column=0,
            padx=(0, 6),
            pady=5,
        )

        entrada_dorsal = ctk.CTkEntry(
            pare,
            width=76,
            height=42,
            justify="center",
            corner_radius=10,
            fg_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#245445",
            text_color=self.COLOR_TEXT,
            placeholder_text=str(index + 1),
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        entrada_dorsal.grid(
            row=fila,
            column=1,
            sticky="ew",
            padx=6,
            pady=5,
        )

        entrada_nom = ctk.CTkEntry(
            pare,
            height=42,
            corner_radius=10,
            fg_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#245445",
            text_color=self.COLOR_TEXT,
            placeholder_text=f"Jugador {index + 1}",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
            ),
        )
        entrada_nom.grid(
            row=fila,
            column=2,
            sticky="ew",
            padx=6,
            pady=5,
        )

        variable_posicio = ctk.StringVar(
            value=posicio_inicial
        )

        menu_posicio = ctk.CTkOptionMenu(
            pare,
            variable=variable_posicio,
            values=self.POSICIONS,
            height=42,
            corner_radius=10,
            fg_color=self.COLOR_PANELL_CLAR,
            button_color=self.COLOR_VERD_FOSC,
            button_hover_color=self.COLOR_VERD,
            dropdown_fg_color=self.COLOR_PANELL,
            dropdown_hover_color=self.COLOR_PANELL_CLAR,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
            ),
        )
        menu_posicio.grid(
            row=fila,
            column=3,
            sticky="ew",
            padx=(6, 0),
            pady=5,
        )

        self.entrades_dorsals.append(entrada_dorsal)
        self.entrades_jugadors.append(entrada_nom)
        self.variables_posicions.append(variable_posicio)
        self.menus_posicions.append(menu_posicio)

        self.carregar_dades_jugador_si_existeixen(
            index=index,
            entrada_dorsal=entrada_dorsal,
            entrada_nom=entrada_nom,
            variable_posicio=variable_posicio,
        )
    def carregar_dades_jugador_si_existeixen(
        self,
        index: int,
        entrada_dorsal,
        entrada_nom,
        variable_posicio,
    ) -> None:
        """
        Recupera les dades d'un jugador si el partit ja havia estat configurat.
        """

        if index < len(self.dades_partit.dorsals):
            dorsal = self.dades_partit.dorsals[index]

            if dorsal:
                entrada_dorsal.insert(
                    0,
                    dorsal,
                )

        if index < len(self.dades_partit.jugadors):
            nom = self.dades_partit.jugadors[index]

            if nom:
                entrada_nom.insert(
                    0,
                    nom,
                )

        if index < len(self.dades_partit.posicions):
            posicio = self.dades_partit.posicions[index]

            if posicio:
                variable_posicio.set(
                    posicio
                )

    # =====================================================
    # BOTONS INFERIORS DEL FORMULARI
    # =====================================================

    def crear_botons_inferiors(self, pare) -> None:
        """
        Crea els botons per tornar a l'inici o començar el partit.
        """

        separador = ctk.CTkFrame(
            pare,
            height=2,
            fg_color="#20483D",
        )
        separador.pack(
            fill="x",
            padx=26,
            pady=(24, 20),
        )

        contenidor_botons = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        contenidor_botons.pack(
            fill="x",
            padx=26,
            pady=(0, 28),
        )

        contenidor_botons.grid_columnconfigure(
            0,
            weight=1,
        )

        boto_tornar = ctk.CTkButton(
            contenidor_botons,
            text="← TORNAR A L'INICI",
            command=self.confirmar_tornada_inici,
            width=190,
            height=48,
            corner_radius=12,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL_CLAR,
            border_width=2,
            border_color="#365F54",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        boto_tornar.grid(
            row=0,
            column=0,
            sticky="w",
        )

        boto_començar = ctk.CTkButton(
            contenidor_botons,
            text="COMENÇAR PARTIT  →",
            command=self.validar_i_començar,
            width=220,
            height=48,
            corner_radius=12,
            fg_color=self.COLOR_VERD,
            hover_color=self.COLOR_VERD_FOSC,
            text_color="#04130E",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
        )
        boto_començar.grid(
            row=0,
            column=1,
            sticky="e",
        )

    # =====================================================
    # PANELL DRET: PREVISUALITZACIÓ
    # =====================================================

    def crear_panell_previsualitzacio(self, pare) -> None:
        """
        Crea el panell dret amb la previsualització tàctica.
        """

        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=22,
        )
        panell.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(14, 0),
        )

        panell.grid_columnconfigure(
            0,
            weight=1,
        )
        panell.grid_rowconfigure(
            2,
            weight=1,
        )

        etiqueta = ctk.CTkLabel(
            panell,
            text="PREVISUALITZACIÓ TÀCTICA",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        etiqueta.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=24,
            pady=(24, 5),
        )

        subtitol = ctk.CTkLabel(
            panell,
            text=(
                "Els jugadors es distribuiran automàticament "
                "segons el sistema seleccionat."
            ),
            anchor="w",
            justify="left",
            wraplength=380,
            font=ctk.CTkFont(
                family="Arial",
                size=13,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 16),
        )

        contenidor_camp = ctk.CTkFrame(
            panell,
            fg_color="#09251C",
            corner_radius=18,
        )
        contenidor_camp.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=24,
            pady=(0, 18),
        )

        contenidor_camp.grid_columnconfigure(
            0,
            weight=1,
        )
        contenidor_camp.grid_rowconfigure(
            0,
            weight=1,
        )

        self.canvas_camp = ctk.CTkCanvas(
            contenidor_camp,
            background=self.COLOR_CAMP,
            highlightthickness=0,
        )
        self.canvas_camp.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=14,
            pady=14,
        )

        self.canvas_camp.bind(
            "<Configure>",
            self.redibuixar_camp,
        )

        self.crear_resum_previsualitzacio(
            panell
        )

    def crear_resum_previsualitzacio(self, pare) -> None:
        """
        Mostra un petit resum del sistema i del nombre de jugadors.
        """

        resum = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL_CLAR,
            corner_radius=14,
        )
        resum.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 24),
        )

        resum.grid_columnconfigure(
            0,
            weight=1,
        )
        resum.grid_columnconfigure(
            1,
            weight=1,
        )

        bloc_sistema = ctk.CTkFrame(
            resum,
            fg_color="transparent",
        )
        bloc_sistema.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=16,
        )

        etiqueta_sistema = ctk.CTkLabel(
            bloc_sistema,
            text="SISTEMA",
            font=ctk.CTkFont(
                family="Arial",
                size=11,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta_sistema.pack()

        self.etiqueta_sistema_actual = ctk.CTkLabel(
            bloc_sistema,
            textvariable=self.variable_sistema,
            font=ctk.CTkFont(
                family="Arial",
                size=22,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        self.etiqueta_sistema_actual.pack(
            pady=(4, 0),
        )

        bloc_jugadors = ctk.CTkFrame(
            resum,
            fg_color="transparent",
        )
        bloc_jugadors.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=18,
            pady=16,
        )

        etiqueta_jugadors = ctk.CTkLabel(
            bloc_jugadors,
            text="TITULARS",
            font=ctk.CTkFont(
                family="Arial",
                size=11,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta_jugadors.pack()

        valor_jugadors = ctk.CTkLabel(
            bloc_jugadors,
            text="11",
            font=ctk.CTkFont(
                family="Arial",
                size=22,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        valor_jugadors.pack(
            pady=(4, 0),
        )

    # =====================================================
    # DIBUIX DEL CAMP
    # =====================================================

    def redibuixar_camp(self, event=None) -> None:
        """
        Redibuixa el camp quan canvia la mida del canvas.
        """

        if self.canvas_camp is None:
            return

        amplada = self.canvas_camp.winfo_width()
        alcada = self.canvas_camp.winfo_height()

        if amplada < 50 or alcada < 50:
            return

        self.dibuixar_camp(
            amplada=amplada,
            alcada=alcada,
        )

    def dibuixar_camp(
        self,
        amplada: int,
        alcada: int,
    ) -> None:
        """
        Dibuixa les línies del camp i els onze jugadors.
        """

        canvas = self.canvas_camp
        canvas.delete("all")

        marge = 24

        x1 = marge
        y1 = marge
        x2 = amplada - marge
        y2 = alcada - marge

        if x2 <= x1 or y2 <= y1:
            return

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=self.COLOR_LINIES,
            width=2,
        )

        centre_x = (
            x1 + x2
        ) / 2

        centre_y = (
            y1 + y2
        ) / 2

        canvas.create_line(
            x1,
            centre_y,
            x2,
            centre_y,
            fill=self.COLOR_LINIES,
            width=2,
        )

        radi_centre = min(
            x2 - x1,
            y2 - y1,
        ) * 0.11

        canvas.create_oval(
            centre_x - radi_centre,
            centre_y - radi_centre,
            centre_x + radi_centre,
            centre_y + radi_centre,
            outline=self.COLOR_LINIES,
            width=2,
        )

        canvas.create_oval(
            centre_x - 3,
            centre_y - 3,
            centre_x + 3,
            centre_y + 3,
            fill=self.COLOR_LINIES,
            outline=self.COLOR_LINIES,
        )

        amplada_area = (
            x2 - x1
        ) * 0.48

        alcada_area = (
            y2 - y1
        ) * 0.17

        canvas.create_rectangle(
            centre_x - amplada_area / 2,
            y1,
            centre_x + amplada_area / 2,
            y1 + alcada_area,
            outline=self.COLOR_LINIES,
            width=2,
        )

        canvas.create_rectangle(
            centre_x - amplada_area / 2,
            y2 - alcada_area,
            centre_x + amplada_area / 2,
            y2,
            outline=self.COLOR_LINIES,
            width=2,
        )

        amplada_area_petita = (
            x2 - x1
        ) * 0.24

        alcada_area_petita = (
            y2 - y1
        ) * 0.07

        canvas.create_rectangle(
            centre_x - amplada_area_petita / 2,
            y1,
            centre_x + amplada_area_petita / 2,
            y1 + alcada_area_petita,
            outline=self.COLOR_LINIES,
            width=2,
        )

        canvas.create_rectangle(
            centre_x - amplada_area_petita / 2,
            y2 - alcada_area_petita,
            centre_x + amplada_area_petita / 2,
            y2,
            outline=self.COLOR_LINIES,
            width=2,
        )

        self.dibuixar_jugadors(
            canvas=canvas,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )

    def dibuixar_jugadors(
        self,
        canvas,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> None:
        """
        Dibuixa els onze jugadors segons la formació seleccionada.
        """

        sistema = self.variable_sistema.get()

        coordenades = self.obtenir_coordenades_formacio(
            sistema
        )

        amplada = x2 - x1
        alcada = y2 - y1

        radi = max(
            17,
            min(
                amplada,
                alcada,
            ) * 0.038,
        )

        for index, coordenada in enumerate(
            coordenades
        ):
            proporcio_x, proporcio_y = coordenada

            x = x1 + amplada * proporcio_x
            y = y1 + alcada * proporcio_y

            dorsal = str(
                index + 1
            )

            if index < len(self.entrades_dorsals):
                dorsal_introduit = (
                    self.entrades_dorsals[index]
                    .get()
                    .strip()
                )

                if dorsal_introduit:
                    dorsal = dorsal_introduit

            canvas.create_oval(
                x - radi,
                y - radi,
                x + radi,
                y + radi,
                fill="#071E17",
                outline=self.COLOR_VERD,
                width=3,
            )

            canvas.create_text(
                x,
                y,
                text=dorsal,
                fill=self.COLOR_TEXT,
                font=(
                    "Arial",
                    11,
                    "bold",
                ),
            )

            nom_jugador = ""

            if index < len(self.entrades_jugadors):
                nom_jugador = (
                    self.entrades_jugadors[index]
                    .get()
                    .strip()
                )

            if nom_jugador:
                nom_curt = (
                    nom_jugador
                    if len(nom_jugador) <= 13
                    else nom_jugador[:12] + "…"
                )

                canvas.create_text(
                    x,
                    y + radi + 11,
                    text=nom_curt,
                    fill=self.COLOR_TEXT,
                    font=(
                        "Arial",
                        9,
                        "bold",
                    ),
                )

    # =====================================================
    # FORMACIONS
    # =====================================================

    def obtenir_coordenades_formacio(
        self,
        sistema: str,
    ) -> list[tuple[float, float]]:
        """
        Retorna les coordenades relatives dels jugadors.
        """

        formacions = {
            "4-3-3": [
                (0.50, 0.91),
                (0.17, 0.73),
                (0.39, 0.77),
                (0.61, 0.77),
                (0.83, 0.73),
                (0.26, 0.52),
                (0.50, 0.58),
                (0.74, 0.52),
                (0.18, 0.27),
                (0.50, 0.18),
                (0.82, 0.27),
            ],
            "4-4-2": [
                (0.50, 0.91),
                (0.17, 0.73),
                (0.39, 0.77),
                (0.61, 0.77),
                (0.83, 0.73),
                (0.17, 0.49),
                (0.39, 0.54),
                (0.61, 0.54),
                (0.83, 0.49),
                (0.38, 0.22),
                (0.62, 0.22),
            ],
            "4-2-3-1": [
                (0.50, 0.91),
                (0.17, 0.73),
                (0.39, 0.77),
                (0.61, 0.77),
                (0.83, 0.73),
                (0.37, 0.57),
                (0.63, 0.57),
                (0.18, 0.36),
                (0.50, 0.39),
                (0.82, 0.36),
                (0.50, 0.17),
            ],
            "3-5-2": [
                (0.50, 0.91),
                (0.25, 0.74),
                (0.50, 0.78),
                (0.75, 0.74),
                (0.12, 0.51),
                (0.32, 0.55),
                (0.50, 0.60),
                (0.68, 0.55),
                (0.88, 0.51),
                (0.38, 0.22),
                (0.62, 0.22),
            ],
            "3-4-3": [
                (0.50, 0.91),
                (0.25, 0.74),
                (0.50, 0.78),
                (0.75, 0.74),
                (0.17, 0.51),
                (0.39, 0.57),
                (0.61, 0.57),
                (0.83, 0.51),
                (0.18, 0.27),
                (0.50, 0.18),
                (0.82, 0.27),
            ],
            "5-3-2": [
                (0.50, 0.91),
                (0.11, 0.70),
                (0.30, 0.76),
                (0.50, 0.79),
                (0.70, 0.76),
                (0.89, 0.70),
                (0.27, 0.49),
                (0.50, 0.56),
                (0.73, 0.49),
                (0.38, 0.21),
                (0.62, 0.21),
            ],
            "5-4-1": [
                (0.50, 0.91),
                (0.11, 0.70),
                (0.30, 0.76),
                (0.50, 0.79),
                (0.70, 0.76),
                (0.89, 0.70),
                (0.17, 0.46),
                (0.39, 0.52),
                (0.61, 0.52),
                (0.83, 0.46),
                (0.50, 0.18),
            ],
        }

        return formacions.get(
            sistema,
            formacions["4-3-3"],
        )

    def obtenir_posicions_inicials(
        self,
        sistema: str,
    ) -> list[str]:
        """
        Retorna les posicions inicials segons el sistema tàctic.
        """

        posicions_per_sistema = {
            "4-3-3": [
                "Porter",
                "Lateral dret",
                "Central dret",
                "Central esquerre",
                "Lateral esquerre",
                "Migcampista centre",
                "Migcampista defensiu",
                "Migcampista centre",
                "Extrem dret",
                "Davanter centre",
                "Extrem esquerre",
            ],
            "4-4-2": [
                "Porter",
                "Lateral dret",
                "Central dret",
                "Central esquerre",
                "Lateral esquerre",
                "Extrem dret",
                "Migcampista centre",
                "Migcampista centre",
                "Extrem esquerre",
                "Davanter centre",
                "Segon davanter",
            ],
            "4-2-3-1": [
                "Porter",
                "Lateral dret",
                "Central dret",
                "Central esquerre",
                "Lateral esquerre",
                "Migcampista defensiu",
                "Migcampista defensiu",
                "Extrem dret",
                "Migcampista ofensiu",
                "Extrem esquerre",
                "Davanter centre",
            ],
            "3-5-2": [
                "Porter",
                "Central dret",
                "Central esquerre",
                "Central dret",
                "Carriler dret",
                "Migcampista centre",
                "Migcampista defensiu",
                "Migcampista centre",
                "Carriler esquerre",
                "Davanter centre",
                "Segon davanter",
            ],
            "3-4-3": [
                "Porter",
                "Central dret",
                "Central esquerre",
                "Central dret",
                "Carriler dret",
                "Migcampista centre",
                "Migcampista centre",
                "Carriler esquerre",
                "Extrem dret",
                "Davanter centre",
                "Extrem esquerre",
            ],
            "5-3-2": [
                "Porter",
                "Carriler dret",
                "Central dret",
                "Central esquerre",
                "Central dret",
                "Carriler esquerre",
                "Migcampista centre",
                "Migcampista defensiu",
                "Migcampista centre",
                "Davanter centre",
                "Segon davanter",
            ],
            "5-4-1": [
                "Porter",
                "Carriler dret",
                "Central dret",
                "Central esquerre",
                "Central dret",
                "Carriler esquerre",
                "Extrem dret",
                "Migcampista centre",
                "Migcampista centre",
                "Extrem esquerre",
                "Davanter centre",
            ],
        }

        return posicions_per_sistema.get(
            sistema,
            posicions_per_sistema["4-3-3"],
        )

    def actualitzar_previsualitzacio(
        self,
        sistema_seleccionat: str | None = None,
    ) -> None:
        """
        Actualitza les posicions i redibuixa el camp.
        """

        sistema = (
            sistema_seleccionat
            if sistema_seleccionat
            else self.variable_sistema.get()
        )

        noves_posicions = self.obtenir_posicions_inicials(
            sistema
        )

        for index, variable in enumerate(
            self.variables_posicions
        ):
            if index < len(noves_posicions):
                variable.set(
                    noves_posicions[index]
                )

        self.redibuixar_camp()

    # =====================================================
    # DORSALS
    # =====================================================

    def assignar_dorsals_automatics(self) -> None:
        """
        Assigna els dorsals de l'1 a l'11.
        """

        for index, entrada in enumerate(
            self.entrades_dorsals,
            start=1,
        ):
            entrada.delete(
                0,
                "end",
            )

            entrada.insert(
                0,
                str(index),
            )

        self.redibuixar_camp()

    # =====================================================
    # OBTENCIÓ DE DADES
    # =====================================================

    def obtenir_dorsals(self) -> list[str]:
        return [
            entrada.get().strip()
            for entrada in self.entrades_dorsals
        ]

    def obtenir_jugadors(self) -> list[str]:
        return [
            entrada.get().strip()
            for entrada in self.entrades_jugadors
        ]

    def obtenir_posicions(self) -> list[str]:
        return [
            variable.get().strip()
            for variable in self.variables_posicions
        ]

    # =====================================================
    # VALIDACIÓ
    # =====================================================

    def validar_formulari(
        self,
    ) -> tuple[bool, str]:
        """
        Comprova totes les dades abans de començar.
        """

        equip = self.variable_equip.get().strip()
        rival = self.variable_rival.get().strip()
        data_partit = self.variable_data.get().strip()

        jugadors = self.obtenir_jugadors()
        dorsals = self.obtenir_dorsals()
        posicions = self.obtenir_posicions()

        if not equip:
            return (
                False,
                "Has d'introduir el nom de l'equip.",
            )

        if not rival:
            return (
                False,
                "Has d'introduir el nom del rival.",
            )

        if not self.validar_data(
            data_partit
        ):
            return (
                False,
                (
                    "La data no és correcta. "
                    "Utilitza el format DD/MM/AAAA."
                ),
            )

        for index, jugador in enumerate(
            jugadors,
            start=1,
        ):
            if not jugador:
                return (
                    False,
                    f"Falta el nom del jugador {index}.",
                )

        noms_normalitzats = [
            nom.lower()
            for nom in jugadors
        ]

        if len(
            set(noms_normalitzats)
        ) != len(noms_normalitzats):
            return (
                False,
                "No es poden repetir noms de jugadors.",
            )

        for index, dorsal in enumerate(
            dorsals,
            start=1,
        ):
            if not dorsal:
                return (
                    False,
                    f"Falta el dorsal del jugador {index}.",
                )

            if not dorsal.isdigit():
                return (
                    False,
                    (
                        f"El dorsal del jugador {index} "
                        "ha de ser numèric."
                    ),
                )

            dorsal_enter = int(dorsal)

            if dorsal_enter < 1 or dorsal_enter > 99:
                return (
                    False,
                    (
                        f"El dorsal del jugador {index} "
                        "ha d'estar entre 1 i 99."
                    ),
                )

        if len(set(dorsals)) != len(dorsals):
            return (
                False,
                "No es poden repetir dorsals.",
            )

        for index, posicio in enumerate(
            posicions,
            start=1,
        ):
            if not posicio:
                return (
                    False,
                    f"Falta la posició del jugador {index}.",
                )

        return (
            True,
            "",
        )

    def validar_data(
        self,
        data_text: str,
    ) -> bool:
        """
        Comprova que una data tingui format DD/MM/AAAA.
        """

        try:
            dia_text, mes_text, any_text = (
                data_text.split("/")
            )

            dia = int(dia_text)
            mes = int(mes_text)
            any_partit = int(any_text)

            date(
                any_partit,
                mes,
                dia,
            )

            return True

        except (
            ValueError,
            TypeError,
        ):
            return False

    # =====================================================
    # GUARDAT I NAVEGACIÓ
    # =====================================================

    def guardar_configuracio(self) -> None:
        """
        Guarda les dades introduïdes al model central.
        """

        self.dades_partit.configurar_partit(
            equip=self.variable_equip.get(),
            rival=self.variable_rival.get(),
            competicio=self.variable_competicio.get(),
            data_partit=self.variable_data.get(),
            sistema=self.variable_sistema.get(),
            local_visitant=self.variable_local_visitant.get(),
            jugadors=self.obtenir_jugadors(),
            dorsals=self.obtenir_dorsals(),
            posicions=self.obtenir_posicions(),
        )

    def validar_i_començar(self) -> None:
        """
        Valida, guarda i obre la pantalla del partit.
        """

        valid, missatge = self.validar_formulari()

        if not valid:
            messagebox.showwarning(
                "Configuració incompleta",
                missatge,
            )
            return

        self.guardar_configuracio()

        configuracio_valida, missatge_model = (
            self.dades_partit.configuracio_valida()
        )

        if not configuracio_valida:
            messagebox.showwarning(
                "Configuració incorrecta",
                missatge_model,
            )
            return

        self.començar_partit()

    def confirmar_tornada_inici(self) -> None:
        """
        Demana confirmació abans de tornar a la portada.
        """

        te_dades = any(
            [
                self.variable_equip.get().strip(),
                self.variable_rival.get().strip(),
                any(
                    self.obtenir_jugadors()
                ),
            ]
        )

        if te_dades:
            confirmacio = messagebox.askyesno(
                "Tornar a l'inici",
                (
                    "Vols tornar a l'inici?\n\n"
                    "Les dades que no hagis guardat "
                    "es podrien perdre."
                ),
            )

            if not confirmacio:
                return

        self.tornar_inici()