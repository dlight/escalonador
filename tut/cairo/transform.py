#! /usr/bin/env python
import framework
from math import pi

class Transform(framework.Screen):
    def draw(self, cr, width, height):
        cr.set_source_rgb(0.5, 0.5, 0.5)
        cr.rectangle(0, 0, width, height)
        cr.fill()

        # draw a rectangle
        cr.set_source_rgb(1.0, 1.0, 1.0)
        cr.rectangle(10, 10, width - 20, height - 20)
        cr.fill()

        # set up a transform so that (0,0) to (1,1)
        # maps to (20, 20) to (width - 40, height - 40)
        cr.translate(20, 20)
        cr.scale((width - 40) / 1.0, (height - 40) / 1.0)

        # draw lines
        cr.set_line_width(0.01)
        cr.set_source_rgb(0.0, 0.0, 0.8)
        cr.move_to(1 / 3.0, 1 / 3.0)
        cr.rel_line_to(0, 1 / 6.0)
        cr.move_to(2 / 3.0, 1 / 3.0)
        cr.rel_line_to(0, 1 / 6.0)
        cr.stroke()

        # and a circle
        cr.set_source_rgb(1.0, 0.0, 0.0)
        radius = 1
        cr.arc(0.5, 0.5, 0.5, 0, 2 * pi)
        cr.stroke()
        cr.arc(0.5, 0.5, 0.33, pi / 3, 2 * pi / 3)
        cr.stroke()

framework.run(Transform)
