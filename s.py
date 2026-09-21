import turtle
import colorsys

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Heart Mandala")
screen.tracer(5)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.width(1.5)


def draw_heart(size):
    start_pos = t.pos()
    t.pendown()
    t.left(50)
    t.forward(size)
    t.circle(size * 0.375, 200)
    t.right(140)
    t.circle(size * 0.375, 200)
    t.forward(size)
    t.penup()
    t.goto(start_pos)


center_y = -40
t.penup()
t.goto(0, center_y)

num_hearts = 140
size = 100

for i in range(num_hearts):
    hue = i / num_hearts
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    t.color(r, g, b)
    t.setheading(i * (360 / num_hearts))
    draw_heart(size)

num_hearts = 100
size = 75

for i in range(num_hearts):
    hue = i / num_hearts
    r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
    t.color(r, g, b)
    t.setheading(i * (360 / num_hearts))
    draw_heart(size)

num_hearts = 70
size = 50

for i in range(num_hearts):
    hue = i / num_hearts
    r, g, b = colorsys.hsv_to_rgb(hue, 0, 1)
    t.color(r, g, b)
    t.setheading(i * (360 / num_hearts))
    draw_heart(size)

screen.update()
screen.exitonclick()   # window band nahi hoga jab tak click na karo