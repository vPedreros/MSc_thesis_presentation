from manim import *
import numpy as np

Text.set_default(color=BLACK)

class LCDMCollapse(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Setup Layout ---
        box_side = 6.0
        box_center = ORIGIN

        # --- Setup Particle Box ---
        bounding_box = Square(side_length=box_side, color=BLACK).move_to(box_center)
        
        np.random.seed(42)
        num_particles = 450
        initial_positions = []
        particles = VGroup()
        
        for _ in range(num_particles):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_positions.append(np.array([x, y, 0]))
            
            p = Dot(box_center + np.array([x, y, 0]), radius=0.03, color=BLUE_E)
            particles.add(p)

        # --- The Physics Engine ---
        t_tracker = ValueTracker(0.0)

        # 1. The Particle Updater (LCDM moderate collapse)
        def update_particles(mob):
            t = t_tracker.get_value()
            current_color = interpolate_color(BLUE_E, RED, t)
            
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                
                # LCDM moderate collapse (maximum 80% contraction in the core)
                # Exponential term coefficient scaled for the 6.0 box
                collapse_factor = 1.0 - t * 0.80 * np.exp(-0.045 * r_init**2)
                
                new_x = init_x * collapse_factor
                new_y = init_y * collapse_factor
                
                p.move_to(box_center + np.array([new_x, new_y, 0]))
                p.set_color(current_color)

        particles.add_updater(update_particles)

        # --- Dynamic Labels ---
        title_label = Text("LCDM (Standard Gravity)", font_size=28).to_edge(UP, buff=0.4)
        
        time_label = always_redraw(
            lambda: Text(
                f"Tiempo: {t_tracker.get_value():.2f}",
                font_size=24
            ).to_edge(UR, buff=0.5)
        )

        # --- Animation Timeline ---
        self.play(Create(bounding_box), Write(title_label), run_time=1.5)
        self.wait(0.5)

        self.play(FadeIn(particles), FadeIn(time_label))
        self.wait(1.5)

        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=6,
            rate_func=smooth
        )
        
        self.wait(3)


class FRCollapse(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Setup Layout ---
        box_side = 6.0
        box_center = ORIGIN

        # --- Setup Particle Box ---
        bounding_box = Square(side_length=box_side, color=BLACK).move_to(box_center)
        
        np.random.seed(42)
        num_particles = 450
        initial_positions = []
        particles = VGroup()
        
        for _ in range(num_particles):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_positions.append(np.array([x, y, 0]))
            
            p = Dot(box_center + np.array([x, y, 0]), radius=0.03, color=BLUE_E)
            particles.add(p)

        # --- The Physics Engine ---
        t_tracker = ValueTracker(0.0)

        # 1. The Particle Updater (f(R) accelerated, denser collapse)
        def update_particles(mob):
            t = t_tracker.get_value()
            current_color = interpolate_color(BLUE_E, RED, t)
            
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                
                # f(R) faster, more concentrated collapse (maximum 92% contraction in the core, collapses faster in time)
                # Exponential term coefficient scaled for the 6.0 box
                collapse_factor = 1.0 - (t**1.2) * 0.92 * np.exp(-0.05 * r_init**2)
                
                new_x = init_x * collapse_factor
                new_y = init_y * collapse_factor
                
                p.move_to(box_center + np.array([new_x, new_y, 0]))
                p.set_color(current_color)

        particles.add_updater(update_particles)

        # --- Dynamic Labels ---
        title_label = Text("f(R) Gravity (Modified)", font_size=28).to_edge(UP, buff=0.4)
        
        time_label = always_redraw(
            lambda: Text(
                f"Tiempo: {t_tracker.get_value():.2f}",
                font_size=24
            ).to_edge(UR, buff=0.5)
        )

        # --- Animation Timeline ---
        self.play(Create(bounding_box), Write(title_label), run_time=1.5)
        self.wait(0.5)

        self.play(FadeIn(particles), FadeIn(time_label))
        self.wait(1.5)

        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=6,
            rate_func=smooth
        )
        
        self.wait(3)


