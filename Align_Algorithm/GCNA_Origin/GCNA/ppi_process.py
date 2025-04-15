# 读取文件
sampling = 0.9
with open('./'+str(sampling)+'/ppi_t_edge.txt', "r") as f:
    lines = f.readlines()

# 存储节点之间的边
edges = set()
for line in lines:
    node1, node2 = map(int, line.strip().split())
    edges.add((node1, node2))

# 查找未出现的节点并添加自环边
for node in range(1767):
    if not any(node in edge for edge in edges):
        edges.add((node, node))

# 将边排序并写回文件
with open('./'+str(sampling)+'/ppi_t_edge.txt', "w") as f:
    for node1, node2 in sorted(edges):
        f.write(f"{node1} {node2}\n")

print("add edge done"+"    "+str(sampling))
