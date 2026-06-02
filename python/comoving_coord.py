from manim import *
import numpy as np

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

def get_spiral_galaxy(color, radius=0.3):
    max_theta = 2.5 * PI  
    b = radius / max_theta
    
    arm1 = ParametricFunction(
        lambda t: np.array([b * t * np.cos(t), b * t * np.sin(t), 0]),
        t_range=[0, max_theta], color=color, stroke_width=4.5
    )
    arm2 = ParametricFunction(
        lambda t: np.array([-b * t * np.cos(t), -b * t * np.sin(t), 0]),
        t_range=[0, max_theta], color=color, stroke_width=4.5
    )
    core = Dot(color=color, radius=radius * 0.35)
    
    return VGroup(core, arm1, arm2)


class GalacticRecessionComovingCoord(Scene):
    def construct(self):
        # --- Scene Setup ---
        self.camera.background_color = WHITE

        # --- Configuration ---
        grid_dim = 6
        grid_scale = 1.0
        a_initial = 1.0
        a_final = 2.0
        expand_time = 8

        a_tracker = ValueTracker(a_initial)

        # --- Visual Elements: Static Background & Galaxies ---
        spacetime_grid = NumberPlane(
            x_range=[-grid_dim, grid_dim, grid_scale],
            y_range=[-grid_dim, grid_dim, grid_scale],
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.5},
            axis_config={"stroke_color": BLACK}
        )

        comoving_pos_a = RIGHT * 2 + UP * 1
        comoving_pos_b = LEFT * 3 + DOWN * 1.5

        galaxy_icon_a = get_spiral_galaxy(color=RED, radius=0.3).move_to(comoving_pos_a)
        galaxy_icon_b = get_spiral_galaxy(color=BLUE_E, radius=0.3).move_to(comoving_pos_b)

        galaxy_a = VGroup(
            galaxy_icon_a,
            Text("Galaxia A", font_size=24, color=RED).next_to(galaxy_icon_a.get_center(), UP, buff=0.5)
        )

        galaxy_b = VGroup(
            galaxy_icon_b,
            Text("Galaxia B", font_size=24, color=BLUE_E).next_to(galaxy_icon_b.get_center(), UP, buff=0.5)
        )

        # --- Visual Elements: Distance Arrow & Math ---
        # Because the galaxies don't move, this arrow is completely static now!
        distance_arrow = DoubleArrow(
            start=galaxy_icon_b.get_center(),
            end=galaxy_icon_a.get_center(),
            color=BLACK,
            buff=0.7, 
            stroke_width=3
        )

        distance_label = MathTex(r"\chi = \frac{d(t)}{a(t)}", font_size=36).move_to(
            distance_arrow.get_center() + DOWN * 0.4 + RIGHT * 0.8
        )

        metric_label = MathTex(r"\dd{s}^2 = a^2(t)\qty[-\dd{t}^2 + \dd{\vb x}^2]").to_edge(DOWN, buff=0.5)
        
        # This is the ONLY object that needs an updater in comoving coordinates
        a_label = MathTex(f"a(t) = {a_initial/2:.2f}").to_edge(UP, buff=0.5)
        a_label.add_updater(
            lambda mob: mob.become(
                MathTex(f"a(t) = {a_tracker.get_value()/2:.2f}").to_edge(UP, buff=0.5)
            )
        )

        # --- Animation Timeline ---
        self.play(Create(spacetime_grid), run_time=2)
        self.wait(1)

        self.play(FadeIn(galaxy_a), FadeIn(galaxy_b))
        self.wait(1)

        self.play(FadeIn(distance_arrow), Write(distance_label))
        self.wait(1.5)

        self.play(Write(metric_label), Write(a_label))
        self.wait(1)

        # Phase 5: The "Expansion"
        # Since we are in the comoving frame, the only thing that visibly 
        # changes during this time is the a(t) counter ticking upwards!
        self.play(
            a_tracker.animate.set_value(a_final), 
            run_time=expand_time, 
            rate_func=linear
        )
        
        self.wait(3)