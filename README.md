# EulerTikz
## Plugin Requirements:
- 'numpy' should be in 'sublime-text-3/Packages'
- the contents of the 'src' folder should be in 'sublime-text-3/Packages/User'
## Plot Requirements:
- numpy and matplotlib should be installed (this is not a plugin)
## Input:
    In the first line, there should be two integers: n the number of nodes, and m the number of edges.
    Then, m lines should follow that each contain two integers u and v such that 0<=u,v<n.
## Notice:
    As of right now, the plugin and the plot only accept undirected graphs.
## Running the Plugin:
    After highlighting the input, enter 'view.run_command("layout")' in the sublime command window.
## Running the Plot:
    force-layout.py is a normal python program that you can run on your terminal
## Methods:
- Firstly, [spectral layout](https://en.wikipedia.org/wiki/Spectral_layout) was used to determine the relative positions of the vertices. Using the eigenvectors corresponding to the smallest positive eigenvalues of the Laplacian, we obtain the coordinates for the ith vertex by using ith entries of the eigenvectors.
- Then, we used a [force-based layout](https://en.wikipedia.org/wiki/Force-directed_graph_drawing) to spread out vertices.
## TODO:

Configurative: Improve and add more configuration tools, this feature will speedup our analyses.

EulerTikz Classifier and more algorithms: classifies graphs based on input, some algorithms work better on certain kinds of graphs.

sublime text live image integration: easy to generate images. how can we integrate them within the sublime text environment?

- Draw rectilinear edges in plugin
- Implement Inverse power method

### Spectral Layout Algorithms
Let G be a ***simple*** graph, D be the degree matrix of G and A be the adjacency matrix of G. Define the Laplacian matrix L = D - A. The Spectral layout algorithms uses the eigenvectors of L as the Cartesian coordinates of the graph's vertices.

The idea of the layout is to compute the two largest (or smallest) eigenvalues and corresponding eigenvectors of the Laplaian matrix of the graph and then use those for actually placing the nodes. The x-coordinate is the value of the i-th coordinate of the first eigenvector. Likewise, the i-th component of the second eigenvector describes the y-coordinate of the point i.
