from manim import *

# Configuramos la plantilla para mantener la consistencia matemática
my_template = TexTemplate()
MathTex.set_default(color=BLACK, tex_template=my_template)
Text.set_default(color=BLACK)

class ScreeningMechanism(Scene):
    def construct(self):
        # Fondo blanco para Keynote
        self.camera.background_color = WHITE

        # --- 1. El Halo de Materia Oscura ---
        # Posicionado en el centro del espacio de Relatividad General
        halo_core = Dot(radius=0.3, color=BLUE_E)
        halo_glow = Dot(radius=0.7, color=BLUE_E, fill_opacity=0.25)
        halo = VGroup(halo_glow, halo_core)
        
        halo_label = Text(
            "Halo de Materia Oscura\n(Alta Densidad)", 
            font="Helvetica", 
            font_size=18, 
            color=BLUE_E, 
            line_spacing=1.2
        ).next_to(halo, DOWN, buff=0.6)

        # --- 2. El Radio de Apantallamiento (Vainshtein) ---
        v_radius = 3.2
        # Círculo punteado que delimita la zona de screening
        screening_circle = DashedVMobject(
            Circle(radius=v_radius, color=DARK_GRAY, stroke_width=3), 
            num_dashes=50
        )
        
        # Flecha indicando el radio a 55 grados para no interferir con los textos laterales
        angle = 55 * DEGREES
        arrow_dir = np.array([np.cos(angle), np.sin(angle), 0])
        start_point = halo_core.get_center() + arrow_dir * 0.3
        end_point = halo_core.get_center() + arrow_dir * v_radius
        
        radius_arrow = Arrow(
            start_point, 
            end_point, 
            buff=0, 
            color=DARK_GRAY, 
            stroke_width=3,
            max_tip_length_to_length_ratio=0.15
        )
        
        rv_label = MathTex("r_V", font_size=32, color=DARK_GRAY)
        rv_text = Text("Radio de Vainshtein", font_size=16, font="Helvetica", color=DARK_GRAY)
        rv_group = VGroup(rv_label, rv_text).arrange(RIGHT, buff=0.15)
        rv_group.next_to(end_point, UR, buff=0.1)

        # --- 3. Las Zonas Físicas ---
        # Zona Interior (Gravedad Estándar) - Ubicada simétricamente a la izquierda
        gr_math = MathTex(r"G_{\mathrm{eff}} = G_{\mathrm{N}}", font_size=42, color=GREEN_E)
        gr_text = Text("RG", font_size=18, font="Helvetica", color=GREEN_E)
        inside_zone = VGroup(gr_math, gr_text).arrange(DOWN, buff=0.15)
        inside_zone.shift(LEFT * 1.85 + UP * 0.4)

        # Zona Exterior (Quinta Fuerza) - Ubicada de forma balanceada a la derecha
        # El anillo translúcido rojo representa visualmente la presencia del campo escalar activo
        fifth_force_field = Annulus(
            inner_radius=v_radius, 
            outer_radius=8.0, 
            color=RED_E, 
            fill_opacity=0.06, 
            stroke_width=0
        )
        
        mod_math = MathTex(r"G_{\mathrm{eff}} > G_{\mathrm{N}}", font_size=42, color=RED_E)
        mod_text = Text("Extensiones a RG", font_size=18, font="Helvetica", color=RED_E)
        outside_zone = VGroup(mod_math, mod_text).arrange(DOWN, buff=0.15)
        outside_zone.shift(RIGHT * 4.9 + UP * 0.4)

        # --- ANIMACIÓN ---
        
        # Paso 1: Aparece el halo y su etiqueta
        self.play(
            FadeIn(halo_glow), 
            GrowFromCenter(halo_core), 
            Write(halo_label), 
            run_time=1.5
        )
        self.wait(1)

        # Paso 2: Se define la frontera de apantallamiento y su radio
        self.play(Create(screening_circle), run_time=1.5)
        self.play(GrowArrow(radius_arrow), FadeIn(rv_group, shift=UP))
        self.wait(1)

        # Paso 3: Revelamos la física INTERIOR (GR)
        self.play(Write(gr_math), FadeIn(gr_text, shift=DOWN))
        self.wait(1.5)

        # Paso 4: Revelamos la física EXTERIOR (Quinta Fuerza)
        self.play(
            FadeIn(fifth_force_field), 
            Write(mod_math), 
            FadeIn(mod_text, shift=DOWN), 
            run_time=2
        )
        
        # Mantenemos la imagen final
        self.wait(3)