class LCDMvsFRComparison(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- Setup Titles and Headers ---
        comparison_title = Text("Comparación en la formación de estructuras", font_size=28).to_edge(UP, buff=0.2)
        t_tracker = ValueTracker(0.0)
        time_label = always_redraw(
            lambda: Text(f"Tiempo: {t_tracker.get_value():.2f}", font_size=24).next_to(comparison_title, DOWN, buff=0.1)
        )

        # --- Setup Layout Coordinates (Bigger boxes, centered vertically) ---
        box_side = 5.2
        lcdm_box_center = LEFT * 3.5 + DOWN * 0.2
        fr_box_center = RIGHT * 3.5 + DOWN * 0.2

        # --- Setup Left Side: LCDM Visual Mobjects ---
        lcdm_box = Square(side_length=box_side, color=BLACK).move_to(lcdm_box_center)
        lcdm_box_label = Text("Relatividad General", font_size=22).next_to(lcdm_box, UP, buff=0.3)

        # --- Setup Right Side: f(R) Visual Mobjects ---
        fr_box = Square(side_length=box_side, color=BLACK).move_to(fr_box_center)
        fr_box_label = Text("Gravedad Modificada", font_size=22).next_to(fr_box, UP, buff=0.3)

        # --- Generate Particles (Same initial positions for scientific comparison) ---
        np.random.seed(42)
        num_particles = 350
        initial_positions = []
        
        lcdm_particles = VGroup()
        fr_particles = VGroup()

        for _ in range(num_particles):
            x = np.random.uniform(-box_side/2, box_side/2)
            y = np.random.uniform(-box_side/2, box_side/2)
            initial_positions.append(np.array([x, y, 0]))
            
            # Start them blue
            p_lcdm = Dot(lcdm_box_center + np.array([x, y, 0]), radius=0.03, color=BLUE_E)
            p_fr = Dot(fr_box_center + np.array([x, y, 0]), radius=0.03, color=BLUE_E)
            
            lcdm_particles.add(p_lcdm)
            fr_particles.add(p_fr)

        # --- The Physics Engines ---
        # 1. LCDM Particle Updater
        def update_lcdm_particles(mob):
            t = t_tracker.get_value()
            current_color = interpolate_color(BLUE_E, RED, t)
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                # Exponential term scaled for the 5.2 box
                collapse_factor = 1.0 - t * 0.80 * np.exp(-0.025 * r_init**2)
                mob[i].move_to(lcdm_box_center + np.array([init_x * collapse_factor, init_y * collapse_factor, 0]))
                mob[i].set_color(current_color)

        # 2. f(R) Particle Updater (Stronger collapse factor, collapses faster)
        def update_fr_particles(mob):
            t = t_tracker.get_value()
            current_color = interpolate_color(BLUE_E, RED, t)
            for i, p in enumerate(mob):
                init_x, init_y, _ = initial_positions[i]
                r_init = np.sqrt(init_x**2 + init_y**2)
                # Exponential term scaled for the 5.2 box
                collapse_factor = 1.0 - (t**1.2) * 0.92 * np.exp(-0.03 * r_init**2)
                mob[i].move_to(fr_box_center + np.array([init_x * collapse_factor, init_y * collapse_factor, 0]))
                mob[i].set_color(current_color)

        lcdm_particles.add_updater(update_lcdm_particles)
        fr_particles.add_updater(update_fr_particles)

        # --- Animation Timeline ---
        self.play(
            Write(comparison_title),
            Create(lcdm_box), Create(lcdm_box_label),
            Create(fr_box), Create(fr_box_label),
            run_time=2.0
        )
        self.wait(0.5)

        self.play(
            FadeIn(lcdm_particles),
            FadeIn(fr_particles),
            FadeIn(time_label)
        )
        self.wait(3.5)

        # Run the simultaneous gravitational collapse
        # Watch how f(R) collapses faster and forms a denser structure earlier!
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(3.5)
