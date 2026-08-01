from __future__ import annotations

from tkinter import messagebox
from tkinter import simpledialog
from typing import Callable

import customtkinter as ctk

from utils.history_manager import editar_partit
from utils.history_manager import eliminar_partit
from utils.history_manager import obtenir_partits_guardats


class HistoryView(ctk.CTkFrame):
    """
    Pantalla que mostra l'historial de partits guardats.

    Permet:
    - seleccionar dos partits;
    - comparar-los;
    - editar les dades generals;
    - eliminar partits.
    """

    COLOR_FONS = "#061B15"
    COLOR_PANELL = "#0D2A22"
    COLOR_TARGETA = "#12382E"
    COLOR_TARGETA_SELECCIONADA = "#185C45"

    COLOR_VERD = "#22C55E"
    COLOR_TEXT = "#F8FAFC"
    COLOR_TEXT_SECUNDARI = "#94A3B8"
    COLOR_VERMELL = "#EF4444"
    COLOR_BLAU = "#38BDF8"
    COLOR_GROC = "#FACC15"

    COLOR_LINIA = "#1F4D3E"
    COLOR_BOTO_DESACTIVAT = "#315B4D"

    def __init__(
        self,
        master,
        tornar_inici: Callable[[], None],
        comparar_partits: Callable[[str, str], None],
    ) -> None:
        super().__init__(
            master,
            fg_color=self.COLOR_FONS,
            corner_radius=0,
        )

        self.tornar_inici = tornar_inici
        self.comparar_partits = comparar_partits

        self.partits_guardats: list[dict] = []
        self.rutes_seleccionades: list[str] = []

        self.targetes: list[ctk.CTkFrame] = []

        self.scroll: ctk.CTkScrollableFrame | None = None
        self.etiqueta_seleccio: ctk.CTkLabel | None = None
        self.boto_comparar: ctk.CTkButton | None = None

        self.grid_columnconfigure(
            0,
            weight=1,
        )
        self.grid_rowconfigure(
            1,
            weight=1,
        )

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
            height=86,
        )
        capcalera.grid(
            row=0,
            column=0,
            sticky="ew",
        )
        capcalera.grid_propagate(False)
        capcalera.grid_columnconfigure(
            0,
            weight=1,
        )

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
            text="Historial de partits",
            font=ctk.CTkFont(
                size=26,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(
            anchor="w"
        )

        ctk.CTkLabel(
            bloc_titol,
            text=(
                "Selecciona dos partits per comparar-los "
                "o utilitza els botons per editar-los."
            ),
            font=ctk.CTkFont(
                size=13,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack(
            anchor="w",
            pady=(2, 0),
        )

        ctk.CTkButton(
            capcalera,
            text="← TORNAR A L'INICI",
            command=self.tornar_inici,
            width=160,
            height=38,
            fg_color="transparent",
            hover_color="#17483A",
            border_width=1,
            border_color="#315B4D",
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
        contenidor = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        contenidor.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=22,
            pady=20,
        )
        contenidor.grid_columnconfigure(
            0,
            weight=1,
        )
        contenidor.grid_rowconfigure(
            0,
            weight=1,
        )

        self.scroll = ctk.CTkScrollableFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=20,
        )
        self.scroll.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        self.scroll.grid_columnconfigure(
            0,
            weight=1,
        )

        self._crear_barra_accions(
            contenidor
        )

        self._actualitzar_historial()

    # =====================================================
    # ACTUALITZACIÓ DE L'HISTORIAL
    # =====================================================

    def _actualitzar_historial(self) -> None:
        """
        Torna a llegir els fitxers de l'historial
        i reconstrueix les targetes.
        """

        if self.scroll is None:
            return

        for widget in self.scroll.winfo_children():
            widget.destroy()

        self.partits_guardats = obtenir_partits_guardats()
        self.targetes.clear()

        # Eliminem seleccions que ja no existeixen.
        rutes_existents = {
            partit.get("ruta", "")
            for partit in self.partits_guardats
        }

        self.rutes_seleccionades = [
            ruta
            for ruta in self.rutes_seleccionades
            if ruta in rutes_existents
        ]

        if not self.partits_guardats:
            self._mostrar_buit()
        else:
            for index, partit in enumerate(
                self.partits_guardats
            ):
                self._crear_targeta(
                    index=index,
                    partit=partit,
                )

        self._actualitzar_boto_comparar()

    # =====================================================
    # HISTORIAL BUIT
    # =====================================================

    def _mostrar_buit(self) -> None:
        if self.scroll is None:
            return

        bloc = ctk.CTkFrame(
            self.scroll,
            fg_color="transparent",
        )
        bloc.grid(
            row=0,
            column=0,
            pady=100,
        )

        ctk.CTkLabel(
            bloc,
            text="⚽",
            font=ctk.CTkFont(
                size=58,
            ),
            text_color=self.COLOR_VERD,
        ).pack()

        ctk.CTkLabel(
            bloc,
            text="Encara no hi ha partits guardats",
            font=ctk.CTkFont(
                size=21,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
        ).pack(
            pady=(12, 4),
        )

        ctk.CTkLabel(
            bloc,
            text="Finalitza un partit perquè aparegui aquí.",
            font=ctk.CTkFont(
                size=14,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack()

    # =====================================================
    # TARGETES DE PARTITS
    # =====================================================

    def _crear_targeta(
        self,
        index: int,
        partit: dict,
    ) -> None:
        if self.scroll is None:
            return

        dades = partit.get(
            "dades",
            {},
        )

        dades_partit = dades.get(
            "partit",
            {},
        )

        resum = dades.get(
            "resum",
            {},
        )

        equip = dades_partit.get(
            "equip",
            "Equip desconegut",
        )

        rival = dades_partit.get(
            "rival",
            "Rival desconegut",
        )

        data = dades_partit.get(
            "data_partit",
            "Sense data",
        )

        competicio = dades_partit.get(
            "competicio",
            "",
        )

        total = resum.get(
            "total",
            0,
        )

        bones = resum.get(
            "bones",
            0,
        )

        dolentes = resum.get(
            "dolentes",
            0,
        )

        precisio = resum.get(
            "precisio",
            0.0,
        )

        try:
            precisio_float = float(
                precisio
            )
        except (
            TypeError,
            ValueError,
        ):
            precisio_float = 0.0

        ruta = partit.get(
            "ruta",
            "",
        )

        seleccionat = (
            ruta in self.rutes_seleccionades
        )

        targeta = ctk.CTkFrame(
            self.scroll,
            fg_color=(
                self.COLOR_TARGETA_SELECCIONADA
                if seleccionat
                else self.COLOR_TARGETA
            ),
            corner_radius=16,
            border_width=1,
            border_color=(
                self.COLOR_VERD
                if seleccionat
                else self.COLOR_LINIA
            ),
        )
        targeta.grid(
            row=index,
            column=0,
            sticky="ew",
            padx=14,
            pady=8,
        )

        targeta.grid_columnconfigure(
            1,
            weight=1,
        )

        self.targetes.append(
            targeta
        )

        indicador = ctk.CTkLabel(
            targeta,
            text=(
                "●"
                if seleccionat
                else "○"
            ),
            font=ctk.CTkFont(
                size=24,
            ),
            text_color=(
                self.COLOR_VERD
                if seleccionat
                else self.COLOR_TEXT_SECUNDARI
            ),
            width=42,
            cursor="hand2",
        )
        indicador.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(14, 4),
        )

        bloc_partit = ctk.CTkFrame(
            targeta,
            fg_color="transparent",
            cursor="hand2",
        )
        bloc_partit.grid(
            row=0,
            column=1,
            rowspan=2,
            sticky="w",
            padx=10,
            pady=14,
        )

        etiqueta_partit = ctk.CTkLabel(
            bloc_partit,
            text=f"{equip}  —  {rival}",
            font=ctk.CTkFont(
                size=17,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT,
            cursor="hand2",
        )
        etiqueta_partit.pack(
            anchor="w"
        )

        detall = data or "Sense data"

        if competicio:
            detall += f" · {competicio}"

        etiqueta_detall = ctk.CTkLabel(
            bloc_partit,
            text=detall,
            font=ctk.CTkFont(
                size=12,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
            cursor="hand2",
        )
        etiqueta_detall.pack(
            anchor="w",
            pady=(4, 0),
        )

        self._crear_dada(
            targeta=targeta,
            columna=2,
            titol="PASSADES",
            valor=str(total),
            color=self.COLOR_TEXT,
        )

        self._crear_dada(
            targeta=targeta,
            columna=3,
            titol="BONES",
            valor=str(bones),
            color=self.COLOR_VERD,
        )

        self._crear_dada(
            targeta=targeta,
            columna=4,
            titol="DOLENTES",
            valor=str(dolentes),
            color=self.COLOR_VERMELL,
        )

        self._crear_dada(
            targeta=targeta,
            columna=5,
            titol="PRECISIÓ",
            valor=f"{precisio_float:.1f} %",
            color=self.COLOR_GROC,
        )

        bloc_botons = ctk.CTkFrame(
            targeta,
            fg_color="transparent",
        )
        bloc_botons.grid(
            row=0,
            column=6,
            rowspan=2,
            padx=(10, 16),
            pady=12,
        )

        ctk.CTkButton(
            bloc_botons,
            text="✎ EDITAR",
            command=lambda r=ruta: self._editar_partit(
                r
            ),
            width=92,
            height=32,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).pack(
            pady=(0, 6),
        )

        ctk.CTkButton(
            bloc_botons,
            text="🗑 ELIMINAR",
            command=lambda r=ruta: self._eliminar_partit(
                r
            ),
            width=92,
            height=32,
            fg_color=self.COLOR_VERMELL,
            hover_color="#DC2626",
            text_color="#FFFFFF",
            font=ctk.CTkFont(
                size=11,
                weight="bold",
            ),
        ).pack()

        widgets_seleccionables = (
            indicador,
            bloc_partit,
            etiqueta_partit,
            etiqueta_detall,
        )

        for widget in widgets_seleccionables:
            widget.bind(
                "<Button-1>",
                lambda event,
                r=ruta,
                t=targeta,
                i=indicador: self._seleccionar_partit(
                    ruta=r,
                    targeta=t,
                    indicador=i,
                ),
            )

    # =====================================================
    # DADES DE LA TARGETA
    # =====================================================

    def _crear_dada(
        self,
        targeta: ctk.CTkFrame,
        columna: int,
        titol: str,
        valor: str,
        color: str,
    ) -> None:
        bloc = ctk.CTkFrame(
            targeta,
            fg_color="transparent",
            width=105,
        )
        bloc.grid(
            row=0,
            column=columna,
            rowspan=2,
            padx=8,
            pady=12,
        )

        ctk.CTkLabel(
            bloc,
            text=titol,
            font=ctk.CTkFont(
                size=10,
                weight="bold",
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        ).pack()

        ctk.CTkLabel(
            bloc,
            text=valor,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
            text_color=color,
        ).pack(
            pady=(5, 0),
        )

    # =====================================================
    # SELECCIÓ DE PARTITS
    # =====================================================

    def _seleccionar_partit(
        self,
        ruta: str,
        targeta: ctk.CTkFrame,
        indicador: ctk.CTkLabel,
    ) -> None:
        if not ruta:
            return

        if ruta in self.rutes_seleccionades:
            self.rutes_seleccionades.remove(
                ruta
            )

            targeta.configure(
                fg_color=self.COLOR_TARGETA,
                border_color=self.COLOR_LINIA,
            )

            indicador.configure(
                text="○",
                text_color=self.COLOR_TEXT_SECUNDARI,
            )

        else:
            if len(self.rutes_seleccionades) >= 2:
                messagebox.showwarning(
                    "Límit de selecció",
                    "Només pots seleccionar dos partits.",
                    parent=self,
                )
                return

            self.rutes_seleccionades.append(
                ruta
            )

            targeta.configure(
                fg_color=self.COLOR_TARGETA_SELECCIONADA,
                border_color=self.COLOR_VERD,
            )

            indicador.configure(
                text="●",
                text_color=self.COLOR_VERD,
            )

        self._actualitzar_boto_comparar()

    # =====================================================
    # EDITAR PARTIT
    # =====================================================

    def _editar_partit(
        self,
        ruta: str,
    ) -> None:
        partit = self._obtenir_partit_per_ruta(
            ruta
        )

        if partit is None:
            messagebox.showerror(
                "Error",
                "No s'han pogut trobar les dades del partit.",
                parent=self,
            )
            return

        dades = partit.get(
            "dades",
            {},
        )

        dades_partit = dades.get(
            "partit",
            {},
        )

        equip_actual = dades_partit.get(
            "equip",
            "",
        )

        rival_actual = dades_partit.get(
            "rival",
            "",
        )

        competicio_actual = dades_partit.get(
            "competicio",
            "",
        )

        data_actual = dades_partit.get(
            "data_partit",
            "",
        )

        equip_nou = simpledialog.askstring(
            "Editar partit",
            "Nom de l'equip:",
            initialvalue=equip_actual,
            parent=self,
        )

        if equip_nou is None:
            return

        equip_nou = equip_nou.strip()

        if not equip_nou:
            messagebox.showwarning(
                "Dades incompletes",
                "El nom de l'equip no pot estar buit.",
                parent=self,
            )
            return

        rival_nou = simpledialog.askstring(
            "Editar partit",
            "Nom del rival:",
            initialvalue=rival_actual,
            parent=self,
        )

        if rival_nou is None:
            return

        rival_nou = rival_nou.strip()

        if not rival_nou:
            messagebox.showwarning(
                "Dades incompletes",
                "El nom del rival no pot estar buit.",
                parent=self,
            )
            return

        competicio_nova = simpledialog.askstring(
            "Editar partit",
            "Competició:",
            initialvalue=competicio_actual,
            parent=self,
        )

        if competicio_nova is None:
            return

        data_nova = simpledialog.askstring(
            "Editar partit",
            "Data del partit:",
            initialvalue=data_actual,
            parent=self,
        )

        if data_nova is None:
            return

        try:
            nova_ruta = editar_partit(
                ruta_fitxer=ruta,
                equip=equip_nou,
                rival=rival_nou,
                competicio=competicio_nova,
                data_partit=data_nova,
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
        ) as error:
            messagebox.showerror(
                "No s'ha pogut editar",
                str(error),
                parent=self,
            )
            return

        if ruta in self.rutes_seleccionades:
            index_seleccio = self.rutes_seleccionades.index(
                ruta
            )

            self.rutes_seleccionades[
                index_seleccio
            ] = str(nova_ruta)

        self._actualitzar_historial()

        messagebox.showinfo(
            "Partit actualitzat",
            "Les dades del partit s'han modificat correctament.",
            parent=self,
        )

    # =====================================================
    # ELIMINAR PARTIT
    # =====================================================

    def _eliminar_partit(
        self,
        ruta: str,
    ) -> None:
        partit = self._obtenir_partit_per_ruta(
            ruta
        )

        nom_partit = "aquest partit"

        if partit is not None:
            dades_partit = (
                partit.get("dades", {})
                .get("partit", {})
            )

            equip = dades_partit.get(
                "equip",
                "Equip",
            )

            rival = dades_partit.get(
                "rival",
                "Rival",
            )

            nom_partit = f"{equip} — {rival}"

        confirmar = messagebox.askyesno(
            "Eliminar partit",
            (
                f"Vols eliminar el partit:\n\n"
                f"{nom_partit}?\n\n"
                f"Aquesta acció no es pot desfer."
            ),
            icon="warning",
            parent=self,
        )

        if not confirmar:
            return

        try:
            eliminar_partit(
                ruta
            )

        except (
            FileNotFoundError,
            ValueError,
            OSError,
        ) as error:
            messagebox.showerror(
                "No s'ha pogut eliminar",
                str(error),
                parent=self,
            )
            return

        if ruta in self.rutes_seleccionades:
            self.rutes_seleccionades.remove(
                ruta
            )

        self._actualitzar_historial()

        messagebox.showinfo(
            "Partit eliminat",
            "El partit s'ha eliminat de l'historial.",
            parent=self,
        )

    # =====================================================
    # LOCALITZAR UN PARTIT
    # =====================================================

    def _obtenir_partit_per_ruta(
        self,
        ruta: str,
    ) -> dict | None:
        for partit in self.partits_guardats:
            if partit.get("ruta") == ruta:
                return partit

        return None

    # =====================================================
    # BARRA D'ACCIONS
    # =====================================================

    def _crear_barra_accions(
        self,
        contenidor: ctk.CTkFrame,
    ) -> None:
        barra = ctk.CTkFrame(
            contenidor,
            fg_color=self.COLOR_PANELL,
            corner_radius=18,
            height=76,
        )
        barra.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(14, 0),
        )
        barra.grid_propagate(False)
        barra.grid_columnconfigure(
            0,
            weight=1,
        )

        self.etiqueta_seleccio = ctk.CTkLabel(
            barra,
            text="0 de 2 partits seleccionats",
            font=ctk.CTkFont(
                size=13,
            ),
            text_color=self.COLOR_TEXT_SECUNDARI,
        )
        self.etiqueta_seleccio.grid(
            row=0,
            column=0,
            sticky="w",
            padx=22,
        )

        ctk.CTkButton(
            barra,
            text="ACTUALITZAR",
            command=self._actualitzar_historial,
            width=130,
            height=42,
            fg_color="transparent",
            hover_color="#17483A",
            border_width=1,
            border_color="#315B4D",
            text_color=self.COLOR_TEXT,
            font=ctk.CTkFont(
                size=12,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            padx=(10, 0),
        )

        self.boto_comparar = ctk.CTkButton(
            barra,
            text="COMPARAR PARTITS",
            command=self._executar_comparacio,
            width=220,
            height=42,
            fg_color=self.COLOR_BOTO_DESACTIVAT,
            hover_color=self.COLOR_BOTO_DESACTIVAT,
            state="disabled",
            text_color="#789488",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )
        self.boto_comparar.grid(
            row=0,
            column=2,
            padx=22,
        )

    # =====================================================
    # ACTUALITZAR BOTÓ DE COMPARACIÓ
    # =====================================================

    def _actualitzar_boto_comparar(self) -> None:
        quantitat = len(
            self.rutes_seleccionades
        )

        if self.etiqueta_seleccio is not None:
            self.etiqueta_seleccio.configure(
                text=(
                    f"{quantitat} de 2 "
                    f"partits seleccionats"
                )
            )

        if self.boto_comparar is None:
            return

        if quantitat == 2:
            self.boto_comparar.configure(
                state="normal",
                fg_color=self.COLOR_VERD,
                hover_color="#16A34A",
                text_color="#04130E",
            )

        else:
            self.boto_comparar.configure(
                state="disabled",
                fg_color=self.COLOR_BOTO_DESACTIVAT,
                hover_color=self.COLOR_BOTO_DESACTIVAT,
                text_color="#789488",
            )

    # =====================================================
    # EXECUTAR COMPARACIÓ
    # =====================================================

    def _executar_comparacio(self) -> None:
        if len(self.rutes_seleccionades) != 2:
            return

        ruta_1 = self.rutes_seleccionades[0]
        ruta_2 = self.rutes_seleccionades[1]

        self.comparar_partits(
            ruta_1,
            ruta_2,
        )