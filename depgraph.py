"""
Dependency Graph
"""

class Node(object):
    """
    A simple node object for use in a graph.

    The Nodes does not prevent you from adding circular dependencies,
    but the traversing functions such as search will not reflect these
    recurrences.
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
    
    def search(self, nname, visited=None):
        """
        Search a the nodes subtree for a node with a given name.
        
        Key arguments:
            nname -- A string with the name of the node to look for.
        
        Returns:
            If the node is in the tree, returns the Node in question.
            Otherwise, returns None.
        """

        ## Guards against: http://effbot.org/zone/default-values.htm
        if visited is None:
            visited = []

        if self.name == nname:
            return self
        visited.append(self.name)
        for child in self.children:
            if not (child.name in visited): 
                res = child.search(nname, visited)
                print(self.name + " : (" + child.name + " == " + nname + ") = " + str(res))
                if res != None:
                    return res
        return None
    
    def return_tree(self, olist, visited=None):
        """
        Return this node's tree.
        
        Key arguments:
            list -- A list to contain the tree (can be non-empty)
        
        Returns:
            list -- The tree of the node appended to the list
        """
        if visited is None:
            visited = []

        if not (self in visited):
            visited.append(self)
            olist.append((self.name, self.children))
            for child in self.children:
                child.return_tree(olist, visited)
        return olist

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
            for node in self.endnodes:
                endnodes += node.name + "|"
        print("Independent nodes: " + endnodes)
    
    def add_independent(self, node):
        """
        Adds a new independent node to the graph.
        
        Key arguments:
            node -- The independent node to be added to the graph
        """
        node.add_parent(self.head)

        # TODO: Do we need the endnode list if they are all connected to
        # the HEAD anyway?
        self.endnodes.append(node)
        self.head.add_child(node)
    
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
            node.add_parent(dependency.branch)
            node.add_child(dependency)
            return True
        else:
            return False
    
    def return_dependencies(self, node):
        """
        Returns a list containing the dependencies of a node one level down.
        
        Key arguments:
            node -- The node to look up dependencies for
        
        Returns:
            dependencies -- A list of the names of all dependencies of the given node
        """ 
        dependencies = []
        for child in node.children:
            dependencies.append(child.name)
        return dependencies
    
    def return_dependencies_str(self, node):
        """
        Returns a string containing the dependencies of a node one level down.
        
        Key arguments:
            node -- The node to look up dependencies for
        
        Returns:
            str -- A string containing all near dependencies of the node in
            readable form.
        """
        ostr = "Dependencies of " + node.name + ": "
        for child in node.children:
            ostr += child.name + ", "

        return ostr[:-2]
    
    def return_graph(self):
        """
        Returns all the dependencies in the current graph in the following form:
        
            [(Node, [Dependency, Dependency, ... Dependency]),
             (Node, [Dependency, Dependency, ... Dependency]),
             ...
             (Node, [Dependency, Dependency, ... Dependency])]
        """
        graph = []

        for node in self.head.children:
            node.return_tree(graph)
        return graph
    
    def print_graph(self):
        """
        Prints the graph in a (somewhat) readable form.
        """
        graph = self.return_graph()
        for i in xrange(0, len(graph)):
            output = "Dependencies of " + graph[i][0] + ": "

            for j in xrange(0, len(graph[i][1])):
                output += graph[i][1][j].name
                if j != len(graph[i][1]) - 1:
                    output += ", "
            print(output)
    
    def convert_objlist(self, objlist):
        """
        Takes a (makefile) list of the following form:
        
            [(Object name, [list of dependencies]),
             (Object name, [list of dependencies])]
        
        The object name is in the form of a string, such as "main.o".
        The list of dependencies are a list of strings, such as "main.c"
        
        This list is then converted into a dependency graph.
        
        NOTE: It will write over any graph currently stored.
        """
        self.endnodes = []
        
        independent = []
        dependent = []
        for i in xrange(0, len(objlist)):
            if objlist[i][1] == []:
                independent.append(objlist[i])
            else:
                dependent.append(objlist[i])
                
        # Add all independent nodes
        for j in xrange(0, len(independent)):
            self.add_independent(Node(independent[j][0]))
        
        # Runs through all dependent nodes until they have all been added.
        # Returns a message if not all dependencies has been added.
        check = 0
        while dependent != []:
            check = len(dependent)
            for k in xrange(0, len(dependent)):
                deleted = []
                for l in xrange(0, len(dependent[k][1])):
                    if self.add_dependency(dependent[k][0],
                                           dependent[k][1][l]):
                        deleted.append(dependent[k][1][l])
                for m in xrange(0, len(deleted)):
                    dependent[k][1].remove(deleted[m])
                if dependent[k][1] == []:
                    del dependent[k]
            if check == len(dependent):
                break
        
        print("Not added due to lack of necessary dependancies: "
              + str(dependent))

    def makefile_to_objlist(filepath):
        """
        Takes a path to a makefile and constructs an object list
        that can be converted to a dependency graph.
        """
        #TODO: Implement.
        pass

    def from_makefile(filepath):
        """
        Takes a filepath and creates a dependency graph.

        NOTE: It will write over any graph currently stored.
        """
        #TODO: Implement.
        pass