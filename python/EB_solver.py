from manim import *
import numpy as np

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

class EBSolverFlow(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Title ---
        title = Tex(
            r"\text{Flujo de un } \textit{Einstein-Boltzmann Solver} \text{ (CLASS)}",
            font_size=28
        ).to_edge(UP, buff=0.4)
        
        self.play(Write(title))
        self.wait(0.5)

        # --- Setup Layout Coordinates ---
        xs = [-4.4, 0.0, 4.4]
        box_y = DOWN * 0.2
        box_h = 3.2

        # --- Block 1: Entradas (Input Parameters) ---
        box1 = RoundedRectangle(width=3.2, height=box_h, corner_radius=0.15, color=BLUE_E, stroke_width=2.5, fill_color=BLUE_E, fill_opacity=0.04).move_to(np.array([xs[0], box_y[1], 0]))
        label1 = Text("Parámetros", font_size=20, weight=BOLD).next_to(box1, UP, buff=0.25)
        desc1 = Text("Entrada (Input)", font_size=12, color=GRAY).next_to(box1.get_top(), DOWN, buff=0.2)
        
        # 2x2 parameter layout for square shape
        v1 = MathTex(r"\omega_b", font_size=24)
        v2 = MathTex(r"\omega_{cdm}", font_size=24)
        v3 = MathTex(r"H_0", font_size=24)
        v4 = MathTex(r"A_s, n_s", font_size=24)
        params_group = VGroup(
            VGroup(v1, v2).arrange(RIGHT, buff=0.6),
            VGroup(v3, v4).arrange(RIGHT, buff=0.6)
        ).arrange(DOWN, buff=0.5).move_to(box1.get_center() + DOWN * 0.15)
        
        block1 = VGroup(box1, label1, desc1, params_group)

        # --- Block 2: Computaciones (CLASS Solver Core) ---
        box2 = RoundedRectangle(width=3.6, height=box_h, corner_radius=0.15, color=ORANGE, stroke_width=2.5, fill_color=ORANGE, fill_opacity=0.04).move_to(np.array([xs[1], box_y[1], 0]))
        label2 = Text("Cálculos", font_size=20, weight=BOLD).next_to(box2, UP, buff=0.25)
        desc2 = Text("Resolución de Ecuaciones", font_size=12, color=GRAY).next_to(box2.get_top(), DOWN, buff=0.2)
        
        # Side-by-side equations layout
        eq1 = MathTex(r"G_{\mu\nu} = 8\pi G T_{\mu\nu}", font_size=18)
        eq2 = MathTex(r"\frac{df_i}{d\tau} = C[f_i]", font_size=18)
        eqs_group = VGroup(eq1, eq2).arrange(RIGHT, buff=0.3)
        
        # Divider line
        divider = Line(LEFT * 1.4, RIGHT * 1.4, stroke_width=1.2, color=GRAY_B)
        
        # Enumeration list of computations
        l1 = Text("1. Fondo (Background)", font_size=14)
        l2 = Text("2. Termodinámica", font_size=14)
        l3 = Text("3. Perturbaciones", font_size=14)
        list_group = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        
        box2_content = VGroup(eqs_group, divider, list_group).arrange(DOWN, buff=0.22).move_to(box2.get_center() + DOWN * 0.15)

        # --- Block 3: Observables (Output Spectra) ---
        box3 = RoundedRectangle(width=3.2, height=box_h, corner_radius=0.15, color=PURPLE_E, stroke_width=2.5, fill_color=PURPLE_E, fill_opacity=0.04).move_to(np.array([xs[2], box_y[1], 0]))
        label3 = Text("Observables", font_size=20, weight=BOLD).next_to(box3, UP, buff=0.25)
        desc3 = Text("Salida (Output)", font_size=12, color=GRAY).next_to(box3.get_top(), DOWN, buff=0.2)
        
        ob_axes = Axes(x_range=[0, 10], y_range=[0, 2], x_length=1.5, y_length=1.5, axis_config={"color": GRAY, "stroke_width": 1.5, "include_tip": False}).move_to(box3.get_center() + DOWN * 0.25)
        ob_curve = ob_axes.plot(lambda x: 1.8 * np.exp(-0.25*x) * np.sin(1.2*x)**2 + 0.1, color=PURPLE_E, stroke_width=3)
        ob_math = MathTex(r"C_\ell^{TT}, P(k)", font_size=22).move_to(box3.get_center() + UP * 0.8)
        block3 = VGroup(box3, label3, desc3, ob_axes, ob_curve, ob_math)

        # --- Main Connecting Arrows ---
        main_arrow1 = Arrow(box1.get_right(), box2.get_left(), color=GRAY, buff=0.1, stroke_width=3)
        main_arrow2 = Arrow(box2.get_right(), box3.get_left(), color=GRAY, buff=0.1, stroke_width=3)

        # --- Animation Timeline ---

        # 1. Show Input Parameters
        self.play(Create(box1), Write(label1), Write(desc1), run_time=1.2)
        self.play(FadeIn(params_group))
        self.wait(0.5)

        # Pulse 1: Input Parameter -> Computations Box
        pulse = Dot(color=YELLOW, radius=0.1)
        pulse.move_to(box1.get_right())
        self.play(FadeIn(pulse))
        self.play(Create(main_arrow1), MoveAlongPath(pulse, Line(box1.get_right(), box2.get_left())), run_time=0.8)
        self.play(FadeOut(pulse))

        # 2. Show Calculations Box
        self.play(Create(box2), Write(label2), Write(desc2), run_time=1.0)
        self.wait(0.3)

        # 3. Write Equations and Divider
        self.play(Write(eqs_group), Create(divider), run_time=1.0)
        self.wait(0.3)

        # 4. Write List of Computations step-by-step
        self.play(Write(l1), run_time=0.6)
        self.play(Write(l2), run_time=0.6)
        self.play(Write(l3), run_time=0.6)
        self.wait(0.5)

        # Pulse 2: Computations Box -> Observables
        pulse.move_to(box2.get_right())
        self.play(FadeIn(pulse))
        self.play(Create(main_arrow2), MoveAlongPath(pulse, Line(box2.get_right(), box3.get_left())), run_time=0.8)
        self.play(FadeOut(pulse))

        # 5. Show Observables (Spectra Output)
        self.play(Create(box3), Write(label3), Write(desc3), run_time=1.2)
        self.play(Create(ob_axes), Write(ob_math))
        self.play(Create(ob_curve), run_time=1.0)
        
        # Final hold
        self.wait(3.0)
