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


class HubblesLawRedshift(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Configuration ---
        a_initial = 1.0
        a_final = 2.0
        expand_time = 8

        a_tracker = ValueTracker(a_initial)

        # --- Visual Elements: Galaxies ---
        comoving_pos_a = LEFT * 5
        comoving_pos_b = ORIGIN 

        galaxy_icon_a = get_spiral_galaxy(color=ORANGE, radius=0.3).move_to(comoving_pos_a)
        galaxy_icon_b = get_spiral_galaxy(color=BLUE_E, radius=0.3).move_to(comoving_pos_b)

        galaxy_a = VGroup(
            galaxy_icon_a,
            Text("Observador", font_size=24).next_to(galaxy_icon_a, UP, buff=0.5)
        )

        galaxy_b = VGroup(
            galaxy_icon_b,
            Text("Galaxia", font_size=24).next_to(galaxy_icon_b, UP, buff=0.5)
        )

        # --- Visual Elements: The Light Wave ---
        def get_redshifted_wave():
            current_a = a_tracker.get_value()
            
            # Get the exact X-coordinates of both galaxies on the screen
            x_observer = galaxy_icon_a.get_center()[0]
            x_galaxy = galaxy_icon_b.get_center()[0]
            
            # Apply the buffer directly to their real coordinates
            start_x = x_observer + 0.4
            end_x = x_galaxy - 0.4
            active_length = end_x - start_x
            
            cycles = 4
            
            alpha = (current_a - a_initial) / (a_final - a_initial)
            current_color = interpolate_color(BLUE_E, RED, alpha)
            
            wave = ParametricFunction(
                lambda t: np.array([
                    t, 
                    0.25 * np.sin(cycles * 2 * PI * (t - start_x) / active_length), 
                    0
                ]),
                t_range=[start_x, end_x],
                color=current_color,
                stroke_width=4
            )
            return wave

        light_wave = always_redraw(get_redshifted_wave)

        # --- Visual Elements: The Math ---
        # Dynamically updates the redshift equation 1 + z = a(t)

        redshift_eq = always_redraw(
            lambda: MathTex(
                r"\frac{\lambda_{\rm obs}}{\lambda_{\rm em}} = (1 +z) = ", 
                f"{a_tracker.get_value():.2f}", 
                font_size=42
            ).to_edge(UP)
        )
        
        # A simple lambda label that tracks the middle of the wave
        lambda_label = always_redraw(
            lambda: MathTex(r"\lambda(t)", font_size=36)
            .next_to(light_wave, DOWN, buff=0.2)
        )

        # --- Visual Elements: Photon ---
        p_tracker = ValueTracker(0.0)
        photon_core = Dot(color=BLUE_E, radius=0.08)
        photon_glow = Dot(color=BLUE_E, radius=0.15, fill_opacity=0.3)
        photon = VGroup(photon_glow, photon_core)

        def update_photon(mob):
            alpha = p_tracker.get_value()
            
            x_observer = galaxy_icon_a.get_center()[0]
            x_galaxy = galaxy_icon_b.get_center()[0]
            
            start_x = x_observer + 0.4
            end_x = x_galaxy - 0.4
            active_length = end_x - start_x
            
            current_x = end_x - alpha * active_length
            cycles = 4
            current_y = 0.25 * np.sin(cycles * 2 * PI * (current_x - start_x) / active_length)
            
            mob.move_to(np.array([current_x, current_y, 0]))

            # Match the wave's color transition (from BLUE_E to RED)
            current_a = a_tracker.get_value()
            alpha_color = (current_a - a_initial) / (a_final - a_initial)
            photon_color = interpolate_color(BLUE_E, RED, alpha_color)
            mob.set_color(photon_color)

        photon.add_updater(update_photon)

        # --- The Redshift Physics Engine ---
        def update_galaxy_b(mob):
            current_a = a_tracker.get_value()
            
            # 1. Update physical position relative to the Observer
            # Physical Distance = Comoving Distance vector * a(t)
            comoving_distance_vector = comoving_pos_b - comoving_pos_a
            physical_distance_vector = comoving_distance_vector * current_a
            
            # New Position = Observer Position + Physical Distance
            target_pos = comoving_pos_a + physical_distance_vector
            
            mob[0].move_to(target_pos)
            mob[1].next_to(mob[0].get_center(), UP, buff=0.5)

            # 2. Update galaxy color to match the wave
            alpha = (current_a - a_initial) / (a_final - a_initial)
            redshifted_color = interpolate_color(BLUE_E, RED, alpha)
            mob[0].set_color(redshifted_color)

        # --- Animation Timeline ---
        self.play(FadeIn(galaxy_a), FadeIn(galaxy_b))
        self.wait(1)

        self.play(Create(light_wave), Write(lambda_label))
        self.play(Write(redshift_eq))
        
        self.wait(1)

        # Attach the kinematics updater right before expansion begins
        galaxy_b.add_updater(update_galaxy_b)

        # Fade in the photon at the start of expansion
        self.play(FadeIn(photon))

        self.play(
            a_tracker.animate.set_value(a_final), 
            p_tracker.animate.set_value(1.0),
            run_time=expand_time, 
            rate_func=linear
        )
        
        # Fade out the photon once it reaches the observer
        self.play(FadeOut(photon))
        
        self.wait(3)