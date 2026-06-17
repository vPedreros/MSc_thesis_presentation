from manim import *
import numpy as np

# Use the physics template to ensure compatibility with your other slides
my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

class NumericalMotivation(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Dynamic Text Overlays ---
        title = Text("The Mathematical Wall", font_size=48, weight=BOLD).to_edge(UP, buff=0.5)
        
        # We will update these labels as the physics changes
        regime_text = Text("1. Linear Perturbation Theory", font_size=36, color=BLUE_E)
        math_status = Text("Analytical Solutions: Valid (Decoupled Modes)", font_size=28, color=GREEN_E)
        
        label_group = VGroup(regime_text, math_status).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.3)

        # --- Particle Grid Setup ---
        grid_width = 10
        grid_height = 4
        spacing = 0.4
        
        particles = VGroup()
        initial_positions = []

        # Create a uniform grid of particles
        for x in np.arange(-grid_width/2, grid_width/2 + spacing, spacing):
            for y in np.arange(-grid_height/2, grid_height/2 + spacing, spacing):
                # Add tiny random noise so it looks like a natural fluid, not a perfect lattice
                noise_x = np.random.uniform(-0.05, 0.05)
                noise_y = np.random.uniform(-0.05, 0.05)
                pos = np.array([x + noise_x, y + noise_y, 0])
                
                initial_positions.append(pos)
                particles.add(Dot(pos + DOWN*1.5, radius=0.04, color=BLUE_E))

        # --- The Physics Engine ---
        # time_tracker drives the animation forward. 
        # regime_tracker dictates which physics rules apply.
        time_tracker = ValueTracker(0.0)
        regime_tracker = ValueTracker(0.0)

        def update_fluid(mob):
            t = time_tracker.get_value()
            regime = regime_tracker.get_value()
            
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                
                # --- REGIME 0: Linear Perturbation (Gentle oscillation) ---
                if regime < 1.0:
                    # Particles sway gently in a predictable sine wave
                    dx = 0.2 * np.sin(init_x) * np.sin(2 * t)
                    dy = 0.1 * np.cos(init_x) * np.sin(2 * t)
                    p.move_to(np.array([init_x + dx, init_y + dy, 0]) + DOWN*1.5)
                    p.set_color(BLUE_E)

                # --- REGIME 1: Non-Linear Collapse (Standard Gravity) ---
                elif 1.0 <= regime < 2.0:
                    collapse_factor = (regime - 1.0) # Scales from 0 to 1
                    
                    # Particles flow towards specific nodes (x = -3, 0, 3)
                    dx = -collapse_factor * 1.5 * np.sin(np.pi * init_x / 3)
                    dy = -collapse_factor * init_y * 0.4 * np.cos(np.pi * init_x / 3)
                    
                    current_color = interpolate_color(BLUE_E, ORANGE, collapse_factor)
                    p.move_to(np.array([init_x + dx, init_y + dy, 0]) + DOWN*1.5)
                    p.set_color(current_color)

                # --- REGIME 2: Coupled Scalar Field (Horndeski Fifth Force) ---
                else:
                    fifth_force_factor = (regime - 2.0) # Scales from 0 to 1
                    
                    # Standard gravity base (from end of regime 1)
                    base_dx = -1.5 * np.sin(np.pi * init_x / 3)
                    base_dy = -init_y * 0.4 * np.cos(np.pi * init_x / 3)
                    
                    # Add intense, chaotic crushing to simulate the scalar field coupling
                    extra_dx = -fifth_force_factor * 1.2 * np.sin(np.pi * init_x / 3)
                    extra_dy = -fifth_force_factor * init_y * 0.8
                    
                    current_color = interpolate_color(ORANGE, RED_E, fifth_force_factor)
                    p.move_to(np.array([init_x + base_dx + extra_dx, init_y + base_dy + extra_dy, 0]) + DOWN*1.5)
                    p.set_color(current_color)

        particles.add_updater(update_fluid)

        # --- Animation Timeline ---
        
        # 1. Intro
        self.play(Write(title), FadeIn(label_group), FadeIn(particles))
        self.wait(1)

        # 2. Linear Regime (Play for a few seconds to show predictability)
        self.play(time_tracker.animate.set_value(4 * PI), run_time=6, rate_func=linear)
        
        # 3. Transition to Non-Linear Collapse
        new_regime_text_1 = Text("2. Highly Non-Linear Collapse", font_size=36, color=ORANGE)
        new_math_status_1 = Text("Analytical Solutions: FAILED (Modes Coupled)", font_size=28, color=RED)
        new_label_group_1 = VGroup(new_regime_text_1, new_math_status_1).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.3)
        
        self.play(
            Transform(label_group, new_label_group_1),
            regime_tracker.animate.set_value(1.0), 
            run_time=0.5
        )
        
        # Animate the gravitational collapse
        self.play(regime_tracker.animate.set_value(2.0), run_time=4, rate_func=smooth)
        self.wait(1)

        # 4. Transition to Coupled Fluids (Modified Gravity)
        new_regime_text_2 = Text("3. Coupled Scalar Field (Horndeski Gravity)", font_size=36, color=RED_E)
        new_math_status_2 = Text("Analytical Solutions: IMPOSSIBLE (Dynamically Coupled Fluids)", font_size=28, color=RED_E)
        new_label_group_2 = VGroup(new_regime_text_2, new_math_status_2).arrange(DOWN, buff=0.2).next_to(title, DOWN, buff=0.3)

        self.play(
            Transform(label_group, new_label_group_2),
            run_time=0.5
        )
        
        # Animate the extreme fifth-force collapse
        self.play(regime_tracker.animate.set_value(3.0), run_time=3, rate_func=rush_into)
        
        # Hold on the final catastrophic collapse
        self.wait(3)