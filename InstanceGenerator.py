import os
import math
import random


def load_file(path):
    directory = os.path.join("raw")
    for Filename in os.listdir(directory):
        print(Filename) 

        with open(os.path.join("raw",Filename)) as f:
            lines = f.readlines()

            Arcs=[]
            for line in lines:
                if line[0]=='A' and line[2]=='=':   
                    content = line[6:-3].split('), (')
                if line[0]=='V' and line[2]=='=':
                    nodes = line[5:-2].split(', ')
                if line.startswith("Omega"):
                    Omega = line.split("=")[1]
                if line.startswith("Theta"):
                    Theta = line.split("=")[1]
                if line.startswith("Lambda"):
                    Lambda = line.split("=")[1]
            for arc in content:
                Arcs.append(arc.split(', '))
            return nodes, Omega, Theta, Lambda
        
def create_instance(nodes,Arcs,Omega ,Theta, Lambda, Number="001"):
#Access arc i by Arcs[i][0] and Arcs[i][1]
    with open(f'instances/rndgraph{Density}-{len(nodes)}_{Omega}-{Theta}-{Lambda}_{Number}.qlp', 'w') as f:
        f.write('MAXIMIZE\n')
        for v in nodes:
                f.write('+alpha_'+str(v)+' ')

        f.write('\nSUBJECT TO\n')
        for v in nodes:
            f.write('+z_'+str(v)+' ')
        f.write('<= '+str(Omega)+'\n')
        for v in nodes:
            f.write('+x_'+str(v)+' ') 
        f.write('<= '+str(Lambda)+'\n')
        for v in nodes:
            f.write('+alpha_'+str(v)+' +y_'+str(v)+' <= 1\n')
        for i in range(len(Arcs)):
            f.write('+alpha_'+str(Arcs[i][1])+' -alpha_'+str(Arcs[i][0])+' -x_'+str(Arcs[i][1])+' -z_'+str(Arcs[i][1])+' <= 0\n')
        f.write('UNCERTAINTY SUBJECT TO\n')
        for v in nodes:
            f.write('+y_'+str(v)+' ')  
        f.write('<= '+str(Theta)+'\n')
        for v in nodes:
            f.write('+y_'+str(v)+' +z_'+str(v)+' <= 1\n')

        f.write('BOUNDS\n')
        for v in nodes:
            f.write('0<=x_'+str(v)+'<=1'+'\n')
            f.write('0<=y_'+str(v)+'<=1'+'\n')
            f.write('0<=z_'+str(v)+'<=1'+'\n')
            f.write('0<=alpha_'+str(v)+'<=1'+'\n')
        f.write('BINARIES\n')
        for v in nodes:
            f.write('x_'+str(v)+'\n')
            f.write('y_'+str(v)+'\n')
            f.write('z_'+str(v)+'\n')
    
        f.write('EXISTS\n')
        for v in nodes:
            f.write('x_'+str(v)+'\n')
            f.write('z_'+str(v)+'\n')
            f.write('alpha_'+str(v)+'\n')
        f.write('ALL\n')
        for v in nodes:    
            f.write('y_'+str(v)+'\n')

        f.write('ORDER\n')
        for v in nodes:
            f.write('z_'+str(v)+'\n')
        for v in nodes:
            f.write('y_'+str(v)+'\n')
        for v in nodes:
            f.write('x_'+str(v)+'\n')
        for v in nodes:
            f.write('alpha_'+str(v)+'\n')
        f.write('END')

def create_rnd_graph(num_nodes,Density):
    nodes = []
    for node in range(1,num_nodes+1):
        nodes.append(node)
    
    full_edges = num_nodes * (num_nodes - 1)
    num_arcs = math.ceil(Density * full_edges)
    
    arcs = []
    # Wähle eine zufällige Reihenfolge der Knoten
    random.shuffle(nodes)

# Erstelle einen gerichteten Spannbaum
    for i in range(1, num_nodes):
        arcs.append((nodes[i-1], nodes[i]))

    while len(arcs) < num_arcs:
        u = random.choice(nodes)
        v = random.choice(nodes)
        if u != v and (u, v) not in arcs:
            arcs.append((u, v))
    return nodes, arcs


if __name__ == "__main__":
    Omega = 3
    Theta = 3
    Lamda = 3
    Density = 0.05
    Num_nodes = 20
    nodes, arcs = create_rnd_graph(Num_nodes,Density,)
    create_instance(nodes,arcs,Omega,Theta,Lamda)
    

