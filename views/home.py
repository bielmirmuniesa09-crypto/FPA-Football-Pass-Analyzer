import customtkinter as ctk


# =========================================================
# PANTALLA D'INICI
# =========================================================

class HomeView(ctk.CTkFrame):
    """
    Pantalla principal de Football Pass Analyzer.

    Inclou:
    - títol de l'aplicació;
    - subtítol;
    - botó per crear un partit;
    - botó per carregar un partit;
    - botó per sortir.
    """

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_VERD = "#22C55E"
    COLOR_VERD_FOSC = "#15803D"
    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"

    def __init__(
        self,
        master,
        nou_partit,
        carregar_partit,
        sortir_aplicacio,
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.nou_partit = nou_partit
        self.carregar_partit = carregar_partit
        self.sortir_aplicacio = sortir_aplicacio

        self.crear_interficie()

    # =====================================================
    # INTERFÍCIE
    # =====================================================

    def crear_interficie(self) -> None:
        """
        Construeix tots els elements visuals de la portada.
        """

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        contenidor = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        contenidor.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=50,
            pady=40,
        )

        contenidor.grid_columnconfigure(0, weight=1)
        contenidor.grid_columnconfigure(1, weight=1)
        contenidor.grid_rowconfigure(0, weight=1)

        self.crear_zona_esquerra(contenidor)
        self.crear_zona_dreta(contenidor)

    # =====================================================
    # ZONA ESQUERRA
    # =====================================================

    def crear_zona_esquerra(self, contenidor) -> None:
        zona_esquerra = ctk.CTkFrame(
            contenidor,
            fg_color="transparent",
        )
        zona_esquerra.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(20, 40),
            pady=20,
        )

        zona_esquerra.grid_columnconfigure(0, weight=1)
        zona_esquerra.grid_rowconfigure(0, weight=1)
        zona_esquerra.grid_rowconfigure(1, weight=0)
        zona_esquerra.grid_rowconfigure(2, weight=0)
        zona_esquerra.grid_rowconfigure(3, weight=0)
        zona_esquerra.grid_rowconfigure(4, weight=1)

        etiqueta_superior = ctk.CTkLabel(
            zona_esquerra,
            text="ANÀLISI DE XARXES DE PASSADES",
            font=ctk.CTkFont(
                family="Arial",
                size=15,
                weight="bold",
            ),
            text_color=self.COLOR_VERD,
        )
        etiqueta_superior.grid(
            row=0,
            column=0,
            sticky="sw",
            pady=(0, 20),
        )

        titol = ctk.CTkLabel(
            zona_esquerra,
            text="FPA",
            justify="left",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=88,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        titol.grid(
            row=1,
            column=0,
            sticky="w",
        )

        subtitol_nom = ctk.CTkLabel(
            zona_esquerra,
            text="Football Pass Analyzer",
            justify="left",
            anchor="w",
            font=ctk.CTkFont(
                family="Arial",
                size=24,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol_nom.grid(
            row=2,
            column=0,
            sticky="w",
            pady=(4, 10),
        )

        subtitol = ctk.CTkLabel(
            zona_esquerra,
            text=(
                "Registra les passades d'un equip, analitza la seva xarxa "
                "de joc i identifica els jugadors més influents."
            ),
            justify="left",
            anchor="w",
            wraplength=570,
            font=ctk.CTkFont(
                family="Arial",
                size=18,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol.grid(
            row=3,
            column=0,
            sticky="w",
            pady=(25, 35),
        )

        contenidor_botons = ctk.CTkFrame(
            zona_esquerra,
            fg_color="transparent",
        )
        contenidor_botons.grid(
            row=4,
            column=0,
            sticky="w",
        )

        boto_nou = ctk.CTkButton(
            contenidor_botons,
            text="NOU PARTIT",
            command=self.nou_partit,
            width=210,
            height=54,
            corner_radius=14,
            fg_color=self.COLOR_VERD,
            hover_color=self.COLOR_VERD_FOSC,
            text_color="#04130E",
            font=ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
            ),
        )
        boto_nou.grid(
            row=0,
            column=0,
            padx=(0, 15),
        )

        boto_carregar = ctk.CTkButton(
            contenidor_botons,
            text="CARREGAR PARTIT",
            command=self.carregar_partit,
            width=210,
            height=54,
            corner_radius=14,
            fg_color="transparent",
            hover_color=self.COLOR_PANELL,
            border_width=2,
            border_color=self.COLOR_VERD,
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                family="Arial",
                size=16,
                weight="bold",
            ),
        )
        boto_carregar.grid(
            row=0,
            column=1,
        )

        boto_sortir = ctk.CTkButton(
            zona_esquerra,
            text="Sortir de l'aplicació",
            command=self.sortir_aplicacio,
            width=180,
            height=38,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#17372E",
            text_color=self.COLOR_TEXT_SECUNDARI,
            font=ctk.CTkFont(
                family="Arial",
                size=13,
            ),
        )
        boto_sortir.grid(
            row=5,
            column=0,
            sticky="sw",
            pady=(40, 0),
        )

    # =====================================================
    # ZONA DRETA
    # =====================================================

    def crear_zona_dreta(self, contenidor) -> None:
        panell = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=28,
        )
        panell.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(20, 20),
            pady=20,
        )

        panell.grid_columnconfigure(0, weight=1)
        panell.grid_rowconfigure(0, weight=1)

        camp = ctk.CTkCanvas(
            panell,
            background="#167447",
            highlightthickness=0,
        )
        camp.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=28,
            pady=28,
        )

        camp.bind(
            "<Configure>",
            lambda event: self.dibuixar_camp(
                camp,
                event.width,
                event.height,
            ),
        )

    # =====================================================
    # DIBUIX DEL CAMP
    # =====================================================

    def dibuixar_camp(
        self,
        canvas,
        amplada: int,
        alcada: int,
    ) -> None:
        """
        Dibuixa un camp de futbol decoratiu.
        """

        canvas.delete("all")

        marge = 30

        x1 = marge
        y1 = marge
        x2 = amplada - marge
        y2 = alcada - marge

        if x2 <= x1 or y2 <= y1:
            return

        color_linies = "#EAF7EF"
        gruix = 3

        canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=color_linies,
            width=gruix,
        )

        centre_x = (x1 + x2) / 2
        centre_y = (y1 + y2) / 2

        canvas.create_line(
            x1,
            centre_y,
            x2,
            centre_y,
            fill=color_linies,
            width=gruix,
        )

        radi = min(
            (x2 - x1) * 0.16,
            (y2 - y1) * 0.11,
        )

        canvas.create_oval(
            centre_x - radi,
            centre_y - radi,
            centre_x + radi,
            centre_y + radi,
            outline=color_linies,
            width=gruix,
        )

        canvas.create_oval(
            centre_x - 4,
            centre_y - 4,
            centre_x + 4,
            centre_y + 4,
            fill=color_linies,
            outline=color_linies,
        )

        area_amplada = (x2 - x1) * 0.48
        area_alcada = (y2 - y1) * 0.18

        canvas.create_rectangle(
            centre_x - area_amplada / 2,
            y1,
            centre_x + area_amplada / 2,
            y1 + area_alcada,
            outline=color_linies,
            width=gruix,
        )

        canvas.create_rectangle(
            centre_x - area_amplada / 2,
            y2 - area_alcada,
            centre_x + area_amplada / 2,
            y2,
            outline=color_linies,
            width=gruix,
        )

        area_petita_amplada = (x2 - x1) * 0.23
        area_petita_alcada = (y2 - y1) * 0.07

        canvas.create_rectangle(
            centre_x - area_petita_amplada / 2,
            y1,
            centre_x + area_petita_amplada / 2,
            y1 + area_petita_alcada,
            outline=color_linies,
            width=gruix,
        )

        canvas.create_rectangle(
            centre_x - area_petita_amplada / 2,
            y2 - area_petita_alcada,
            centre_x + area_petita_amplada / 2,
            y2,
            outline=color_linies,
            width=gruix,
        )

        self.dibuixar_nodes_decoratius(
            canvas,
            x1,
            y1,
            x2,
            y2,
        )

    def dibuixar_nodes_decoratius(
        self,
        canvas,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> None:
        """
        Dibuixa onze nodes decoratius simulant una formació 4-3-3.
        """

        amplada = x2 - x1
        alcada = y2 - y1

        posicions = [
            (0.50, 0.90),
            (0.18, 0.72),
            (0.39, 0.76),
            (0.61, 0.76),
            (0.82, 0.72),
            (0.28, 0.52),
            (0.50, 0.57),
            (0.72, 0.52),
            (0.20, 0.28),
            (0.50, 0.18),
            (0.80, 0.28),
        ]

        radi = max(
            12,
            min(amplada, alcada) * 0.025,
        )

        for numero, (px, py) in enumerate(
            posicions,
            start=1,
        ):
            x = x1 + amplada * px
            y = y1 + alcada * py

            canvas.create_oval(
                x - radi,
                y - radi,
                x + radi,
                y + radi,
                fill="#071E17",
                outline="#22C55E",
                width=3,
            )

            canvas.create_text(
                x,
                y,
                text=str(numero),
                fill="#F8FAFC",
                font=("Arial", 11, "bold"),
            )