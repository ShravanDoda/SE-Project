from graphviz import Digraph
from spotify_interface import process_metadata

spotify = Digraph(comment='Spotify Graph', format='svg')

spotify_graph.graph_attr['rankdir'] = 'LR'

def add_nodes_digraph():
    meta_dict = process_metadata.get_meta_dict()
    spotify_graph.node(meta_dict['track'], meta_dict['track'])
    spotify_graph.node(meta_dict['album'], meta_dict['album'])
    spotify_graph.node(meta_dict['artist'], meta_dict['artist'])

def add_edges_digraph():
    meta_dict = process_metadata.get_meta_dict()
    spotify_graph.edge(meta_dict['track'], meta_dict['album'])
    spotify_graph.edge(meta_dict['album'], meta_dict['track'])
    spotify_graph.edge(meta_dict['track'], meta_dict['artist'])
    spotify_graph.edge(meta_dict['artist'], meta_dict['track'])
    spotify_graph.edge(meta_dict['album'], meta_dict['artist'])
    spotify_graph.edge(meta_dict['artist'], meta_dict['album'])

def updateAndCreateDgraph():
    add_edges_digraph()
    add_nodes_digraph()
    f = open('graph.svg', 'a')
    f.write(spotify_graph.pipe().decode('utf-8'))
    f.close()
