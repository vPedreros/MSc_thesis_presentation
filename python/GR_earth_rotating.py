from manim import *
import numpy as np

# Apply our global defaults for the white background style
Text.set_default(color=BLACK)
Tex.set_default(color=BLACK)
MathTex.set_default(color=BLACK)

class SpacetimeCurvature(ThreeDScene):
    def construct(self):
        # --- Scene Setup ---
        self.camera.background_color = WHITE
        
        # Use MathTex for formulas, and fix it to the 2D frame overlay so it doesn't get distorted in 3D space
        efe = MathTex(
            r"G_{\mu\nu}",
            r"=\frac{8\pi G}{c^4}",
            r"T_{\mu\nu}",
            font_size=75
            ).to_edge(UP)
        efe[0].set_color(BLUE_E)
        efe[2].set_color(RED_E)

        self.add_fixed_in_frame_mobjects(efe)
        self.remove(efe)

        # Position the camera for a good 3D isometric view
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES)

        # --- The Spacetime Grid ---
        # We use a Gaussian function to create a smooth, visually pleasing well
        def gravity_well_func(u, v):
            r_squared = u**2 + v**2
            # The depth of the well is determined by the coefficient (here, -2.5)
            z = -2.5 * np.exp(-0.4 * r_squared)
            return np.array([u, v, z])


        spacetime_surface = Surface(
            gravity_well_func,
            u_range=[-5, 5],
            v_range=[-5, 5],
            resolution=(30, 30),
            fill_opacity=0.1,
            checkerboard_colors=[LIGHT_GRAY, WHITE],
            stroke_width=1,
            stroke_color=BLUE_E
        )

        # --- Celestial Bodies ---
        # The Sun sits at the bottom of the gravity well
        sun = Sphere(
            center=np.array([0, 0, -2.5]), 
            radius=0.6, 
            checkerboard_colors=[RED_E, RED_E]
        )

        # The Earth will orbit at a radius of 2 units (closer to the Sun)
        orbit_radius = 2.2
        # Calculate the depth of the well at the Earth's orbit so it sits on the grid
        earth_z = -2.5 * np.exp(-0.4 * (orbit_radius**2))
        
        earth = Sphere(
            center=np.array([orbit_radius, 0, earth_z]), 
            radius=0.2, 
            checkerboard_colors=[RED_E, RED_E]
        )

        # --- The Physics Engine (Updater) ---
        # Animate the Earth moving along the curved surface
        theta_tracker = ValueTracker(0)

        def update_earth(mob):
            theta = theta_tracker.get_value()
            x = orbit_radius * np.cos(theta)
            y = orbit_radius * np.sin(theta)
            z = -2.5 * np.exp(-0.4 * (x**2 + y**2))
            mob.move_to(np.array([x, y, z]))

        earth.add_updater(update_earth)

        # --- Animation Timeline ---
        # 1. Fade in the flat components
        self.play(Create(spacetime_surface), FadeIn(sun), FadeIn(earth))
        self.wait(1)

        # 2. Slowly rotate the camera during the orbit for cinematic effect (Merged animations)
        self.move_camera(
            theta=-90 * DEGREES, 
            added_anims=[theta_tracker.animate.set_value(2 * PI)],
            run_time=6,
            rate_func=linear
        )
        
        self.play(Write(efe[0]))
        self.wait(1)
        
        self.play(Write(efe[2]))
        self.wait(1)
        
        self.play(Write(efe[1]))
        self.wait(1)

        self.wait(5)
