from manim import *
import numpy as np

class ExpandingUniverseIntro(Scene):
    def construct(self):
        # --- Configuration ---
        L = 4.0  # Comoving size of the box
        N_particles = 40
        np.random.seed(42)  # Ensures the random motion is exactly the same every render
        
        # --- Physical Setup ---
        # Generate random initial comoving positions between [-L/2, L/2]
        comoving_pos = np.random.uniform(-L/2, L/2, (N_particles, 3))
        comoving_pos[:, 2] = 0  # Restrict to 2D plane
        
        # Generate random peculiar velocities
        velocities = np.random.normal(0, 0.6, (N_particles, 3))
        velocities[:, 2] = 0

        # The scale factor a(t), starting at 1.0
        scale_factor_tracker = ValueTracker(1.0)

        # --- Visual Elements ---
        # The bounding box
        box = Square(side_length=L, color=WHITE)
        
        # The particle group
        particles = VGroup()
        for i in range(N_particles):
            if i == 0:
                # The Highlighted Particle (Anchor)
                dot = Dot(color=YELLOW)
            else:
                # Background Particles
                dot = Dot(color=BLUE)
            particles.add(dot)

        self.add(box, particles)

        # --- The Physics Engine (Updater) ---
        def update_universe(mob, dt):
            a = scale_factor_tracker.get_value()
            
            # 1. Expand the box
            box.become(Square(side_length=L * a, color=WHITE))
            
            # 2. Update particle positions
            for i, dot in enumerate(particles):
                # Kinematics: update comoving position
                comoving_pos[i] += velocities[i] * dt
                
                # Periodic Boundary Conditions (wrapping)
                # Shift by L/2 to calculate modulo, then shift back to center at origin
                comoving_pos[i, 0] = ((comoving_pos[i, 0] + L/2) % L) - L/2
                comoving_pos[i, 1] = ((comoving_pos[i, 1] + L/2) % L) - L/2
                
                # Cosmology: Physical distance = scale factor * comoving distance
                physical_pos = comoving_pos[i] * a
                dot.move_to(physical_pos)

        # Attach the updater to the scene
        particles.add_updater(update_universe)

        # --- Animation Timeline ---
        # Phase 1: Static universe (a=1) to demonstrate periodicity
        self.wait(3.5)

        # Phase 2: Cosmic expansion kicks in
        self.play(
            scale_factor_tracker.animate.set_value(1.7), 
            run_time=6, 
            rate_func=linear
        )
        
        # Phase 3: Hold the final frame
        self.wait(2)
