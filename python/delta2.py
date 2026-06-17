from manim import *
import numpy as np

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

class StructureFormation(Scene):
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
        # We manually position the y-label to the right of the axis to avoid collision with the peak
        y_label = axes.get_y_axis_label(MathTex(r"\delta"), direction=RIGHT).shift(RIGHT * 0.3 + UP * 0.2)
        axes_group = VGroup(axes, x_label, y_label)

        # --- Setup Particle Box ---
        # Draw the physical bounding box (now a Square)
        bounding_box = Square(side_length=box_side, color=BLACK).move_to(box_center)
        box_label = Text("Animación de Colapso", font_size=24).next_to(bounding_box, DOWN, buff=0.3)
        
        # Generate initial random particle positions
        np.random.seed(42) # Keeps the particle layout exactly the same every time you render
        num_particles = 350
        initial_positions = []
        particles = VGroup()
        
        for _ in range(num_particles):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_positions.append(np.array([x, y, 0]))
            
            # Start them all blue
            p = Dot(box_center + np.array([x, y, 0]), radius=0.03, color=BLUE_E)
            particles.add(p)

        # --- The Physics Engine ---
        t_tracker = ValueTracker(0.0)

        # 1. The Particle Updater (Spherical Collapse in 2D)
        def update_particles(mob):
            t = t_tracker.get_value()
            current_color = interpolate_color(BLUE_E, RED, t)
            
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                
                # Radial distance from the center of the box
                r_init = np.sqrt(init_x**2 + init_y**2)
                
                # Non-uniform spherical collapse factor:
                # The core collapses faster (up to 85%), outer parts slower.
                # Since the scale factor is a monotonic function of r_init, particles do not cross.
                collapse_factor = 1.0 - t * 0.85 * np.exp(-0.12 * r_init**2)
                
                new_x = init_x * collapse_factor
                new_y = init_y * collapse_factor
                
                p.move_to(box_center + np.array([new_x, new_y, 0]))
                p.set_color(current_color)

        # 2. The Density Curve Updater
        def get_density_curve():
            t = t_tracker.get_value()
            amp = 0.3 + 2.7 * t
            sigma = 1.5 - 1.1 * t
            void_drop = 0.2 * t
            
            curve = axes.plot(
                lambda x: amp * np.exp(- (x**2) / (2 * sigma**2)) - void_drop,
                color=interpolate_color(BLUE_E, RED, t),
                stroke_width=4
            )
            area = axes.get_area(curve, color=interpolate_color(BLUE_E, RED, t), opacity=0.3)
            return VGroup(curve, area)

        density_plot = always_redraw(get_density_curve)
        particles.add_updater(update_particles)

        # --- Dynamic Labels ---
        regime_label = always_redraw(
            lambda: Text(
                "Régimen Lineal" if t_tracker.get_value() < 0.5 else "Colapso no Lineal",
                font_size=36,
                color=BLUE_E if t_tracker.get_value() < 0.5 else RED
            ).to_edge(UP, buff=0.3)
        )
        
        delta_label = always_redraw(
            lambda: MathTex(
                r"\delta \ll 1" if t_tracker.get_value() < 0.5 else r"\delta \gg 1",
                font_size=42,
                color=BLUE_E if t_tracker.get_value() < 0.5 else RED
            ).next_to(regime_label, DOWN, buff=0.1)
        )

        # Time passing label
        time_label = always_redraw(
            lambda: Text(
                f"Tiempo: {t_tracker.get_value():.2f}",
                font_size=28
            ).to_edge(UR, buff=0.5)
        )

        # --- Animation Timeline ---
        self.play(Create(axes_group), Create(bounding_box), Write(box_label), run_time=1.5)
        self.wait(0.5)

        self.play(FadeIn(density_plot), FadeIn(particles), Write(regime_label), Write(delta_label), FadeIn(time_label))
        self.wait(1.5)

        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=6,
            rate_func=smooth
        )
        
        self.wait(3)