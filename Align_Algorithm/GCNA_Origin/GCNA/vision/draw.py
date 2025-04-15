# 作者：York
# 时间：2022/4/14 17:05
import matplotlib.pyplot as plt
import networkx as nx
#G = graph
plt.figure(figsize=(20,20))
nx.draw(G, with_labels= True,font_color='#000000',node_color='r',font_size=8,node_size=20)
plt.show()