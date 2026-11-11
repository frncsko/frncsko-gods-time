import customtkinter as ctk

# Configuración visual global
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AdSelectApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AdSelect - Gestor de Campañas & Creativos")
        self.geometry("1100x700")
        self.minsize(950, 600)

        # Configuración de rejilla principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_panel_principal()

    def crear_sidebar(self):
        # Barra lateral izquierda
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        # Logotipo / Título
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="AdSelect",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 20), sticky="w")

        # Botones de navegación
        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame,
            text=" Panel General",
            fg_color="#1f538d",
            anchor="w",
            font=ctk.CTkFont(size=14)
        )
        self.btn_dashboard.grid(row=1, column=0, padx=15, pady=8, sticky="ew")

        self.btn_ads = ctk.CTkButton(
            self.sidebar_frame,
            text=" Mis Creativos",
            fg_color="transparent",
            text_color="#c0c0c0",
            hover_color="#2b2b2b",
            anchor="w",
            font=ctk.CTkFont(size=14)
        )
        self.btn_ads.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        self.btn_metrics = ctk.CTkButton(
            self.sidebar_frame,
            text=" Rendimiento / ROI",
            fg_color="transparent",
            text_color="#c0c0c0",
            hover_color="#2b2b2b",
            anchor="w",
            font=ctk.CTkFont(size=14)
        )
        self.btn_metrics.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.btn_billing = ctk.CTkButton(
            self.sidebar_frame,
            text=" Presupuesto & Facturación",
            fg_color="transparent",
            text_color="#c0c0c0",
            hover_color="#2b2b2b",
            anchor="w",
            font=ctk.CTkFont(size=14)
        )
        self.btn_billing.grid(row=4, column=0, padx=15, pady=8, sticky="ew")

        # Estado del servicio / Saldo
        self.balance_card = ctk.CTkFrame(self.sidebar_frame, fg_color="#18181b", corner_radius=10)
        self.balance_card.grid(row=7, column=0, padx=15, pady=20, sticky="ew")

        ctk.CTkLabel(
            self.balance_card,
            text="Saldo disponible:",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        ).pack(anchor="w", padx=12, pady=(10, 2))

        ctk.CTkLabel(
            self.balance_card,
            text="$350.00 USD",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4ade80"
        ).pack(anchor="w", padx=12, pady=(0, 10))

    def crear_panel_principal(self):
        # Contenedor principal derecho
        self.main_frame = ctk.CTkFrame(self, fg_color="#121214", corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=2)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # 1. Cabecera superior (Top Bar)
        self.crear_topbar()

        # 2. Métricas rápidas (KPI Cards)
        self.crear_metricas()

        # 3. Lista de Anuncios y Selector
        self.crear_lista_anuncios()

        # 4. Panel lateral de edición / previsualización
        self.crear_panel_edicion()

    def crear_topbar(self):
        topbar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        topbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        title = ctk.CTkLabel(
            topbar,
            text="Gestor de Anuncios Activos",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(side="left")

        btn_new_ad = ctk.CTkButton(
            topbar,
            text="+ Nuevo Creativo",
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=13, weight="bold"),
            width=140
        )
        btn_new_ad.pack(side="right")

    def crear_metricas(self):
        metrics_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        metrics_container.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        metrics_container.grid_columnconfigure((0, 1, 2, 3), weight=1)

        datos = [
            ("Impresiones", "124,520", "#38bdf8"),
            ("Clics Totales", "4,830", "#a
