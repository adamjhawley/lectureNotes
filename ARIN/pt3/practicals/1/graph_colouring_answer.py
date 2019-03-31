import sys
import pycosat

fobj = open(sys.argv[1])
colours = range(int(fobj.readline().rstrip()))
vertices = range(int(fobj.readline().rstrip()))
edges = []
for line in fobj:
    [frm,to] = line.rstrip().split()
    edges.append((int(frm), int(to))) 
fobj.close()

cnf = []
last = {'last':1}
enc = {}

def encode(vertex,colour):
    try:
        return enc[vertex,colour]
    except KeyError:
        thislast = last['last']
        enc[vertex,colour] = thislast
        last['last'] += 1
        return thislast
    
for v in vertices:
    # at least one colour
    cnf.append([encode(v,colour) for colour in colours])
    # at most one colour
    for i, c1 in enumerate(colours):
        for c2 in colours[i+1:]:
            cnf.append([-encode(v,c1),-encode(v,c2)])

for (frm,to) in edges:
    for c in colours:
        # cannot have same colour for two connected vertices
        cnf.append([-encode(frm,c),-encode(to,c)])

print (cnf)
sol = pycosat.solve(cnf)
if sol != 'UNSAT':
    for (vertex,colour), val in enc.items():
        if sol[val-1] > 0:
            print ('vertex', vertex, 'has colour', colour )
else:
    print ('cannot colour')
