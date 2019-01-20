# Eulertikz

## Project Overview
EulerTikz is a visualization tool for discrete graphs, or networks. The tool includes a Latex Parser that extracts a graph encoded using the tikzpicture in a relative placement format and generate a visualization of the corresponding graph.

## Utilities
The dependencies include:
* Python 3.x.x
* Numpy
* Pygame

## How to use
To run the program over a Tex document, simply input the .tex file through stdin and run force-latex.py.

## Methods
* Firstly, spectral layout was used to determine the relative positions of the vertices. Using the eigenvectors corresponding to the smallest positive eigenvalues of the Laplacian, we obtain the coordinates for the ith vertex by using ith entries of the eigenvectors.
* Then, we used a force-based layout to spread out vertices.

### Spectral Layout Algorithms
Let G be a simple graph, D be the degree matrix of G and A be the adjacency matrix of G. Define the Laplacian matrix L = D - A. The Spectral layout algorithms uses the eigenvectors of L as the Cartesian coordinates of the graph's vertices.

The idea of the layout is to compute the two largest (or smallest) eigenvalues and corresponding eigenvectors of the Laplaian matrix of the graph and then use those for actually placing the nodes. The x-coordinate is the value of the i-th coordinate of the first eigenvector. Likewise, the i-th component of the second eigenvector describes the y-coordinate of the point i.

### Issues
Configurative: Improve and add more configuration tools, this feature will speedup our analyses.

EulerTikz Classifier and more algorithms: classifies graphs based on input, some algorithms work better on certain kinds of graphs.

sublime text live image integration: easy to generate images. how can we integrate them within the sublime text environment?

* Draw rectilinear edges in plugin
* Implement Inverse power method