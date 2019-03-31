import pycosat
import sys

def generateVertices(ipt):
    vertices = {}
    for i in ipt:
        if i[0] in vertices.keys():
            vertices[i[0]].append(i[1])
        else:
            vertices[i[0]] = [i[1]]
    
        if i[1] in vertices.keys():
            vertices[i[1]].append(i[0])
        else:
            vertices[i[1]] = [i[0]]
    return vertices

def main():
    f = open(sys.argv[1])
    ipt = eval(f.readline().rstrip())
    vertices = generateVertices(ipt)
    colours = eval(f.readline().rstrip())
    literals = {}
    counter = 1

    #Generate literals
    for vertex in vertices.keys():
        for colour in colours:
            literals[(vertex, colour,)] = counter
            counter += 1
    print(literals)

    #Every vertex should have at least one colour
    clauses = []
    for i in vertices:
        clause = []
        for c in colours:
            clause.append(literals[(i,c,)])
        clauses.append(clause)

    #Every vertex should have at most one colour
    for v in vertices:
        for i, c in enumerate(colours):
            for c2 in colours[i+1:]:
                clauses.append([-literals[(v,c,)], -literals[(v,c2)]])
        
    #No neighbours should have the same colour
    for v in vertices:
        for n in vertices[v]:
            for c in colours:
                clauses.append([-literals[(v,c,)], -literals[(n,c,)]])

    decode = {}

    for i in literals.keys():
        decode[literals[i]] = i

    sol = pycosat.solve(clauses)
    if sol != 'UNSAT':
        for i in sol:
            if i>0:
                pair = decode[i]
                print("Vector ", pair[0], "is colour", pair[1])
    else:
        print(sol)

if __name__ == "__main__":
    main()
