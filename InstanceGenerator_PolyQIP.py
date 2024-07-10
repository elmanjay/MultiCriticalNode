import os
 
# Use raw string to avoid issues with backslashes
directory = r'raw'

# Check if the directory exists
if not os.path.isdir(directory):
    print(f"The directory '{directory}' does not exist.")
else:
    for filename in os.listdir(directory):
        print(filename)
        
        # Construct the full file path
        filepath = os.path.join(directory, filename)
        
        with open(filepath, 'r') as f:
            lines = f.readlines()
            print(lines)  # Printing lines just to show it worked
for Filename in os.listdir(directory):
    print(Filename) 

    with open('raw/'+Filename) as f:
        lines = f.readlines()

    SplitFilename=Filename.split('_')
    Data=SplitFilename[1].split('-')
    print(Data)
    Omega=Data[0]
    Theta=Data[1]
    Lambda=Data[2]

    Arcs=[]
    for line in lines:
        if line[0]=='A' and line[2]=='=':   
            content = line[6:-3].split('), (')
        if line[0]=='V' and line[2]=='=':
            nodes = line[5:-2].split(', ')
    for arc in content:
        Arcs.append(arc.split(', '))

#Access arc i by Arcs[i][0] and Arcs[i][1]
    with open('Instances_PolyQIP/'+Filename+'.qlp', 'w') as f:
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
            f.write('+alpha_'+str(v)+' -z_'+str(v)+' +y_'+str(v)+' <= 1\n')
        for i in range(len(Arcs)):
            f.write('+alpha_'+str(Arcs[i][1])+' -alpha_'+str(Arcs[i][0])+' -x_'+str(Arcs[i][1])+' -z_'+str(Arcs[i][1])+' <= 0\n')
        f.write('UNCERTAINTY SUBJECT TO\n')
        for v in nodes:
            f.write('+y_'+str(v)+' ')  
        f.write('<= '+str(Theta)+'\n')

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
