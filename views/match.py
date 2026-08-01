from __future__ import annotations

from tkinter import messagebox

import customtkinter as ctk

from models.match_data import MatchData


# =========================================================
# PANTALLA DE REGISTRE DEL PARTIT
# =========================================================

class MatchView(ctk.CTkFrame):
    """
    Pantalla principal per registrar les passades del partit.

    Funcionament:
    1. Seleccionar el jugador que realitza la passada.
    2. Seleccionar el jugador destinatari.
    3. Registrar-la com a passada bona o dolenta.

    També permet:
    - registrar una passada dolenta sense destinatari;
    - desfer l'última passada;
    - consultar l'historial;
    - veure estadístiques en directe;
    - finalitzar el partit.
    """

    # =====================================================
    # COLORS
    # =====================================================

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_PANELL_CLAR = "#12372D"

    COLOR_VERD = "#22C55E"
    COLOR_VERD_FOSC = "#15803D"

    COLOR_VERMELL = "#EF4444"
    COLOR_VERMELL_FOSC = "#B91C1C"

    COLOR_GROC = "#FACC15"
    COLOR_BLAU = "#38BDF8"

    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"

    COLOR_CAMP = "#167447"
    COLOR_CAMP_FOSC = "#12633D"
    COLOR_LINIES = "#EAF7EF"

    COLOR_NODE = "#071E17"
    COLOR_NODE_SELECCIONAT = "#FACC15"
    COLOR_NODE_DESTI = "#38BDF8"

    # =====================================================
    # CONSTRUCTOR
    # =====================================================

    def __init__(
        self,
        master,
        dades_partit: MatchData,
        tornar_configuracio,
        finalitzar_partit,
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.dades_partit = dades_partit
        self.tornar_configuracio = tornar_configuracio
        self.finalitzar_partit = finalitzar_partit

        # Índex del jugador que fa la passada.
        self.jugador_origen: int | None = None

        # Índex del jugador que rep o havia de rebre la passada.
        self.jugador_desti: int | None = None

        # Coordenades dels jugadors dibuixats al camp.
        self.coordenades_jugadors: dict[int, tuple[float, float]] = {}

        # Radi dels nodes dels jugadors.
        self.radi_jugador = 25

        # Referències visuals.
        self.canvas_camp = None
        self.contenidor_historial = None

        # Etiquetes d'estadístiques.
        self.etiqueta_total = None
        self.etiqueta_bones = None
        self.etiqueta_dolentes = None
        self.etiqueta_precisio = None

        self.etiqueta_seleccio_origen = None
        self.etiqueta_seleccio_desti = None
        self.etiqueta_instruccio = None

        self.crear_interficie()

    # =====================================================
    # CREACIÓ GENERAL
    # =====================================================

    def crear_interficie(self) -> None:
        """
        Construeix tota la pantalla de registre.
        """

        self.grid_columnconfigure(
            0,
            weight=1,
        )

        self.grid_rowconfigure(
            1,
            weight=1,
        )

        self.crear_capçalera()

        cos = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        cos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=24,
            pady=(8, 24),
        )

        cos.grid_columnconfigure(
            0,
            weight=3,
        )

        cos.grid_columnconfigure(
            1,
            weight=1,
        )

        cos.grid_rowconfigure(
            0,
            weight=1,
        )

        self.crear_zona_camp(
            cos
        )

        self.crear_panell_lateral(
            cos
        )

        self.actualitzar_estadistiques()
        self.actualitzar_historial()
        self.actualitzar_panell_seleccio()

    # =====================================================
    # CAPÇALERA
    # =====================================================

    def crear_capçalera(self) -> None:
        """
        Crea la franja superior amb el partit i els controls.
        """

        capçalera = ctk.CTkFrame(
            self,
            fg_color=self.COLOR_PANELL,
            corner_radius=0,
            height=84,
        )
        capçalera.grid(
            row=0,
            column=0,
            sticky="ew",
        )

        capçalera.grid_columnconfigure(
            0,
            weight=1,
        )

        capçalera.grid_columnconfigure(
            1,
            weight=0,
        )

        bloc_partit = ctk.CTkFrame(
            capçalera,
            fg_color="transparent",
        )
        bloc_partit.grid(
            row=0,
            column=0,
            sticky="w",
            padx=28,
            pady=16,
        )

        text_partit = (
            f"{self.dades_partit.equip}  —  "
            f"{self.dades_partit.rival}"
        )

        titol = ctk.CTkLabel(
            bloc_partit,
            text=text_partit,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=24,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        titol.pack(
            anchor="w",
        )

        detalls = (
            f"{self.dades_partit.competicio}"
            f"   ·   {self.dades_partit.data_partit}"
            f"   ·   {self.dades_partit.sistema}"
            f"   ·   {self.dades_partit.local_visitant}"
        )

        subtitol = ctk.CTkLabel(
            bloc_partit,
            text=detalls,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol.pack(
            anchor="w",
            pady=(5, 0),
        )

        bloc_botons = ctk.CTkFrame(
            capçalera,
            fg_color="transparent",
        )
        bloc_botons.grid(
            row=0,
            column=1,
            sticky="e",
            padx=28,
            pady=16,
        )

        boto_configuracio = ctk.CTkButton(
            bloc_botons,
            text="← CONFIGURACIÓ",
            command=self.confirmar_tornada_configuracio,
            width=160,
            height=42,
            corner_radius=11,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#365F54",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_configuracio.grid(
            row=0,
            column=0,
            padx=(0, 10),
        )

        boto_finalitzar = ctk.CTkButton(
            bloc_botons,
            text="FINALITZAR PARTIT",
            command=self.confirmar_finalitzacio,
            width=180,
            height=42,
            corner_radius=11,
            fg_color=self.COLOR_VERD,
            hover_color=self.COLOR_VERD_FOSC,
            text_color="#04130E",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        boto_finalitzar.grid(
            row=0,
            column=1,
        )

    # =====================================================
    # ZONA DEL CAMP
    # =====================================================

    def crear_zona_camp(self, pare) -> None:
        """
        Crea el camp de futbol i els controls de registre.
        """

        zona = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=22,
        )
        zona.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12),
        )

        zona.grid_columnconfigure(
            0,
            weight=1,
        )

        zona.grid_rowconfigure(
            1,
            weight=1,
        )

        self.crear_panell_instruccions(
            zona
        )

        self.crear_canvas_camp(
            zona
        )

        self.crear_controls_passades(
            zona
        )

    # =====================================================
    # INSTRUCCIONS I SELECCIÓ
    # =====================================================

    def crear_panell_instruccions(self, pare) -> None:
        """
        Mostra què ha de fer l'usuari i quins jugadors ha seleccionat.
        """

        panell = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        panell.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=22,
            pady=(20, 12),
        )

        panell.grid_columnconfigure(
            0,
            weight=1,
        )

        panell.grid_columnconfigure(
            1,
            weight=0,
        )

        bloc_instruccio = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        bloc_instruccio.grid(
            row=0,
            column=0,
            sticky="w",
        )

        etiqueta_titol = ctk.CTkLabel(
            bloc_instruccio,
            text="REGISTRE EN DIRECTE",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        etiqueta_titol.pack(
            anchor="w",
        )

        self.etiqueta_instruccio = ctk.CTkLabel(
            bloc_instruccio,
            text="Selecciona el jugador que realitza la passada.",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
            text_color=self.COLOR_TEXT,
        )
        self.etiqueta_instruccio.pack(
            anchor="w",
            pady=(5, 0),
        )

        bloc_seleccio = ctk.CTkFrame(
            panell,
            fg_color=self.COLOR_PANELL_CLAR,
            corner_radius=13,
        )
        bloc_seleccio.grid(
            row=0,
            column=1,
            sticky="e",
        )

        bloc_origen = ctk.CTkFrame(
            bloc_seleccio,
            fg_color="transparent",
        )
        bloc_origen.grid(
            row=0,
            column=0,
            padx=16,
            pady=10,
        )

        etiqueta_origen_titol = ctk.CTkLabel(
            bloc_origen,
            text="ORIGEN",
            font=ctk.CTkFont(
                family="Arial",
                size=10,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta_origen_titol.pack()

        self.etiqueta_seleccio_origen = ctk.CTkLabel(
            bloc_origen,
            text="—",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_GROC,
        )
        self.etiqueta_seleccio_origen.pack(
            pady=(3, 0),
        )

        separador = ctk.CTkFrame(
            bloc_seleccio,
            width=2,
            height=38,
            fg_color="#365F54",
        )
        separador.grid(
            row=0,
            column=1,
            pady=10,
        )

        bloc_desti = ctk.CTkFrame(
            bloc_seleccio,
            fg_color="transparent",
        )
        bloc_desti.grid(
            row=0,
            column=2,
            padx=16,
            pady=10,
        )

        etiqueta_desti_titol = ctk.CTkLabel(
            bloc_desti,
            text="DESTÍ",
            font=ctk.CTkFont(
                family="Arial",
                size=10,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta_desti_titol.pack()

        self.etiqueta_seleccio_desti = ctk.CTkLabel(
            bloc_desti,
            text="—",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
                weight="bold",
            ),
            text_color=self.COLOR_BLAU,
        )
        self.etiqueta_seleccio_desti.pack(
            pady=(3, 0),
        )

    # =====================================================
    # CANVAS DEL CAMP
    # =====================================================

    def crear_canvas_camp(self, pare) -> None:
        """
        Crea el canvas interactiu del camp de futbol.
        """

        contenidor = ctk.CTkFrame(
            pare,
            fg_color="#09251C",
            corner_radius=18,
        )
        contenidor.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=(0, 14),
        )

        contenidor.grid_columnconfigure(
            0,
            weight=1,
        )

        contenidor.grid_rowconfigure(
            0,
            weight=1,
        )

        self.canvas_camp = ctk.CTkCanvas(
            contenidor,
            background=self.COLOR_CAMP,
            highlightthickness=0,
            cursor="hand2",
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

        self.canvas_camp.bind(
            "<Button-1>",
            self.gestionar_clic_camp,
        )

    # =====================================================
    # CONTROLS DE PASSADES
    # =====================================================

    def crear_controls_passades(self, pare) -> None:
        """
        Crea els botons per registrar i corregir passades.
        """

        controls = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        controls.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=22,
            pady=(0, 20),
        )

        controls.grid_columnconfigure(
            0,
            weight=1,
        )

        boto_cancelar = ctk.CTkButton(
            controls,
            text="CANCEL·LAR SELECCIÓ",
            command=self.cancelar_seleccio,
            width=180,
            height=46,
            corner_radius=12,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL_CLAR,
            border_width=1,
            border_color="#365F54",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_cancelar.grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
        )

        boto_desfer = ctk.CTkButton(
            controls,
            text="↶ DESFER ÚLTIMA",
            command=self.desfer_ultima_passada,
            width=165,
            height=46,
            corner_radius=12,
            fg_color=self.COLOR_PANELL_CLAR,
            hover_color="#1B4A3D",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_desfer.grid(
            row=0,
            column=1,
            padx=10,
        )

        boto_sense_desti = ctk.CTkButton(
            controls,
            text="DOLENTA SENSE DESTÍ",
            command=self.registrar_dolenta_sense_desti,
            width=190,
            height=46,
            corner_radius=12,
            fg_color="#7F1D1D",
            hover_color=self.COLOR_VERMELL_FOSC,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_sense_desti.grid(
            row=0,
            column=2,
            padx=10,
        )

        boto_dolenta = ctk.CTkButton(
            controls,
            text="PASSADA DOLENTA",
            command=self.registrar_passada_dolenta,
            width=180,
            height=46,
            corner_radius=12,
            fg_color=self.COLOR_VERMELL,
            hover_color=self.COLOR_VERMELL_FOSC,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
        )
        boto_dolenta.grid(
            row=0,
            column=3,
            padx=10,
        )

        boto_bona = ctk.CTkButton(
            controls,
            text="PASSADA BONA",
            command=self.registrar_passada_bona,
            width=170,
            height=46,
            corner_radius=12,
            fg_color=self.COLOR_VERD,
            hover_color=self.COLOR_VERD_FOSC,
            text_color="#04130E",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
        )
        boto_bona.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(10, 0),
        )

    # =====================================================
    # PANELL LATERAL
    # =====================================================

    def crear_panell_lateral(self, pare) -> None:
        """
        Crea les estadístiques i l'historial del partit.
        """

        lateral = ctk.CTkFrame(
            pare,
            fg_color="transparent",
        )
        lateral.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0),
        )

        lateral.grid_columnconfigure(
            0,
            weight=1,
        )

        lateral.grid_rowconfigure(
            1,
            weight=1,
        )

        self.crear_targetes_estadistiques(
            lateral
        )

        self.crear_historial(
            lateral
        )

    # =====================================================
    # ESTADÍSTIQUES
    # =====================================================

    def crear_targetes_estadistiques(self, pare) -> None:
        """
        Crea les targetes amb les estadístiques globals.
        """

        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        panell.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12),
        )

        titol = ctk.CTkLabel(
            panell,
            text="ESTADÍSTIQUES EN DIRECTE",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        titol.pack(
            fill="x",
            padx=20,
            pady=(20, 14),
        )

        graella = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        graella.pack(
            fill="x",
            padx=16,
            pady=(0, 18),
        )

        graella.grid_columnconfigure(
            0,
            weight=1,
        )

        graella.grid_columnconfigure(
            1,
            weight=1,
        )

        self.etiqueta_total = self.crear_targeta_estadistica(
            graella,
            fila=0,
            columna=0,
            titol="TOTAL",
            valor="0",
            color=self.COLOR_TEXT,
        )

        self.etiqueta_bones = self.crear_targeta_estadistica(
            graella,
            fila=0,
            columna=1,
            titol="BONES",
            valor="0",
            color=self.COLOR_VERD,
        )

        self.etiqueta_dolentes = self.crear_targeta_estadistica(
            graella,
            fila=1,
            columna=0,
            titol="DOLENTES",
            valor="0",
            color=self.COLOR_VERMELL,
        )

        self.etiqueta_precisio = self.crear_targeta_estadistica(
            graella,
            fila=1,
            columna=1,
            titol="PRECISIÓ",
            valor="0,0 %",
            color=self.COLOR_GROC,
        )

    def crear_targeta_estadistica(
        self,
        pare,
        fila: int,
        columna: int,
        titol: str,
        valor: str,
        color: str,
    ):
        """
        Crea una targeta estadística individual.
        """

        targeta = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL_CLAR,
            corner_radius=14,
        )
        targeta.grid(
            row=fila,
            column=columna,
            sticky="ew",
            padx=5,
            pady=5,
        )

        etiqueta_titol = ctk.CTkLabel(
            targeta,
            text=titol,
            font=ctk.CTkFont(
                family="Arial",
                size=10,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        etiqueta_titol.pack(
            pady=(12, 2),
        )

        etiqueta_valor = ctk.CTkLabel(
            targeta,
            text=valor,
            font=ctk.CTkFont(
                family="Arial",
                size=22,
                weight="bold",
            ),
            text_color=color,
        )
        etiqueta_valor.pack(
            pady=(0, 12),
        )

        return etiqueta_valor

    # =====================================================
    # HISTORIAL
    # =====================================================

    def crear_historial(self, pare) -> None:
        """
        Crea el panell desplaçable de passades registrades.
        """

        panell = ctk.CTkFrame(
            pare,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        panell.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        panell.grid_columnconfigure(
            0,
            weight=1,
        )

        panell.grid_rowconfigure(
            1,
            weight=1,
        )

        capçalera = ctk.CTkFrame(
            panell,
            fg_color="transparent",
        )
        capçalera.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(18, 10),
        )

        capçalera.grid_columnconfigure(
            0,
            weight=1,
        )

        titol = ctk.CTkLabel(
            capçalera,
            text="HISTORIAL DE PASSADES",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=13,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        titol.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.etiqueta_quantitat_historial = ctk.CTkLabel(
            capçalera,
            text="0 accions",
            font=ctk.CTkFont(
                family="Arial",
                size=11,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        self.etiqueta_quantitat_historial.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.contenidor_historial = ctk.CTkScrollableFrame(
            panell,
            fg_color="#09251C",
            corner_radius=14,
            scrollbar_button_color=self.COLOR_VERD_FOSC,
            scrollbar_button_hover_color=self.COLOR_VERD,
        )
        self.contenidor_historial.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=14,
            pady=(0, 14),
        )

        self.contenidor_historial.grid_columnconfigure(
            0,
            weight=1,
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

        if amplada < 100 or alcada < 100:
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
        Dibuixa el camp i els jugadors.
        """

        canvas = self.canvas_camp
        canvas.delete("all")

        marge = 25

        x1 = marge
        y1 = marge
        x2 = amplada - marge
        y2 = alcada - marge

        if x2 <= x1 or y2 <= y1:
            return

        # Franges decoratives.
        amplada_franja = (x2 - x1) / 8

        for index in range(8):
            color = (
                self.COLOR_CAMP
                if index % 2 == 0
                else self.COLOR_CAMP_FOSC
            )

            canvas.create_rectangle(
                x1 + index * amplada_franja,
                y1,
                x1 + (index + 1) * amplada_franja,
                y2,
                fill=color,
                outline=color,
            )

        # Límits del camp.
        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=self.COLOR_LINIES,
            width=3,
        )

        centre_x = (x1 + x2) / 2
        centre_y = (y1 + y2) / 2

        # Línia de mig camp.
        canvas.create_line(
            x1,
            centre_y,
            x2,
            centre_y,
            fill=self.COLOR_LINIES,
            width=3,
        )

        # Cercle central.
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
            width=3,
        )

        canvas.create_oval(
            centre_x - 4,
            centre_y - 4,
            centre_x + 4,
            centre_y + 4,
            fill=self.COLOR_LINIES,
            outline=self.COLOR_LINIES,
        )

        # Àrees grans.
        amplada_area = (x2 - x1) * 0.48
        alcada_area = (y2 - y1) * 0.18

        canvas.create_rectangle(
            centre_x - amplada_area / 2,
            y1,
            centre_x + amplada_area / 2,
            y1 + alcada_area,
            outline=self.COLOR_LINIES,
            width=3,
        )

        canvas.create_rectangle(
            centre_x - amplada_area / 2,
            y2 - alcada_area,
            centre_x + amplada_area / 2,
            y2,
            outline=self.COLOR_LINIES,
            width=3,
        )

        # Àrees petites.
        amplada_area_petita = (x2 - x1) * 0.23
        alcada_area_petita = (y2 - y1) * 0.07

        canvas.create_rectangle(
            centre_x - amplada_area_petita / 2,
            y1,
            centre_x + amplada_area_petita / 2,
            y1 + alcada_area_petita,
            outline=self.COLOR_LINIES,
            width=3,
        )

        canvas.create_rectangle(
            centre_x - amplada_area_petita / 2,
            y2 - alcada_area_petita,
            centre_x + amplada_area_petita / 2,
            y2,
            outline=self.COLOR_LINIES,
            width=3,
        )

        # Punts de penal.
        canvas.create_oval(
            centre_x - 3,
            y1 + alcada_area * 0.68 - 3,
            centre_x + 3,
            y1 + alcada_area * 0.68 + 3,
            fill=self.COLOR_LINIES,
            outline=self.COLOR_LINIES,
        )

        canvas.create_oval(
            centre_x - 3,
            y2 - alcada_area * 0.68 - 3,
            centre_x + 3,
            y2 - alcada_area * 0.68 + 3,
            fill=self.COLOR_LINIES,
            outline=self.COLOR_LINIES,
        )

        self.dibuixar_jugadors(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
        )

    def dibuixar_jugadors(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> None:
        """
        Dibuixa els onze jugadors segons la formació.
        """

        canvas = self.canvas_camp
        sistema = self.dades_partit.sistema

        coordenades = self.obtenir_coordenades_formacio(
            sistema
        )

        amplada = x2 - x1
        alcada = y2 - y1

        self.coordenades_jugadors.clear()

        self.radi_jugador = max(
            21,
            min(amplada, alcada) * 0.042,
        )

        for index, (px, py) in enumerate(coordenades):
            x = x1 + amplada * px
            y = y1 + alcada * py

            self.coordenades_jugadors[index] = (
                x,
                y,
            )

            color_farciment = self.COLOR_NODE
            color_contorn = self.COLOR_VERD
            gruix_contorn = 3

            if index == self.jugador_origen:
                color_farciment = "#4A3F05"
                color_contorn = self.COLOR_NODE_SELECCIONAT
                gruix_contorn = 5

            elif index == self.jugador_desti:
                color_farciment = "#083B4A"
                color_contorn = self.COLOR_NODE_DESTI
                gruix_contorn = 5

            canvas.create_oval(
                x - self.radi_jugador,
                y - self.radi_jugador,
                x + self.radi_jugador,
                y + self.radi_jugador,
                fill=color_farciment,
                outline=color_contorn,
                width=gruix_contorn,
                tags=(
                    f"jugador_{index}",
                    "jugador",
                ),
            )

            dorsal = (
                self.dades_partit.dorsals[index]
                if index < len(self.dades_partit.dorsals)
                else str(index + 1)
            )

            canvas.create_text(
                x,
                y - 3,
                text=dorsal,
                fill=self.COLOR_TEXT,
                font=(
                    "Arial",
                    max(
                        11,
                        int(self.radi_jugador * 0.52),
                    ),
                    "bold",
                ),
                tags=(
                    f"jugador_{index}",
                    "jugador",
                ),
            )

            nom = (
                self.dades_partit.jugadors[index]
                if index < len(self.dades_partit.jugadors)
                else f"Jugador {index + 1}"
            )

            nom_curt = (
                nom
                if len(nom) <= 14
                else nom[:13] + "…"
            )

            canvas.create_text(
                x,
                y + self.radi_jugador + 13,
                text=nom_curt,
                fill=self.COLOR_TEXT,
                font=(
                    "Arial",
                    10,
                    "bold",
                ),
                tags=(
                    f"jugador_{index}",
                    "jugador",
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
        Retorna les coordenades relatives de cada formació.
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

    # =====================================================
    # INTERACCIÓ AMB EL CAMP
    # =====================================================

    def gestionar_clic_camp(self, event) -> None:
        """
        Detecta quin jugador ha estat seleccionat.
        """

        jugador_clicat = self.detectar_jugador(
            event.x,
            event.y,
        )

        if jugador_clicat is None:
            return

        if self.jugador_origen is None:
            self.jugador_origen = jugador_clicat
            self.jugador_desti = None

        elif self.jugador_desti is None:
            if jugador_clicat == self.jugador_origen:
                self.cancelar_seleccio()
                return

            self.jugador_desti = jugador_clicat

        else:
            self.jugador_origen = jugador_clicat
            self.jugador_desti = None

        self.actualitzar_panell_seleccio()
        self.redibuixar_camp()

    def detectar_jugador(
        self,
        x_clic: float,
        y_clic: float,
    ) -> int | None:
        """
        Retorna l'índex del jugador situat sota el clic.
        """

        for index, (x, y) in self.coordenades_jugadors.items():
            distancia_quadrada = (
                (x_clic - x) ** 2
                + (y_clic - y) ** 2
            )

            if distancia_quadrada <= (
                self.radi_jugador + 10
            ) ** 2:
                return index

        return None

    # =====================================================
    # PANELL DE SELECCIÓ
    # =====================================================

    def actualitzar_panell_seleccio(self) -> None:
        """
        Actualitza els textos d'origen, destí i instrucció.
        """

        if self.jugador_origen is None:
            self.etiqueta_seleccio_origen.configure(
                text="—"
            )
            self.etiqueta_seleccio_desti.configure(
                text="—"
            )
            self.etiqueta_instruccio.configure(
                text="Selecciona el jugador que realitza la passada."
            )
            return

        nom_origen = self.obtenir_nom_jugador(
            self.jugador_origen
        )

        self.etiqueta_seleccio_origen.configure(
            text=nom_origen
        )

        if self.jugador_desti is None:
            self.etiqueta_seleccio_desti.configure(
                text="—"
            )
            self.etiqueta_instruccio.configure(
                text=(
                    "Ara selecciona el destinatari, "
                    "o registra una passada dolenta sense destí."
                )
            )
            return

        nom_desti = self.obtenir_nom_jugador(
            self.jugador_desti
        )

        self.etiqueta_seleccio_desti.configure(
            text=nom_desti
        )

        self.etiqueta_instruccio.configure(
            text=(
                "Selecciona si la passada ha estat "
                "bona o dolenta."
            )
        )

    def obtenir_nom_jugador(
        self,
        index: int,
    ) -> str:
        """
        Retorna el nom del jugador amb dorsal.
        """

        nom = self.dades_partit.jugadors[index]

        dorsal = (
            self.dades_partit.dorsals[index]
            if index < len(self.dades_partit.dorsals)
            else str(index + 1)
        )

        return f"{dorsal}. {nom}"

    def cancelar_seleccio(self) -> None:
        """
        Elimina la selecció actual.
        """

        self.jugador_origen = None
        self.jugador_desti = None

        self.actualitzar_panell_seleccio()
        self.redibuixar_camp()

    # =====================================================
    # REGISTRE DE PASSADES
    # =====================================================

    def registrar_passada_bona(self) -> None:
        """
        Registra una passada completada.
        """

        if self.jugador_origen is None:
            messagebox.showwarning(
                "Falta l'origen",
                "Selecciona primer el jugador que fa la passada.",
            )
            return

        if self.jugador_desti is None:
            messagebox.showwarning(
                "Falta el destinatari",
                "Selecciona el jugador que rep la passada.",
            )
            return

        try:
            self.dades_partit.registrar_passada_bona(
                origen=self.jugador_origen,
                desti=self.jugador_desti,
            )

        except (
            ValueError,
            IndexError,
            TypeError,
        ) as error:
            messagebox.showerror(
                "No s'ha pogut registrar",
                str(error),
            )
            return

        self.finalitzar_registre_passada()

    def registrar_passada_dolenta(self) -> None:
        """
        Registra una passada dolenta amb destinatari.
        """

        if self.jugador_origen is None:
            messagebox.showwarning(
                "Falta l'origen",
                "Selecciona primer el jugador que fa la passada.",
            )
            return

        if self.jugador_desti is None:
            messagebox.showwarning(
                "Falta el destinatari",
                (
                    "Selecciona el destinatari previst o utilitza "
                    "'Dolenta sense destí'."
                ),
            )
            return

        try:
            self.dades_partit.registrar_passada_dolenta(
                origen=self.jugador_origen,
                desti=self.jugador_desti,
            )

        except (
            ValueError,
            IndexError,
            TypeError,
        ) as error:
            messagebox.showerror(
                "No s'ha pogut registrar",
                str(error),
            )
            return

        self.finalitzar_registre_passada()

    def registrar_dolenta_sense_desti(self) -> None:
        """
        Registra una passada fallada sense destinatari concret.
        """

        if self.jugador_origen is None:
            messagebox.showwarning(
                "Falta l'origen",
                "Selecciona primer el jugador que perd la passada.",
            )
            return

        try:
            self.dades_partit.registrar_passada_dolenta(
                origen=self.jugador_origen,
                desti=None,
            )

        except (
            ValueError,
            IndexError,
            TypeError,
        ) as error:
            messagebox.showerror(
                "No s'ha pogut registrar",
                str(error),
            )
            return

        self.finalitzar_registre_passada()

    def finalitzar_registre_passada(self) -> None:
        """
        Actualitza la interfície després de registrar una passada.
        """

        self.jugador_origen = None
        self.jugador_desti = None

        self.actualitzar_estadistiques()
        self.actualitzar_historial()
        self.actualitzar_panell_seleccio()
        self.redibuixar_camp()

    # =====================================================
    # ESTADÍSTIQUES EN DIRECTE
    # =====================================================

    def actualitzar_estadistiques(self) -> None:
        """
        Actualitza les quatre targetes estadístiques.
        """

        total = self.dades_partit.total_passades()
        bones = self.dades_partit.total_passades_bones()
        dolentes = self.dades_partit.total_passades_dolentes()
        precisio = self.dades_partit.percentatge_encert_global()

        self.etiqueta_total.configure(
            text=str(total)
        )

        self.etiqueta_bones.configure(
            text=str(bones)
        )

        self.etiqueta_dolentes.configure(
            text=str(dolentes)
        )

        text_precisio = (
            f"{precisio:.1f} %"
            .replace(".", ",")
        )

        self.etiqueta_precisio.configure(
            text=text_precisio
        )

    # =====================================================
    # HISTORIAL
    # =====================================================

    def actualitzar_historial(self) -> None:
        """
        Reconstrueix l'historial de passades.
        """

        for element in self.contenidor_historial.winfo_children():
            element.destroy()

        historial = self.dades_partit.historial_passades()

        quantitat = len(historial)

        text_accions = (
            "1 acció"
            if quantitat == 1
            else f"{quantitat} accions"
        )

        self.etiqueta_quantitat_historial.configure(
            text=text_accions
        )

        if not historial:
            buit = ctk.CTkLabel(
                self.contenidor_historial,
                text=(
                    "Encara no s'ha registrat cap passada.\n"
                    "Selecciona dos jugadors al camp."
                ),
                justify="center",
                font=ctk.CTkFont(
                    family="Arial",
                    size=12,
                ),
                text_color=self.COLOR_TEXT_SECUNDARI,
            )
            buit.grid(
                row=0,
                column=0,
                sticky="ew",
                padx=12,
                pady=30,
            )
            return

        historial_invers = list(
            reversed(historial)
        )

        for fila, passada in enumerate(historial_invers):
            self.crear_fila_historial(
                fila=fila,
                passada=passada,
            )

    def crear_fila_historial(
        self,
        fila: int,
        passada: dict,
    ) -> None:
        """
        Crea una fila de l'historial.
        """

        es_bona = passada["resultat"] == "bona"

        color_resultat = (
            self.COLOR_VERD
            if es_bona
            else self.COLOR_VERMELL
        )

        text_resultat = (
            "BONA"
            if es_bona
            else "DOLENTA"
        )

        targeta = ctk.CTkFrame(
            self.contenidor_historial,
            fg_color=self.COLOR_PANELL_CLAR,
            corner_radius=12,
        )
        targeta.grid(
            row=fila,
            column=0,
            sticky="ew",
            padx=4,
            pady=5,
        )

        targeta.grid_columnconfigure(
            1,
            weight=1,
        )

        numero = ctk.CTkLabel(
            targeta,
            text=f"#{passada['numero']}",
            width=42,
            font=ctk.CTkFont(
                family="Arial",
                size=11,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        numero.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(10, 5),
            pady=10,
        )

        trajecte = ctk.CTkLabel(
            targeta,
            text=(
                f"{passada['origen']}  →  "
                f"{passada['desti']}"
            ),
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=12,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        trajecte.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
            pady=(9, 1),
        )

        resultat = ctk.CTkLabel(
            targeta,
            text=text_resultat,
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=10,
                weight="bold",
            ),
            text_color=color_resultat,
        )
        resultat.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=(1, 9),
        )

        indicador = ctk.CTkFrame(
            targeta,
            width=5,
            height=42,
            corner_radius=3,
            fg_color=color_resultat,
        )
        indicador.grid(
            row=0,
            column=2,
            rowspan=2,
            padx=(5, 10),
            pady=9,
        )

    # =====================================================
    # DESFER
    # =====================================================

    def desfer_ultima_passada(self) -> None:
        """
        Elimina l'última passada.
        """

        passada_eliminada = (
            self.dades_partit.desfer_ultima_passada()
        )

        if passada_eliminada is None:
            messagebox.showinfo(
                "Sense passades",
                "No hi ha cap passada per desfer.",
            )
            return

        self.cancelar_seleccio()
        self.actualitzar_estadistiques()
        self.actualitzar_historial()

    # =====================================================
    # NAVEGACIÓ
    # =====================================================

    def confirmar_tornada_configuracio(self) -> None:
        """
        Confirma el retorn a la configuració.
        """

        if self.dades_partit.total_passades() > 0:
            confirmacio = messagebox.askyesno(
                "Tornar a la configuració",
                (
                    "Ja hi ha passades registrades.\n\n"
                    "Si tornes a la configuració i comences de nou, "
                    "l'historial es reiniciarà.\n\n"
                    "Vols continuar?"
                ),
            )

            if not confirmacio:
                return

        self.tornar_configuracio()

    def confirmar_finalitzacio(self) -> None:
        """
        Confirma que el partit s'ha acabat.
        """

        total = self.dades_partit.total_passades()

        if total == 0:
            confirmacio = messagebox.askyesno(
                "Partit sense passades",
                (
                    "No s'ha registrat cap passada.\n\n"
                    "Vols finalitzar igualment?"
                ),
            )

        else:
            confirmacio = messagebox.askyesno(
                "Finalitzar partit",
                (
                    f"S'han registrat {total} passades.\n\n"
                    "Vols finalitzar el partit i veure els resultats?"
                ),
            )

        if confirmacio:
            self.finalitzar_partit()