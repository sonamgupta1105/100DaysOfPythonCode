'''
Reference: https://www.geeksforgeeks.org/detect-cycle-in-a-graph/

This code creates a graph, generate paths and detects a cycle using DFS

Few things to note:
1. In the main function, input_data is a dictionary which is then converted into a pandas dataframe.
2. The decision string in the dataframe 'end_approve' is encoded as 0 whereas 'end_deny' as -1 for the sake of reading it into a graph. 
3. When you call generate_paths(df_in), it reads the dataframe into a list of lists
4. The string values are renamed back before printing the output. 
5. If any value in the input dataframe is changed to a repeated value of a node, ValueError is raised. 
6. There are 2 util functions, one for finding paths, and the other for detecting the cycle.

'''
from collections import defaultdict

import pandas as pd
class Graph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
    
    # Creating a global list for returning the output. 
    global decision_path
    decision_path = []
    

    def addEdge(self, u, v):
        self.graph[u].append(v)
    
    def pathsUtil(self, u, d, visited_nodes, path):
        visited_nodes[u] = True
        path.append(u)

        if u == d:
            decision_path.append(list(path))
            
        else:
            for i in self.graph[u]:
                if visited_nodes[i]==False:
                    self.pathsUtil(i, d, visited_nodes, path)
            
        path.pop()
        visited_nodes[u]=False
        
    
    def printAllPaths(self, s, d):
        visited = [False]*(self.V)
        path = []
        self.pathsUtil(s, d, visited, path)
        
        
    def cycleUtil(self, v, visited, recStack):
 
        visited[v] = True
        recStack[v] = True

        for neighbor in self.graph[v]:

            if visited[neighbor] == False:
                if self.cycleUtil(neighbor, visited, recStack) == True:
                    return True
            
            elif recStack[neighbor] == True:
                return True
 
        recStack[v] = False
        return False
 
    def isCyclic(self):
        visited = [False] * (self.V + 1)
        recStack = [False] * (self.V + 1)
        for node in range(self.V):
            if visited[node] == False:
                if self.cycleUtil(node,visited,recStack) == True:
                    return True
        return False

def generate_paths(df_in):
    input = df_in.values.tolist()
    #Initializing maximum vertices
    g = Graph(200)
    
    # First row is the starting node as mentioned in the problem statement
    root = input[0][0]
    for i in range(0, len(input)):
        left = input[i][1]
        right = input[i][2]

        g.addEdge(input[i][0],left)
        g.addEdge(input[i][0],right)

    if g.isCyclic() == 1:
        raise ValueError("Circular path detected")
    else:      
        print ("Paths to decision:")
        g.printAllPaths(root, 0)
        g.printAllPaths(root, -1)

        # Converting the decision strings in the list of lists to its original names
        for i, x in enumerate(decision_path):
            for j, a in enumerate(x):
                if a == 0:
                    decision_path[i][j] = 'end_approve'
                if a == -1:
                    decision_path[i][j] = 'end_deny'

        print(decision_path)

if __name__ == "__main__":
    input_data = {'Node_ID':[1, 2, 3],
                'true':[2, 'end_approve', 'end_deny'],
                'false':[3, 3, 'end_approve']}
    
    df_in = pd.DataFrame(input_data)
    df_in = df_in.replace(['end_approve'], 0)
    df_in = df_in.replace(['end_deny'], -1)

    generate_paths(df_in)
