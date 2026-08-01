import customtkinter as ctk


class LoadingView(ctk.CTkFrame):
    """Pantalla breu de transició entre les vistes de l'aplicació."""

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_VERD = "#22C55E"
    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"

    def __init__(
        self,
        master,
        missatge: str = "Carregant...",
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self._pas_animacio = 0
        self._animacio_activa = True
        self._missatge_base = missatge.rstrip(".")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        panell = ctk.CTkFrame(
            self,
            width=440,
            height=240,
            fg_color=self.COLOR_PANELL,
            corner_radius=26,
        )
        panell.grid(
            row=0,
            column=0,
        )
        panell.grid_propagate(False)

        panell.grid_columnconfigure(0, weight=1)
        panell.grid_rowconfigure(
            (0, 1, 2),
            weight=1,
        )

        icona = ctk.CTkLabel(
            panell,
            text="⚽",
            font=ctk.CTkFont(size=54),
            text_color=self.COLOR_VERD,
        )
        icona.grid(
            row=0,
            column=0,
            pady=(24, 2),
        )

        self.etiqueta = ctk.CTkLabel(
            panell,
            text=f"{self._missatge_base}...",
            font=ctk.CTkFont(
                family="Arial",
                size=24,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        )
        self.etiqueta.grid(
            row=1,
            column=0,
            pady=(0, 4),
        )

        subtitol = ctk.CTkLabel(
            panell,
            text="Preparant les dades i la visualització",
            font=ctk.CTkFont(
                family="Arial",
                size=14,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        subtitol.grid(
            row=2,
            column=0,
            pady=(0, 28),
        )

        self.after(
            120,
            self._animar,
        )

    def _animar(self) -> None:
        """
        Anima els punts del missatge de càrrega.
        """

        if (
            not self._animacio_activa
            or not self.winfo_exists()
        ):
            return

        punts = "." * (
            (self._pas_animacio % 3) + 1
        )

        self.etiqueta.configure(
            text=f"{self._missatge_base}{punts}"
        )

        self._pas_animacio += 1

        self.after(
            320,
            self._animar,
        )

    def destroy(self) -> None:
        """
        Atura l'animació abans de destruir la pantalla.
        """

        self._animacio_activa = False
        super().destroy()
        