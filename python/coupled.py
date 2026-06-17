from manim import *
import numpy as np

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

class MultiSpeciesFormation(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Setup Layout ---
        # We split the screen:
        # Left: 2D Comoving Simulation Box (Square)
        # Right: 1D Density Contrast Plot (Axes)
        box_side = 4.0
        box_center = LEFT * 3.2 + UP * 0.2
        axes_center = RIGHT * 3.0 + DOWN * 0.5

        # --- Setup Axes ---
        axes = Axes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-0.5, 3.5, 1],
            axis_config={"color": BLACK, "include_numbers": False},
            x_length=5.0,
            y_length=4.0
        ).move_to(axes_center)

        x_label = axes.get_x_axis_label(MathTex(r"x"))
        # Repositioned to the right side to avoid collision with the axes/peaks
        y_label = axes.get_y_axis_label(MathTex(r"\delta"), direction=RIGHT).shift(RIGHT * 0.3 + UP * 0.2)
        axes_group = VGroup(axes, x_label, y_label)

        # --- Setup Particle Box ---
        bounding_box = Square(side_length=box_side, color=BLACK).move_to(box_center)
        box_label = Text("Animación Multi-Especie", font_size=24).next_to(bounding_box, DOWN, buff=0.3)
        
        # Generate initial random particle positions
        np.random.seed(42) 
        num_cdm = 300
        num_baryons = 300
        num_neutrinos = 300
        
        initial_cdm = []
        initial_bar = []
        initial_neu = []
        
        particles_cdm = VGroup()
        particles_bar = VGroup()
        particles_neu = VGroup()
        
        # Initialize Cold Dark Matter (Blue)
        for _ in range(num_cdm):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_cdm.append(np.array([x, y, 0]))
            particles_cdm.add(Dot(box_center + np.array([x, y, 0]), radius=0.025, color=BLUE_E, fill_opacity=0.8))

        # Initialize Baryons (Orange)
        for _ in range(num_baryons):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_bar.append(np.array([x, y, 0]))
            particles_bar.add(Dot(box_center + np.array([x, y, 0]), radius=0.025, color=ORANGE, fill_opacity=0.8))

        # Initialize Neutrinos (Green)
        for _ in range(num_neutrinos):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_neu.append(np.array([x, y, 0]))
            particles_neu.add(Dot(box_center + np.array([x, y, 0]), radius=0.025, color=GREEN_D, fill_opacity=0.7))

        # --- The Physics Engine ---
        t_tracker = ValueTracker(0.0)

        # 1. Particle Updaters (Spherical collapse in 2D)
        def update_cdm(mob):
            t = t_tracker.get_value()
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_cdm[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                # CDM: tight spherical collapse, core contracts by up to 82%
                collapse_factor = 1.0 - t * 0.82 * np.exp(-0.10 * r_init**2)
                p.move_to(box_center + np.array([init_x * collapse_factor, init_y * collapse_factor, 0]))

        def update_bar(mob):
            t = t_tracker.get_value()
            n = len(mob)
            # Gas pressure thermal motion
            noise_x = np.random.normal(0, 0.04 * t, n)
            noise_y = np.random.normal(0, 0.04 * t, n)
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_bar[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                # Baryons: moderate spherical collapse (up to 60% contraction) due to pressure support
                collapse_factor = 1.0 - t * 0.60 * np.exp(-0.06 * r_init**2)
                p.move_to(box_center + np.array([
                    init_x * collapse_factor + noise_x[i], 
                    init_y * collapse_factor + noise_y[i], 
                    0
                ]))

        def update_neu(mob):
            t = t_tracker.get_value()
            n = len(mob)
            # Huge thermal motion (free-streaming)
            noise_x = np.random.normal(0, 0.22 * t, n)
            noise_y = np.random.normal(0, 0.22 * t, n)
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_neu[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                # Neutrinos: very weak collapse (15% contraction) due to extremely high velocity dispersion
                collapse_factor = 1.0 - t * 0.15 * np.exp(-0.02 * r_init**2)
                p.move_to(box_center + np.array([
                    init_x * collapse_factor + noise_x[i], 
                    init_y * collapse_factor + noise_y[i], 
                    0
                ]))

        # 2. Density Curve Updater
        def get_density_curves():
            t = t_tracker.get_value()
            
            # CDM: High peak, narrow width
            amp_cdm = 0.3 + 3.0 * t
            sigma_cdm = 1.5 - 1.1 * t
            void_cdm = 0.25 * t
            
            # Baryons: Lower peak, wider width (pressure support)
            amp_bar = 0.3 + 1.2 * t
            sigma_bar = 1.5 - 0.5 * t
            void_bar = 0.15 * t

            # Neutrinos: Very flat, minimal collapse
            amp_neu = 0.3 + 0.15 * t
            sigma_neu = 1.5 - 0.1 * t
            void_neu = 0.03 * t
            
            curve_cdm = axes.plot(
                lambda x: amp_cdm * np.exp(- (x**2) / (2 * sigma_cdm**2)) - void_cdm,
                color=BLUE_E, stroke_width=4
            )
            curve_bar = axes.plot(
                lambda x: amp_bar * np.exp(- (x**2) / (2 * sigma_bar**2)) - void_bar,
                color=ORANGE, stroke_width=4
            )
            curve_neu = axes.plot(
                lambda x: amp_neu * np.exp(- (x**2) / (2 * sigma_neu**2)) - void_neu,
                color=GREEN_D, stroke_width=4
            )
            
            area_cdm = axes.get_area(curve_cdm, color=BLUE_E, opacity=0.15)
            area_bar = axes.get_area(curve_bar, color=ORANGE, opacity=0.2)
            area_neu = axes.get_area(curve_neu, color=GREEN_D, opacity=0.1)
            
            return VGroup(area_cdm, area_bar, area_neu, curve_cdm, curve_bar, curve_neu)

        density_plots = always_redraw(get_density_curves)
        particles_cdm.add_updater(update_cdm)
        particles_bar.add_updater(update_bar)
        particles_neu.add_updater(update_neu)

        # --- Labels ---
        title = always_redraw(
            lambda: Text(
                "Régimen Lineal" if t_tracker.get_value() < 0.5 else "Colapso Multi-Especie No Lineal",
                font_size=32, weight=BOLD
            ).to_edge(UP, buff=0.3)
        )

        # Temporizador (Time passing label)
        time_label = always_redraw(
            lambda: Text(
                f"Tiempo: {t_tracker.get_value():.2f}",
                font_size=24
            ).to_edge(UR, buff=0.5)
        )

        # --- Animation Timeline ---
        self.play(Create(axes_group), Create(bounding_box), Write(box_label), run_time=1.5)
        self.wait(0.5)

        # Show the initial roughly uniform state
        self.play(
            FadeIn(density_plots), 
            FadeIn(particles_cdm), 
            FadeIn(particles_bar), 
            FadeIn(particles_neu), 
            Write(title), 
            FadeIn(time_label)
        )
        self.wait(1.5)

        # Run the gravitational collapse
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=7,
            rate_func=smooth
        )
        
        # Hold on the final structure
        self.wait(3)