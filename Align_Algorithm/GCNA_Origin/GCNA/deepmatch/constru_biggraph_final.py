from deepmatch.DeepMatching import *
from deepmatch.initialMatching import *
def tag(list1,num):#list1采样列表，num当前节点编号，sample，采样数量，n原图节点
    return list1.index(num)

#写入outdegreelist和outdegree文件
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
    with open('../../algos/nrp/outdegreelist.txt', 'w') as fout:
        for i in range(n):
            for j in edges[i]:
                deginv = 1.0 / (len(edges[i]))
                fout.write(str(i) + " " + str(j) + " " + str(deginv) + "\n")
    print("writing " + 'outdegree.txt')
    with open('../../algos/nrp/outdegree.txt', 'w') as fout:
        for i in range(n):
            fout.write(str(i) + " " + str((len(edges[i]))) + "\n")

def combin_biggraph_final(inptut_graph,ratio,sample_nodes,aline_file,out_graph,isdirected):
    #True代表无向图
    G =load_file(inptut_graph,False)
    print("原图节点数："+str(G.number_of_nodes()))
    #去除一定的边
    G1_sample = sample_graph(G, ratio)
    print("破坏后图中节点：" + str(G1_sample.number_of_nodes()))
    G2 = get_subgraph(G1_sample, sample_nodes)
    GC2 = max((G2.subgraph(c1) for c1 in nx.connected_components(G2)), key=len)
    G1 = get_subgraph(G, sample_nodes)
    GC1 = max((G1.subgraph(c1) for c1 in nx.connected_components(G1)), key=len)



    #匹配的点
    nodes_match=[]
    #不匹配的点
    nodes_no_match={}

    nodes_G2 = list(G1_sample.nodes())
    # nodes_G2.sort()
    seed_time1=time.time()
    matches_ms=bipartite_matching(GC1, GC2)
    seed_time2 = time.time()
    seed_time=seed_time2-seed_time1
    # print("seed time is %f" % seed_time)
    nodes_g2=[]
    # print("before %f" % len(nodes_G2))
    for match in matches_ms:
        nodes_G2.remove(match[1])
        nodes_g2.append(match[1])
        if match[0] == match[1]:
            nodes_match.append(match[1])
            nodes_match.sort()
        else:
            nodes_no_match[match[1]]=match[0]
    # print("after %f" % len(nodes_G2))
    print("不匹配的点")
    print(nodes_no_match)
    #图1中不匹配的点
    match_g1=list(nodes_no_match.keys())
    #图2中不匹配的点
    match_g2 = list(nodes_no_match.values())

    out_graph_begin=time.time()
    dict1 = {}
    s=G.order()
    for i in nodes_G2:
        dict1[i] = s
        s=s+1
    #结合图
    # f = open(out_graph,'w')
    dict1.update(nodes_no_match)
    G1_sample = nx.relabel_nodes(G1_sample, dict1)

    compose_graph = nx.compose(G, G1_sample)

    nx.write_edgelist(compose_graph,out_graph,data=False)
    out_graph_after = time.time()
    print("write out graph time is %f" % (out_graph_after-out_graph_begin))
    #写原图
    # print("writing source graph")
    # for i in edges_g1:
    #     f.writelines(str(i[0])+" "+str(i[1])+"\n")
    # print("writing source graph done")
    # #写目标图
    # print("writing taget graph")
    # for i in edges_g2:
    #     u=i[0]
    #     v=i[1]
    #     if u in nodes_match and v in nodes_match:
    #         continue
    #     if u not in nodes_match:
    #         if u in match_g2:
    #             u = match_g1[match_g2.index(u)]
    #         else:
    #             # 采样列表，当前节点编号，采样数量，原图节点
    #             # u = tag(nodes_G2, u)+G.order()
    #             u=dict1[u]+G.order()
    #     if v not in nodes_match:
    #         if v in match_g2:
    #             v = match_g1[match_g2.index(v)]
    #         else:
    #             # v = tag(nodes_G2, v)+G.order()
    #             v = dict1[v] + G.order()
    #     f.writelines(str(u) + " " + str(v)+"\n")
    # f.close()
    # print("writing taget graph done")
    # out_graph_after = time.time()
    # print("write out graph time is %f" % (out_graph_after-out_graph_begin))
    #G_new = load_file(out_graph)
    #有节点丢失
    # print("新图节点总数："+str(G.number_of_nodes()*2-len(nodes_g2)))
    # print(dict1)
    #在新图上实际对应节点
    fb = open(aline_file,'w')
    for i in nodes_G2:
        fb.writelines(str(i)+" "+str(dict1[i])+"\n")
    fb.close()
    const(G.order()+len(nodes_G2),isdirected,out_graph)
    # edgelist = nx.read_edgelist(out_graph)
    return G.order()+len(nodes_G2)



def combin_biggraph_true(inptut_graph,ratio,sample_nodes,aline_file,out_graph,isdirected):
    #True代表无向图
    G =load_file(inptut_graph,False)
    print("原图节点数："+str(G.number_of_nodes()))
    #去除一定的边
    G1_sample = sample_graph(G, ratio)
    print("破坏后图中节点：" + str(G1_sample.number_of_nodes()))
    G2 = get_subgraph(G1_sample, sample_nodes)
    GC2 = max((G2.subgraph(c1) for c1 in nx.connected_components(G2)), key=len)
    G1 = get_subgraph(G, sample_nodes)
    GC1 = max((G1.subgraph(c1) for c1 in nx.connected_components(G1)), key=len)



    #匹配的点
    nodes_match=[]
    #不匹配的点
    nodes_no_match={}

    nodes_G2 = list(G1_sample.nodes())
    seed_time1=time.time()
    matches_ms = []
    for i in GC2.nodes():
        matches_ms.append((int(i), int(i)))


    seed_time2 = time.time()
    seed_time=seed_time2-seed_time1
    # print("seed time is %f" % seed_time)
    nodes_g2=[]
    # print("before %f" % len(nodes_G2))
    for match in matches_ms:
        nodes_G2.remove(match[1])
        nodes_g2.append(match[1])
        if match[0] == match[1]:
            nodes_match.append(match[1])
            nodes_match.sort()
        else:
            nodes_no_match[match[1]]=match[0]
    print("不匹配的点")
    print(nodes_no_match)


    out_graph_begin=time.time()
    dict1 = {}
    s=G.order()
    for i in nodes_G2:
        dict1[i] = s
        s=s+1
    dict1.update(nodes_no_match)
    G1_sample = nx.relabel_nodes(G1_sample, dict1)

    compose_graph = nx.compose(G, G1_sample)

    nx.write_edgelist(compose_graph,out_graph,data=False)
    out_graph_after = time.time()
    print("write out graph time is %f" % (out_graph_after-out_graph_begin))
    fb = open(aline_file,'w')
    for i in nodes_G2:
        fb.writelines(str(i)+" "+str(dict1[i])+"\n")
    fb.close()
    const(G.order()+len(nodes_G2),isdirected,out_graph)
    # edgelist = nx.read_edgelist(out_graph)
    return G.order()+len(nodes_G2),seed_time


