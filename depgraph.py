"""
Dependency Graph
"""

class Node(object):
    """
    A simple node object for use in a tree graph
    """
    def __init__(self, name):
        """
        Initializes a new node with a specified name.
        The node is not connected to any other nodes.
        
        Key arguments:
            name -- A string consisting of the key identifier
        """
        self.name = name
        self.parents = []
        self.children = []

    def __str__(self):
        return "NODE( " + self.name + " )"
    
    def add_child(self, child):
        """
        Adds a child to the node.
        
        Key arguments:
            child -- Another node object
        """
        child.parents.append(self)
        self.children.append(child)
    
    def add_parent(self, parent):
        """
        Adds a parent to the node
        
        Key arguments:
            parent -- Another node object
        """
        self.parents.append(parent)
        parent.children.append(self)
    
    def search(self, name, visited = []):
        """
        Search a the nodes subtree for a node with a given name.
        
        Key arguments:
            name -- A string with the name of the node to look for.
        
        Returns:
            If the node is in the tree, returns the Node in question.
            Otherwise, returns None.
        """
        if self.name == name:
            return self
        visited.append(self.name)
        for child in self.children:
            if not (child.name in visited): 
                res = child.search(name, visited)
                if res != None:
                    return res
                visited.append(child.name)
        return None
    
    def return_tree(self, list, visited):
        """
        Return this node's tree.
        
        Key arguments:
            list -- A list to contain the tree (can be non-empty)
        
        Returns:
            list -- The tree of the node appended to the list
        """
        if not (self in visited):
            visited.append(self)
            list.append((self.name, self.children))
            for i in range(0, len(self.children)):
                self.children[i].return_tree(list, visited)
        return list

class DependencyGraph(object):
    """
    Dependency graph built from the bottom and up.
    """
    def __init__(self):
        """
        Creates a new empty dependency graph.
        """
        self.head = Node("HEAD")
        self.endnodes = []
    
    def print_info(self):
        """
        Prints the current independent nodes (if any).
        """
        endnodes = "|"
        if self.endnodes == None:
            endnodes += "None|"
        else:
            for i in range (0, len(self.endnodes)):
                endnodes += self.endnodes[i].name + "|"
        print("Independent nodes: " + endnodes)
    
    def add_independent(self, node):
        """
        Adds a new independent node to the graph.
        
        Key arguments:
            node -- The independent node to be added to the graph
        """
        node.branch = self.head
        self.endnodes.append(node)
        self.head.leaves.append(node)
    
    def add_dependency(self, nodename, depname):
        """
        Adds a new dependency to the graph.
        
        Key arguments:
            nodename: The name of the node that gets a new dependency added.
                      If the node does not exist, it is added to the graph.
            depname: The name of the dependency it should be connected to.
                    It must already be in the tree.
        
        Returns:
            True if the dependency has been created, otherwise False. False
            only occurs when trying to create a dependency to a node that does
            not exist in the graph.
        """
        node = self.head.search(nodename)
        if node == None:
            node = Node(nodename)
        dependency = self.head.search(depname)
        if dependency != None:
            if self.head in dependency.parents:
                self.head.leaves.remove(dependency)
            node.add_branch(dependency.branch)
            node.add_leaf(dependency)
            return True
        else:
            return False
    
    def return_dependencies(self, node):
        """
        Returns a list containing the dependencies of a node one level down.
        
        Key arguments:
            node -- The node to look up dependencies for
        
        Returns:
            list -- A list of the names of all dependencies of the given node
        """ 
        list = []
        for i in range(0, len(node.leaves)):
            list.append(node.leaves[i].name)
        return list
    
    def return_dependencies_str(self, node):
        """
        Returns a string containing the dependencies of a node one level down.
        
        Key arguments:
            node -- The node to look up dependencies for
        
        Returns:
            str -- A string containing all near dependencies of the node in
            readable form.
        """
        str = "Dependencies of " + node.name + ": "
        for i in range(0, len(node.leaves)):
            str += node.leaves[i].name
            if i != len(node.leaves) - 1:
                str += ", "
        return str
    
    def return_graph(self):
        """
        Returns all the dependencies in the current graph in the following form:
        
            [(Node, [Dependency, Dependency, ... Dependency]),
             (Node, [Dependency, Dependency, ... Dependency]),
             ...
             (Node, [Dependency, Dependency, ... Dependency])]
        """
        list = []
        visited = []
        for i in range(0, len(self.head.leaves)):
            self.head.leaves[i].return_tree(list, visited)
        return list
    
    def print_graph(self):
        """
        Prints the graph in a (somewhat) readable form.
        """
        graph = self.return_graph()
        for i in range(0, len(graph)):
            str = "Dependencies of " + graph[i][0] + ": "
            for j in range(0, len(graph[i][1])):
                str += graph[i][1][j].name
                if j != len(graph[i][1]) - 1:
                    str += ", "
            print(str)
    
    def convert_makefile(self, list):
        """
        Takes a (makefile) list of the following form:
        
            [(Object name, [list of dependencies]),
             (Object name, [list of dependencies])]
        
        The object name is in the form of a string, such as "main.o".
        The list of dependencies are a list of strings, such as "main.c"
        
        This list is then converted into a dependency graph.
        
        NOTE: It will write over any current graph stored.
        """
        self.endnodes = []
        
        independent = []
        dependent = []
        for i in range(0, len(list)):
            if list[i][1] == []:
                independent.append(list[i])
            else:
                dependent.append(list[i])
                
        # Add all independent nodes
        for j in range(0, len(independent)):
            self.add_independent(Node(independent[j][0]))
        
        # Runs through all dependent nodes until they have all been added.
        # Returns a message if not all dependencies has been added.
        check = 0
        while dependent != []:
            check = len(dependent)
            for k in range(0, len(dependent)):
                deleted = []
                for l in range(0, len(dependent[k][1])):
                    if self.add_dependency(dependent[k][0],
                                            dependent[k][1][l]):
                        deleted.append(dependent[k][1][l])
                for m in range(0, len(deleted)):
                    dependent[k][1].remove(deleted[m])
                if dependent[k][1] == []:
                    del dependent[k]
            if check == len(dependent):
                break
        
        print("Not added due to lack of necessary dependancies: "
              + str(dependent))