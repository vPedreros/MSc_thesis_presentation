from manim import *
import numpy as np

my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

# Change default text colors to black for visibility on white
Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)


def get_spiral_galaxy(color, radius=0.3):
    # Determine how tightly the arms wind. 
    # This scales the spiral so its maximum extent matches the requested radius.
    max_theta = 2.5 * PI  # 1.25 full turns
    b = radius / max_theta
    
    # Arm 1: Standard parametric spiral
    arm1 = ParametricFunction(
        lambda t: np.array([b * t * np.cos(t), b * t * np.sin(t), 0]),
        t_range=[0, max_theta],
        color=color,
        stroke_width=4.5
    )
    
    # Arm 2: Rotated 180 degrees (adding PI to the angle, or simply negating x and y)
    arm2 = ParametricFunction(
        lambda t: np.array([-b * t * np.cos(t), -b * t * np.sin(t), 0]),
        t_range=[0, max_theta],
        color=color,
        stroke_width=4.5
    )
    
    # The galactic core
    core = Dot(color=color, radius=radius * 0.35)
    
    # Group them together so they behave like a single object
    return VGroup(core, arm1, arm2)


class GalacticRecession(Scene):
    def construct(self):
        # --- Configuration ---
        grid_dim = 6          # Number of comoving grid cells per dimension
        grid_scale = 1.0       # Size of each initial grid cell
        a_initial = 1.0       # Initial scale factor
        a_final = 2.0         # Final scale factor (expansion factor)
        expand_time = 8       # Seconds for the expansion

        # ValueTracker to manage the scale factor a(t)
        a_tracker = ValueTracker(a_initial)

        # --- Visual Elements: Spacetime Grid ---
        # Create a basic grid structure using NumberPlane or standard VGroups
        spacetime_grid = NumberPlane(
            x_range=[-grid_dim, grid_dim, grid_scale],
            y_range=[-grid_dim, grid_dim, grid_scale],
            background_line_style={
                "stroke_color": GRAY,
                "stroke_opacity": 0.5
            },
            axis_config={"stroke_color": BLACK}
        )

        # A "VGroup" to bundle the grid and everything anchored to it
        cosmic_contents = VGroup(spacetime_grid)

        # --- Visual Elements: The Galaxies ---
        # We define their constant COMOVING positions.
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

        # Anchor galaxies to the spacetime grid
        # cosmic_contents.add(galaxy_a, galaxy_b)

        # --- The Physics Engine (Updater) ---
        # Attach a custom attribute to track the accumulated scale factor
        cosmic_contents.current_scale = a_initial

        # This function runs every single frame.
        def update_cosmic_contents(mob, dt):
            target_scale = a_tracker.get_value()
            
            # Scale relative to the last frame's scale, then update the tracker
            mob.scale(target_scale / mob.current_scale)
            mob.current_scale = target_scale

        def update_galaxy_a(mob):
            target_pos = comoving_pos_a * a_tracker.get_value()
            # mob[0] is the spiral icon, mob[1] is the text
            mob[0].move_to(target_pos)
            mob[1].next_to(mob[0].get_center(), UP, buff=0.5)

        def update_galaxy_b(mob):
            target_pos = comoving_pos_b * a_tracker.get_value()
            mob[0].move_to(target_pos)
            mob[1].next_to(mob[0].get_center(), DOWN, buff=0.5)

        # The internal handling of scaling in Manim can be nuanced.
        # A more robust approach for an updater scenario is
        # using 'become' or updating positions explicitly. 
        # But for this simple scenario, scaling the whole VGroup works.
        cosmic_contents.add_updater(update_cosmic_contents)

        # We also need a dynamic label for the scale factor
        a_label = MathTex(f"a(t) = {a_initial/2:.2f}").to_edge(UP, buff=0.5)
        metric_label = MathTex(r"\dd{s}^2 = a^2(t)\qty[-\dd{t}^2 + \dd{\vb x}^2]").to_edge(DOWN, buff=0.5)
        a_label.add_updater(
            lambda mob: mob.become(
                MathTex(f"a(t) = {a_tracker.get_value()/2:.2f}").to_edge(UP, buff=0.5)
            )
        )

        # --- Visual Elements: Distance Arrow & Label ---
        # We use always_redraw so they track the galaxies dynamically 
        # without being stretched by the VGroup scaling.
        distance_arrow = always_redraw(
            lambda: DoubleArrow(
                start=galaxy_icon_b.get_center(),
                end=galaxy_icon_a.get_center(),
                color=BLACK,
                buff=0.7, # Padding so it doesn't overlap the spiral arms
                stroke_width=3
            )
        )

        distance_label = always_redraw(
            lambda: MathTex(r"d(t) = a(t) \chi", font_size=36)
            # Place it at the center of the arrow, then shift it up and left
            .move_to(distance_arrow.get_center() + DOWN * 0.4 + RIGHT * 0.8)
        )
        # --- Animation Timeline ---
        
        # Phase 1: Showcase the Spacetime Grid
        # We draw the grid lines dynamically so the audience understands the geometry.
        self.play(Create(spacetime_grid), run_time=2)
        self.wait(1)

        # Phase 2: Add the Galaxies
        # We fade them in at their comoving coordinates.
        self.play(FadeIn(galaxy_a), FadeIn(galaxy_b))
        self.wait(1)

        # Phase 3: Measure the Distance
        # We fade in the always_redraw arrow and label before the expansion starts.
        self.play(FadeIn(distance_arrow), Write(distance_label))
        self.wait(1.5)

        # Phase 4: Introduce the Math
        # Right before the universe expands, we bring in the governing equations.
        self.play(Write(metric_label), Write(a_label))
        self.wait(1)

        # Phase 5: The Expansion
        # CRITICAL: We attach the updater to the bundle right here, at the exact 
        # moment it needs to start scaling, preventing any weird drawing glitches.
        self.add(cosmic_contents)
        cosmic_contents.add_updater(update_cosmic_contents)

        # Attach the new kinematics updaters to the galaxies
        galaxy_a.add_updater(update_galaxy_a)
        galaxy_b.add_updater(update_galaxy_b)

        # The tracker changes value, causing the updater to stretch the universe.
        self.play(
            a_tracker.animate.set_value(a_final), 
            run_time=expand_time, 
            rate_func=linear
        )
        
        # Phase 6: Hold the final expanded state
        self.wait(3)
