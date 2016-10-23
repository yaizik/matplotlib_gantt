# matplotlib_gantt

Plot simple Gannt diagrams using python and matplotlib.

(Adapted from http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/, which is based on https://bitbucket.org/DBrent/phd/src/1d1c5444d2ba2ee3918e0dfd5e886eaeeee49eec/visualisation/plot_gantt.py)

Usage example:
```python
TABLE = """
start,   end, event,  color
5,6, Task 1, blue
6,8, Task 2, blue
7,9, Task 3, blue
0,3, Task 4, red
2, 6, Task 5, red
5, 6, Task 6, green
6,7, Task 7, green
4, 8, Task 8, green
4, 9, Task 9 , green
4, 10, Task 10, green
4, 11, Task 11, green
4, 12, Task 12, green
4, 13, Task 13, green
5, 18, Task 14, green
9, 17, Task 15, green
"""
df = pandas.read_csv(StringIO.StringIO(TABLE))
g = Gannt()

g.draw_gannt(df,"example1")
g.draw_gannt(df,"example2")
```
Will generate the following diagram:

![gannt diagram](example.png)
