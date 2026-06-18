from manim import *

# Ensure physics package compatibility to match your thesis
my_template = TexTemplate()
my_template.add_to_preamble(r"\usepackage{physics}")

# Set Keynote-friendly presentation colors
Text.set_default(color=BLACK)
Tex.set_default(color=BLACK, tex_template=my_template)
MathTex.set_default(color=BLACK, tex_template=my_template)

class ReducedHorndeski(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # --- 1. The Main Full Action ---
        action_full = MathTex(
            r"S[g_{\mu\nu},\phi] = \int \mathrm{d}^4 x\sqrt{-g}\left[M^2_{\mathrm{Pl}}\sum_{i=2}^5\mathcal{L}_i(g_{\mu\nu},\phi) + \mathcal{L}_{\mathrm{m}}(g_{\mu\nu},\psi_{\rm{m}})\right]"
        ).scale(0.8).to_edge(UP, buff=0.8)

        # --- 2. The Lagrangians ---
        l2 = MathTex(r"\mathcal{L}_2 = G_2(\phi, X) = K(\phi, X)")
        l3 = MathTex(r"\mathcal{L}_3 = -G_3(\phi, X)\Box\phi")
        
        # Split L4 into parts so we can safely highlight and cross out the second half later
        l4 = MathTex(
            r"\mathcal{L}_4 = ",
            r"G_4(\phi, X)",
            r" R ",
            r"+ G_{4X}(\phi,X)\left[(\Box\phi)^2-\nabla_\mu\nabla_\nu\phi\nabla^\mu\nabla^\nu\phi\right]"
        )

        l5_1 = MathTex(r"\mathcal{L}_5 = G_5(\phi,X)G_{\mu\nu}\nabla^\mu\nabla^\nu\phi")
        l5_2 = MathTex(
            r"\quad -\frac{1}{6}G_{5X}(\phi,X) \left[(\Box\phi)^3+2\nabla_\mu\nabla^\nu\phi\nabla_\nu\nabla^\alpha\phi\nabla_\alpha\nabla^\mu\phi - 3\nabla_\mu\nabla_\nu\phi\nabla^\mu\nabla^\nu\phi\Box\phi\right]"
        )

        # Group and position the Lagrangians (using standard 0.65 scale to prevent overflows)
        lagrangians = VGroup(l2, l3, l4, l5_1, l5_2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.65)
        l5_2.shift(RIGHT * 1.0) # Indent the second line of L5 slightly for formatting
        lagrangians.next_to(action_full, DOWN, buff=0.8)

        # --- ANIMATION SEQUENCE ---
        
        # 1. Introduce the full mathematics
        self.play(Write(action_full))
        self.wait(0.5)
        self.play(FadeIn(lagrangians, lag_ratio=0.1), run_time=2)
        self.wait(1.5)

        # 2. Highlight the terms that are going to be removed (change color to red)
        self.play(
            l4[3].animate.set_color(RED_E),
            l5_1.animate.set_color(RED_E),
            l5_2.animate.set_color(RED_E),
            run_time=1.5
        )
        self.wait(1)

        # 3. Cross out the highlighted terms
        cross_l4 = Cross(l4[3], stroke_color=RED_E, stroke_width=4)
        cross_l5_1 = Cross(l5_1, stroke_color=RED_E, stroke_width=4)
        cross_l5_2 = Cross(l5_2, stroke_color=RED_E, stroke_width=4)

        self.play(
            Create(cross_l4),
            Create(cross_l5_1),
            Create(cross_l5_2),
            run_time=1.5
        )
        self.wait(1.5)

        # 4. Fade out the crossed-out terms
        self.play(
            FadeOut(l4[3], cross_l4),
            FadeOut(l5_1, cross_l5_1),
            FadeOut(l5_2, cross_l5_2),
            run_time=1.5
        )
        self.wait(0.5)

        # 5. Transform the remaining terms and center them
        # Define the target reduced action
        action_reduced = MathTex(
            r"S[g_{\mu\nu},\phi] = \int \mathrm{d}^4 x\sqrt{-g}\left[M^2_{\mathrm{Pl}}\sum_{i=2}^{4}\mathcal{L}_i(g_{\mu\nu},\phi) + \mathcal{L}_{\mathrm{m}}(g_{\mu\nu},\psi_{\rm{m}})\right]"
        ).scale(0.8).to_edge(UP, buff=0.8)

        # Define the target reduced L4 (G_4X = 0, so G_4 depends only on \phi)
        l4_reduced = MathTex(r"\mathcal{L}_4 = ", r"G_4(\phi)", r" R").scale(0.65)
        l4_reduced[1].set_color(BLUE_E) # Highlight the surviving modification

        # Create a target configuration for the surviving lagrangians
        target_group = VGroup(l2.copy(), l3.copy(), l4_reduced).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        target_group.next_to(action_reduced, DOWN, buff=0.8)

        # Animate the transition to the final layout
        self.play(
            Transform(action_full, action_reduced),
            Transform(VGroup(l4[0], l4[1], l4[2]), target_group[2]),
            l2.animate.move_to(target_group[0]),
            l3.animate.move_to(target_group[1]),
            run_time=2
        )
        
        self.wait(3)