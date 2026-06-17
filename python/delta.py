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

        # --- Setup Axes ---
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-0.5, 3.5, 1],
            axis_config={"color": BLACK, "include_numbers": False},
            x_length=8,
            y_length=5
        ).shift(DOWN * 0.5)

        x_label = axes.get_x_axis_label(MathTex(r"x \text{ (Comoving Position)}"))
        # We manually position the y-label to the right so it doesn't collide with the axis/peak
        y_label = axes.get_y_axis_label(MathTex(r"\delta \text{ (Density Contrast)}"), direction=RIGHT).shift(RIGHT * 0.5 + UP * 0.2)

        axes_group = VGroup(axes, x_label, y_label)

        # --- The Physics Tracker ---
        # We use a time tracker 't' going from 0.0 (linear) to 1.0 (highly non-linear)
        t_tracker = ValueTracker(0.0)

        # --- The Density Function Engine ---
        def get_density_curve():
            t = t_tracker.get_value()
            
            # As 't' goes from 0 to 1, gravity forces the collapse:
            # 1. The peak amplitude grows massively
            amp = 0.3 + 2.7 * t
            
            # 2. The spatial width of the halo shrinks
            sigma = 1.5 - 1.1 * t
            
            # 3. The surrounding voids empty out (density drops below average)
            void_drop = 0.2 * t
            
            # Draw the curve using a Gaussian profile to represent the halo
            curve = axes.plot(
                lambda x: amp * np.exp(- (x**2) / (2 * sigma**2)) - void_drop,
                color=interpolate_color(BLUE_E, RED, t),
                stroke_width=4
            )
            
            # Shade the region under the curve to represent the physical mass
            area = axes.get_area(curve, color=interpolate_color(BLUE_E, RED, t), opacity=0.3)
            
            return VGroup(curve, area)

        density_plot = always_redraw(get_density_curve)

        # --- Dynamic Labels ---
        # These labels will automatically swap text and color exactly halfway through the collapse
        regime_label = always_redraw(
            lambda: Text(
                "Linear Regime" if t_tracker.get_value() < 0.5 else "Non-Linear Collapse",
                font_size=36,
                color=BLUE_E if t_tracker.get_value() < 0.5 else RED
            ).to_edge(UP, buff=0.5)
        )
        
        delta_label = always_redraw(
            lambda: MathTex(
                r"\delta \ll 1" if t_tracker.get_value() < 0.5 else r"\delta \gg 1",
                font_size=42,
                color=BLUE_E if t_tracker.get_value() < 0.5 else RED
            ).next_to(regime_label, DOWN, buff=0.2)
        )

        # Time passing label
        time_label = always_redraw(
            lambda: Text(
                f"Time: {t_tracker.get_value():.2f}",
                font_size=28
            ).to_edge(UR, buff=0.8)
        )

        # --- Animation Timeline ---
        self.play(Create(axes_group), run_time=1.5)
        self.wait(0.5)

        # Fade in the gentle, linear wave
        self.play(FadeIn(density_plot), Write(regime_label), Write(delta_label), FadeIn(time_label))
        self.wait(1.5)

        # Run the gravitational collapse
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=6,
            rate_func=smooth # Starts slow, speeds up in the middle, slows down at the end
        )
        
        # Hold on the sharply peaked halo
        self.wait(3)