from deepmatch.initialMatching import *

def tag(list1,num,sample,n):#list1采样列表，num当前节点编号，sample，采样数量，n原图节点
    k=0
    if num>list1[sample-1]:
        return num+n-sample
    for i in range(0,sample):
        if(list1[i]<num):
            k=k+1
    return num+n-k

def const(n,isdirected,input_graph):
    edges = {i: [] for i in range(n)}
    with open(input_graph, 'r') as fin:
        for line in fin:
            u, v = line.split()
            u, v = int(u), int(v)
            edges[u].append(v)
            if isdirected == False:
                edges[v].append(u)
    print("writing " + 'outdegreelist.txt' )
    with open('D:/netalign/algos/nrp/outdegreelist.txt', 'w') as fout:
        for i in range(n):
            for j in edges[i]:
                deginv = 1.0 / (len(edges[i]))
                fout.write(str(i) + " " + str(j) + " " + str(deginv) + "\n")
    print("writing " + 'outdegree.txt')
    with open('D:/netalign/algos/nrp/outdegree.txt', 'w') as fout:
        for i in range(n):
            fout.write(str(i) + " " + str((len(edges[i]))) + "\n")


def combin_graph(inptut_graph,ratio,sample_nodes,aline_file,out_graph,isdirected):
    G =load_file(inptut_graph)
    print("原图节点数："+str(G.number_of_nodes()))
    G1_sample = sample_graph(G, ratio)
    print("破坏后图中节点：" + str(G1_sample.number_of_nodes()))
    G1 = get_subgraph(G1_sample, sample_nodes)
    GC1 = max((G1.subgraph(c1) for c1 in nx.connected_components(G1)), key=len)
    nodes = GC1.nodes()
    nodes=list(nodes)
    nodes.sort()
    print(nodes)
    nodes_num=len(nodes)
    print("采样节点数："+str(nodes_num))

    f = open(out_graph,'w')
    with open(inptut_graph, 'r') as fin:  # 原图
        for line in fin:
            f.writelines(line)
            u, v = line.split()
            u, v = int(u), int(v)
            if u in nodes and v in nodes:
                continue
            if u not in nodes:
                u = tag(nodes, u,nodes_num,G.number_of_nodes())
            if v not in nodes:
                v = tag(nodes, v,nodes_num,G.number_of_nodes())
            f.writelines(str(u) + " " + str(v) + "\n")

    f.close()
    G_new = load_file(out_graph)
    print("新图节点总数："+str(G_new.number_of_nodes()))
    fb = open(aline_file,'w')
    for i in range(G1_sample.number_of_nodes()):
        if i in nodes:
            continue
        fb.writelines(str(i)+" "+str(tag(nodes, i,nodes_num,G.number_of_nodes()))+"\n")
    fb.close()
    const(G_new.number_of_nodes(),isdirected,out_graph)
    return (G_new.number_of_nodes())




# combin_graph("data/blocat.txt",0.80,500,"aline_true.txt","combin_blocat.txt",False)