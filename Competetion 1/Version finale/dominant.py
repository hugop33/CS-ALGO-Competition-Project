import sys, os, time

import networkx as nx

########### Pour les deux méthodes ###########

def is_dominant(G, D):

    dominated_nodes = set(D)
    
    for node in D:
        dominated_nodes.update(G.neighbors(node))
        
    return dominated_nodes == set(G.nodes)

def improve_dominating_set_recursive(G, D0):
    D = D0.copy()
    
    improvement = True
    while improvement:
        improvement = False
        for node in list(D):
            D_temp = D - {node}
            if is_dominant(G, D_temp):
                D = D_temp
                improvement = True
                break 

    return D

###########  Méthode 1 (V6)  ###########

def dominant_set(g, bonus):
    not_dominated = set(g.nodes)
    dominating_set = set()
    while not_dominated:
        v = max(not_dominated, key=lambda x: len(set(g.neighbors(x)) & not_dominated) + bonus * sum(1 for y in set(g.neighbors(x)) & not_dominated if len(set(g.neighbors(y)) & not_dominated) == 1))
        dominating_set.add(v)
        not_dominated -= {v} | set(g.neighbors(v))
    return dominating_set

def dominant_set_avoiding(g, avoiding_set, bonus):
    not_dominated = set(g.nodes)
    dominating_set = set()
    while not_dominated:
        v = max(not_dominated, key=lambda x: len(set(g.neighbors(x)) & not_dominated) + bonus * sum(1 for y in set(g.neighbors(x)) & not_dominated if len(set(g.neighbors(y)) & not_dominated) == 1) - (10 if x in avoiding_set else 0))
        dominating_set.add(v)
        not_dominated -= {v} | set(g.neighbors(v))
    return dominating_set

###########  Méthode 2 (V10)  ###########

def greedy_dominating_set_from_node(G, start_node, exclude_nodes=set()):
    dominating_set = {start_node}
    dominated_nodes = set(dominating_set)
    
    while len(dominated_nodes) < len(G):
        dom_counts = [(len(set(G[node]) - dominated_nodes), node) for node in G if node not in dominating_set and node not in exclude_nodes]

        if not dom_counts:  # arrêter boucles infinis
            break

        _, next_node = max(dom_counts)

        dominating_set.add(next_node)
        dominated_nodes.add(next_node)
        dominated_nodes.update(G[next_node])
    
    return dominating_set

def greedy_dominating_set(G, exclude_nodes=set()):

    best_dominating_set = set(G.nodes())

    sorted_nodes = sorted(G.nodes(), key=lambda node: G.degree(node), reverse=True)

    # 10 premiers nœuds
    for node in sorted_nodes[:10]:
        if node not in exclude_nodes:
            dominating_set = greedy_dominating_set_from_node(G, node, exclude_nodes)
            if len(dominating_set) < len(best_dominating_set):
                best_dominating_set = dominating_set

    return best_dominating_set


###########  Dominant fonction principale  ###########

def dominant(g):
    
    ### Méthode 1 ###
    
    best_score = float('inf')
    best_D1 = best_D2 = None
    V = set(g.nodes)
    
    # Teste les bonus de feuilles du graphe par pas de 0.5
    for bonus in [i/2 for i in range(5,11)]:
        D1 = dominant_set(g, bonus)
        D1=improve_dominating_set_recursive(g, D1)
        D2 = dominant_set_avoiding(g, D1, bonus)
        D2 =improve_dominating_set_recursive(g, D2)
                
        score = (len(D1) + len(D2) + len(D1 & D2)) / len(V)
        
        if score < best_score:
            best_score = score
            best_D1, best_D2 = D1, D2
    
    D1_1,D2_1,score_1= best_D1, best_D2,best_score
    
    ### Méthode 2 ###
    
    D1 = greedy_dominating_set(g)
    D1 = improve_dominating_set_recursive(g, D1)
    D2 = greedy_dominating_set(g, D1)
    D2 = improve_dominating_set_recursive(g, D2)

    for D in [D1, D2]:
        nodes_to_check = list(D)
        for node in nodes_to_check:
            D.remove(node)
            if not is_dominant(g, D):
                D.add(node)
    
        score = (len(D1) + len(D2) + len(D1.intersection(D2))) / len(V)
    
    D1_2,D2_2,score_2= D1, D2, score
    
    ### Affichage ###
    
    if score_1 > score_2 and is_dominant(g, D1_2) and is_dominant(g, D2_2):
        print (1,g.number_of_nodes(),g.number_of_edges(),is_dominant(g, D1_2), is_dominant(g, D2_2), score_2)
        
        
        return D1_2,D2_2
    
    else :
        print (0,g.number_of_nodes(),g.number_of_edges(),is_dominant(g, D1_1), is_dominant(g, D2_1), score_1)
        return D1_1,D2_1


    

#########################################
#### Ne pas modifier le code suivant ####
#########################################


def load_graph(name):
    with open(name, "r") as f:
        state = 0
        G = None
        for l in f:
            if state == 0:  # Header nb of nodes
                state = 1
            elif state == 1:  # Nb of nodes
                nodes = int(l)
                state = 2
            elif state == 2:  # Header position
                i = 0
                state = 3
            elif state == 3:  # Position
                i += 1
                if i >= nodes:
                    state = 4
            elif state == 4:  # Header node weight
                i = 0
                state = 5
                G = nx.Graph()
            elif state == 5:  # Node weight
                G.add_node(i, weight=int(l))
                i += 1
                if i >= nodes:
                    state = 6
            elif state == 6:  # Header edge
                i = 0
                state = 7
            elif state == 7:
                if i > nodes:
                    pass
                else:
                    edges = l.strip().split(" ")
                    for j, w in enumerate(edges):
                        w = int(w)
                        if w == 1 and (not i == j):
                            G.add_edge(i, j)
                    i += 1

        return G


#########################################
#### Ne pas modifier le code suivant ####
#########################################
if __name__ == "__main__":
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])

    # un repertoire des graphes en entree doit être passé en parametre 1
    if not os.path.isdir(input_dir):
        print(input_dir, "doesn't exist")
        exit()

    # un repertoire pour enregistrer les dominants doit être passé en parametre 2
    if not os.path.isdir(output_dir):
        print(input_dir, "doesn't exist")
        exit()

        # fichier des reponses depose dans le output_dir et annote par date/heure
    output_filename = 'answers_{}.txt'.format(time.strftime("%d%b%Y_%H%M%S", time.localtime()))
    output_file = open(os.path.join(output_dir, output_filename), 'w')

    for graph_filename in sorted(os.listdir(input_dir)):
        # importer le graphe
        g = load_graph(os.path.join(input_dir, graph_filename))

        # calcul du dominant
        d1, d2 = dominant(g)
        D1 = sorted(d1, key=lambda x: int(x))
        D2 = sorted(d2, key=lambda x: int(x))

        # ajout au rapport
        output_file.write(graph_filename)
        for node in D1:
            output_file.write(' {}'.format(node))
        output_file.write('-')
        for node in D2:
            output_file.write(' {}'.format(node))
        output_file.write('\n')

    output_file.close()
