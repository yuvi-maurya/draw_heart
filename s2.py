from turtle import *

bgcolor("black")
speed(0)
hideturtle()
for i in range(160):
    color("white")
    circle(i)
    color("blue")
    circle(i * 0.8)
    right(5)
    forward(5)
done()
    