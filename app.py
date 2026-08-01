import customtkinter as ctk

from models.match_data import MatchData
from utils.history_manager import guardar_partit
from views.comparison import ComparisonView
from views.history import HistoryView
from views.home import HomeView
from views.loading import LoadingView
from views.match import MatchView
from views.results import ResultsView
from views.setup import SetupView


# =========================================================
# CONFIGURACIÓ GENERAL
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


# =========================================================
# APLICACIÓ PRINCIPAL
# =========================================================

class FootballPassAnalyzer(ctk.CTk):
    """
    Finestra principal de FPA - Football Pass Analyzer.

    Gestiona:
    - les dades del partit;
    - les transicions entre pantalles;
    - el guardat automàtic;
    - l'historial;
    - la comparació de partits.
    """

    COLOR_FONS = "#061B15"

    def __init__(self) -> None:
        super().__init__()

        self.title("FPA - Football Pass Analyzer")
        self.geometry("1450x900")
        self.minsize(1180, 760)

        self.configure(
            fg_color=self.COLOR_FONS
        )

        # Dades del partit actual.
        self.dades_partit = MatchData()

        # Pantalla visible.
        self.pantalla_actual = None

        # Evita guardar diverses vegades el mateix partit.
        self.partit_guardat = False

        # Identificador de la transició programada.
        self.transicio_programada = None

        self.mostrar_inici()

    # =====================================================
    # GESTIÓ DE PANTALLES
    # =====================================================

    def eliminar_pantalla_actual(self) -> None:
        """
        Elimina la pantalla visible.
        """

        if self.pantalla_actual is None:
            return

        try:
            self.pantalla_actual.destroy()

        except Exception as error:
            print(
                "No s'ha pogut destruir la pantalla actual: "
                f"{error}"
            )

        finally:
            self.pantalla_actual = None

    def cancel_lar_transicio_programada(self) -> None:
        """
        Cancel·la una transició anterior si encara està pendent.
        """

        if self.transicio_programada is None:
            return

        try:
            self.after_cancel(
                self.transicio_programada
            )

        except Exception:
            pass

        self.transicio_programada = None

    def mostrar_pantalla(
        self,
        classe_pantalla,
        **arguments,
    ) -> None:
        """
        Mostra directament una pantalla.
        """

        self.cancel_lar_transicio_programada()
        self.eliminar_pantalla_actual()

        try:
            pantalla = classe_pantalla(
                master=self,
                **arguments,
            )

            pantalla.pack(
                fill="both",
                expand=True,
            )

            self.pantalla_actual = pantalla

        except Exception as error:
            print(
                "Error en carregar la pantalla "
                f"{classe_pantalla.__name__}: {error}"
            )

            raise

    def mostrar_amb_carrega(
        self,
        classe_pantalla,
        missatge: str = "Carregant",
        retard: int = 120,
        **arguments,
    ) -> None:
        """
        Mostra breument una pantalla de càrrega.

        Els retards són petits per no alentir artificialment
        l'aplicació.
        """

        self.cancel_lar_transicio_programada()
        self.eliminar_pantalla_actual()

        pantalla_carrega = LoadingView(
            master=self,
            missatge=missatge,
        )

        pantalla_carrega.pack(
            fill="both",
            expand=True,
        )

        self.pantalla_actual = pantalla_carrega

        # Mostra immediatament el contingut de càrrega.
        self.update_idletasks()

        self.transicio_programada = self.after(
            max(50, retard),
            lambda: self._completar_transicio(
                classe_pantalla,
                arguments,
            ),
        )

    def _completar_transicio(
        self,
        classe_pantalla,
        arguments: dict,
    ) -> None:
        """
        Completa la transició programada.
        """

        self.transicio_programada = None

        self.mostrar_pantalla(
            classe_pantalla,
            **arguments,
        )

    # =====================================================
    # INICI
    # =====================================================

    def mostrar_inici(
        self,
        amb_carrega: bool = False,
    ) -> None:
        """
        Mostra la pantalla principal.
        """

        arguments = {
            "nou_partit": self.mostrar_configuracio,
            "carregar_partit": self.carregar_partit,
            "sortir_aplicacio": self.tancar_aplicacio,
        }

        if amb_carrega:
            self.mostrar_amb_carrega(
                HomeView,
                missatge="Tornant a l'inici",
                retard=90,
                **arguments,
            )

        else:
            self.mostrar_pantalla(
                HomeView,
                **arguments,
            )

    # =====================================================
    # CONFIGURACIÓ
    # =====================================================

    def mostrar_configuracio(self) -> None:
        """
        Obre la configuració del partit.
        """

        self.mostrar_amb_carrega(
            SetupView,
            missatge="Preparant el partit",
            retard=100,
            dades_partit=self.dades_partit,
            tornar_inici=lambda: self.mostrar_inici(
                amb_carrega=True
            ),
            començar_partit=self.mostrar_partit,
        )

    # =====================================================
    # CAMP INTERACTIU
    # =====================================================

    def mostrar_partit(self) -> None:
        """
        Obre el camp interactiu.
        """

        self.mostrar_amb_carrega(
            MatchView,
            missatge="Carregant el camp",
            retard=120,
            dades_partit=self.dades_partit,
            tornar_configuracio=self.mostrar_configuracio,
            finalitzar_partit=self.mostrar_resultats,
        )

    # =====================================================
    # RESULTATS
    # =====================================================

    def mostrar_resultats(self) -> None:
        """
        Guarda el partit una sola vegada i mostra els resultats.
        """

        if not self.partit_guardat:

            try:
                ruta_guardada = guardar_partit(
                    self.dades_partit
                )

                self.partit_guardat = True

                print(
                    "Partit guardat correctament a: "
                    f"{ruta_guardada}"
                )

            except Exception as error:
                print(
                    "No s'ha pogut guardar el partit: "
                    f"{error}"
                )

        # Resultats és una pantalla més pesada perquè calcula
        # estadístiques i centralitats. Mantenim una transició
        # lleugerament més llarga, però molt inferior a l'anterior.
        self.mostrar_amb_carrega(
            ResultsView,
            missatge="Calculant els resultats",
            retard=180,
            dades_partit=self.dades_partit,
            tornar_partit=self.mostrar_partit,
            nou_partit=self.crear_nou_partit,
            tornar_inici=lambda: self.mostrar_inici(
                amb_carrega=True
            ),
        )

    # =====================================================
    # HISTORIAL
    # =====================================================

    def carregar_partit(self) -> None:
        """
        Obre l'historial de partits.
        """

        self.mostrar_amb_carrega(
            HistoryView,
            missatge="Carregant l'historial",
            retard=120,
            tornar_inici=lambda: self.mostrar_inici(
                amb_carrega=True
            ),
            comparar_partits=self.mostrar_comparacio,
        )

    # =====================================================
    # COMPARACIÓ
    # =====================================================

    def mostrar_comparacio(
        self,
        ruta_partit_1: str,
        ruta_partit_2: str,
    ) -> None:
        """
        Obre la comparació de dos partits.
        """

        self.mostrar_amb_carrega(
            ComparisonView,
            missatge="Comparant els partits",
            retard=150,
            ruta_partit_1=ruta_partit_1,
            ruta_partit_2=ruta_partit_2,
            tornar_historial=self.carregar_partit,
            tornar_inici=lambda: self.mostrar_inici(
                amb_carrega=True
            ),
        )

    # =====================================================
    # NOU PARTIT
    # =====================================================

    def crear_nou_partit(self) -> None:
        """
        Reinicia les dades del partit.
        """

        self.dades_partit = MatchData()
        self.partit_guardat = False

        self.mostrar_configuracio()

    # =====================================================
    # TANCAR
    # =====================================================

    def tancar_aplicacio(self) -> None:
        """
        Demana confirmació abans de tancar.
        """

        from tkinter import messagebox

        confirmacio = messagebox.askyesno(
            "Sortir",
            "Segur que vols tancar FPA - Football Pass Analyzer?",
        )

        if confirmacio:
            self.cancel_lar_transicio_programada()
            self.destroy()


# =========================================================
# EXECUCIÓ
# =========================================================

if __name__ == "__main__":
    aplicacio = FootballPassAnalyzer()
    aplicacio.mainloop()
    