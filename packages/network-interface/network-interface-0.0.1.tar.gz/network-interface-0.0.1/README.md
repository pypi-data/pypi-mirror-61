

# network-interface
In order to install, open the command prompt and type:
```
pip install network-interface
```

In this module you will find NetworkInterface class which is an abstract class to standardize the way of creating a network graph in networkx.

Once you install this library, you have to install igraph library where:
- Refer to [igraph/python](https://igraph.org/python/ ) if you are a linux or mac user
- Refer to [stackoverflow](https://stackoverflow.com/questions/34113151/how-to-install-igraph-for-python-on-windows) if you are a windows user

In order to use the class, you have to inherit this class and define the following abstract methods according to your dataset:
- get_nodes
- get_edges

This class also has some helpful methods like (use help function to get more info about them):
- get_nodes_list
- get_edges_list
- create_network_graph
- nodes_df_to_nodes_list
- calculate_nodes_positions(using the most common algorithms to calculate nodes positions in a network graph)
- append_nodes_positions_to_nodes_attributes
- get_nodes_pos_dict

The following directory [to be added later]() shows a concrete example about how to use the class
