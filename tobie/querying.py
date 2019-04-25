from importlib import reload
from redis_proxy import get_connection
from graph_init import create_graph
from spotify_interface import process_metadata, display_art
from create_nodes import CreateTrackNode, CreateArtistNode, CreateAlbumNode
from create_edges import createAlbumEdge, createTrackEdge, createArtistEdge


def process_result_set(result):
    for subset in result.result_set:
        for item in range(len(subset)):
            subset[item] = subset[item].decode('utf-8')

class queryFacade:
    def __init__(self):
        self.graph = create_graph()
        self.redis_connection = get_connection()

    def get_songs(self):
        query = 'MATCH (track:track) RETURN track.name, track.length, track.uri'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_artists(self):
        query = 'MATCH (artist:artist) RETURN artist.name'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_albums(self):
        query = 'MATCH (album:album) RETURN album.name, album.art_url'
        result = self.graph.query(query)
        process_result_set(result)
        result.pretty_print()

    def get_album_art_url_from_track(self, track_name):
        query = 'MATCH (album:album)-[:containstrack]->(:track {name:"%s"}) RETURN album.art_url' %(track_name)
        result = self.graph.query(query)
        process_result_set(result)
        try:
            subset = result.result_set[-1]
            art_url = subset[0]
            display_art.display_art(art_url)
        except IndexError:
            print("No song found")


class Update:
    def __init__(self):
        self.meta_dict = process_metadata.get_meta_dict()
        print(self.meta_dict)

    def updateTrackNodes(self):
        CreateTrackNode(self.meta_dict).create_track_node()

    def updateArtistNode(self):
        CreateArtistNode(self.meta_dict).create_artist_node()

    def updateAlbumNode(self):
        CreateAlbumNode(self.meta_dict).create_album_node()

    def updateTrackEdges(self):
        createTrackEdge(self.meta_dict).create_artist_edge()
        createTrackEdge(self.meta_dict).create_album_edge()

    def updateArtistEdges(self):
        createArtistEdge(self.meta_dict).create_album_edge()
        createArtistEdge(self.meta_dict).create_track_edge()

    def updateAlbumEdges(self):
        createAlbumEdge(self.meta_dict).create_artist_edge()
        createAlbumEdge(self.meta_dict).create_track_edge()

    def update_all_nodes(self):
        self.updateAlbumNode()
        self.updateArtistNode()
        self.updateTrackNodes()

    def update_all_edges(self):
        self.updateTrackEdges()
        self.updateArtistEdges()
        self.updateAlbumEdges()
        

def help():
    print("Fetch all song metadata - GET songs")
    print("Fetch all album metadata - GET albums")
    print("Fetch all artist metadata - GET artist")
    print("Fetch all <a>, <b> metadata - GET <a> <b>")


def driver_func(inp):
    if inp.strip() == "GET songs":
        queryFacade().get_songs()
    elif inp.strip() == "GET artists":
        queryFacade().get_artists()
    elif inp.strip() == "GET albums":
        queryFacade().get_albums()
    elif inp.strip() == "OPEN album art":
        track_name = input(">>> Enter Track name: ")
        queryFacade().get_album_art_url_from_track(track_name)
    elif inp.strip() == "update":
        update_obj = Update()
        update_obj.update_all_nodes()
        update_obj.update_all_edges()


print("Type help to get information about commands")
print("Type exit to quit")
while True:
    query = input(">>> ")
    if query=="help":
        help()
    elif query=="exit":
        break
    elif query=="update":
        reload(process_metadata)
        driver_func("update")
    else:
        driver_func(query)
