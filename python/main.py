def main():
    print("Hello from msc-thesis-presentation!")

from manim import *

class CreateCircle(Scene):
	def construct(self):
		circle = Circle()  # This creates a circle
		circle.set_fill(PINK, opacity=0.5)  # Give it a color and transparency
		self.play(Create(circle))  # Show circle

class SquareToCircle(Scene):
	def construct(self):
		circle = Circle()
		circle.set_fill(PINK, opacity=0.5)
		
		square = Square()
		square.rotate(PI / 4)
		
		self.play(Create(square))
		self.play(Transform(square, circle))
		self.play(FadeOut(square))

class SquareAndCircle(Scene):
	def construct(self):
		circle = Circle()
		circle.set_fill(PINK, opacity=0.5)
		
		square = Square()
		square.set_fill(BLUE, opacity=0.5)

		square.next_to(circle, RIGHT, buff=0.5)
		self.play(Create(circle), Create(square))

class AnimatedSquareToCircle(Scene):
	def construct(self):
		circle = Circle()
		square = Square()

		self.play(Create(square))
		self.play(square.animate.rotate(PI / 4))
		self.play(Transform(square, circle))
		self.play(
			square.animate.set_fill(PINK, opacity=0.5)
		)

class DifferentRotations(Scene):
	def construct(self):
		left_square = Square(color=BLUE, fill_opacity=0.7).shift(2*LEFT)
		right_square = Square(color=PURPLE, fill_opacity=0.7).shift(2*RIGHT)
		
		self.play(
			left_square.animate.rotate(PI), Rotate(right_square, angle=PI), run_time=2,
		)
		self.wait()
class TwoTransforms(Scene):
	def transform(self):
		a = Circle()
		b = Square()
		c = Triangle()
		self.play(Transform(a,b))
		self.play(Transform(a,c))
		self.play(FadeOut(a))

	def replacement_transform(self):
		a = Circle()
		b = Square()
		c = Triangle()
		self.play(ReplacementTransform(a,b))
		self.play(ReplacementTransform(b,c))
		self.play(FadeOut(c))

	def construct(self):
		self.transform()
		self.wait(0.5)
		self.replacement_transform()
if __name__ == "__main__":
    main()
