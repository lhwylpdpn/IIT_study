import pydot
from IPython.display import Image



dot_string=""" graph my_graph {
a [label="a"];
b [label="b"];
c [label="c"];
a--b--c[color=blue];
}"""
pydot_graph = pydot.graph_from_dot_data(dot_string)[0]
#print(pydot_graph)
Image(pydot_graph.create_png())