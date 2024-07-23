from manim import *


class Pith(Scene):
    def construct(self):
        sq = Square(side_length=5, stroke_color=GREEN, fill_color=BLUE, fill_opacity=0.75)
        self.play(Create(sq), run_time=3)
        self.wait()


class Testing(Scene):
    def construct(self):
        name = Tex("Amedee").to_edge(UL, buff=0.5)
        sq = Square(side_length=0.5, fill_color=GREEN, fill_opacity=0.75).shift(LEFT * 3)
        tri = Triangle().scale(0.6).to_edge(DR)

        self.play(Write(name))
        self.play(DrawBorderThenFill(sq), run_time=2)
        self.play(Create(tri))
        self.wait()
        self.play(name.animate.to_edge(UR), run_time=2)
        self.play(sq.animate.scale(2), tri.animate.to_edge(DL), run_time=3)
        self.wait()


class Getters(Scene):
    def construct(self):
        rect = Rectangle(fill_color=WHITE, height=3, width=2.5).to_edge(UL)
        circ = Circle().to_edge(DOWN)
        arrow = always_redraw(lambda: Line(start=rect.get_bottom(), end=circ.get_top(), buff=0.5).add_tip())
        self.play(Create(VGroup(rect, circ, arrow)))
        self.wait()
        self.play(rect.animate.to_edge(UR), circ.animate.scale(0.5), run_time=2)
        self.wait()


class Updaters(Scene):
    def construct(self):
        num = MathTex("ln(2)")
        box = always_redraw(lambda: SurroundingRectangle(
            num, color=BLUE, fill_color=RED, fill_opacity=0.4, buff=1
        ))
        name = always_redraw(lambda: Tex("Amedee").next_to(box, DOWN, buff=0.95))
        self.play(Create(VGroup(num, box, name)))
        self.wait()
        self.play(num.animate.shift(RIGHT * 3), run_time=2)
        self.wait()


class ValueTrackers(Scene):
    def construct(self):
        k = ValueTracker(0)
        num = always_redraw(lambda: DecimalNumber().set_value(k.get_value()))

        self.play(FadeIn(num))
        self.wait()
        self.play(k.animate.set_value(3), run_time=5, rate_func=smooth)


class Graphing(Scene):
    def construct(self):
        plane = (
            NumberPlane(x_range=[-2, 2, 0.5], x_length=8, y_range=[0, 16, 3], y_length=6)
            .to_edge(DOWN)
            .add_coordinates()
        )
        k = ValueTracker(1)
        num = DecimalNumber(1, num_decimal_places=2)
        newlabels = MathTex("f(X) = ", 1, "x^2")
        num.add_updater(lambda v: v.set_value(k.get_value()))
        num.move_to(newlabels[1])
        newlabels.to_edge(UP)

        labels = plane.get_axis_labels(x_label="x", y_label=f"f(x)")

        parab = plane.plot(lambda x: x ** 2, x_range=[-2, 2], color=GREEN)
        parab2 = plane.plot(lambda x: 3 * x ** 2, x_range=[-2, 2], color=GREEN)

        func_label = (
            MathTex("f(x) = {x}^{2}")
            .scale(0.6)
            .next_to(parab, RIGHT, buff=0.5)
            .set_color(GREEN)
        )

        self.play(DrawBorderThenFill(plane))
        self.wait()
        self.play(FadeIn(VGroup(labels, parab, func_label, newlabels)))
        self.wait()
        self.play(Transform(parab, parab2), k.animate.set_value(3), run_time=5, rate_func=smooth)
        self.wait()



class EquationAnimation(Scene):
    def construct(self):
        # 创建一个文本对象，用于显示方程式
        equation = MathTex("a =", "1")
        equation.to_edge(UP)

        # 创建一个ValueTracker来追踪数字的值
        value_tracker = ValueTracker(1)

        # 创建一个DecimalNumber对象来显示数字，并与ValueTracker关联
        number = DecimalNumber(1, num_decimal_places=2)
        number.add_updater(lambda v: v.set_value(value_tracker.get_value()))
        number.move_to(equation[1])

        # 添加文本对象和数字对象到场景中
        self.play(Create(equation))
        self.play(Write(number))

        # 使用ValueTracker逐渐增加数字的值
        self.play(value_tracker.animate.set_value(5), run_time=4)
