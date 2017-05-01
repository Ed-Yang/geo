import logging

from s2sphere import Cell, CellId, LatLng

log = logging.getLogger(__name__)


def get_cell_ids(lat, long, radius = 10):
    origin = CellId.from_lat_lng(LatLng.from_degrees(float(lat), float(long))).parent(15)
    walk = [origin]
    right = origin.next()
    left = origin.prev()

    # Search around provided radius
    for i in range(radius):
        walk.append(right)
        walk.append(left)
        right = right.next()
        left = left.prev()

    # Return everything
    return sorted(walk)

def getNeighbors(lat, lng):
    origin = CellId.from_lat_lng(LatLng.from_degrees(lat, lng)).parent(15)
    neighbors = {origin}

    edge_neighbors = origin.get_edge_neighbors()
    surrounding_neighbors = [
        edge_neighbors[0],                          # North neighbor
        edge_neighbors[0].get_edge_neighbors()[1],  # North-east neighbor
        edge_neighbors[1],                          # East neighbor
        edge_neighbors[2].get_edge_neighbors()[1],  # South-east neighbor
        edge_neighbors[2],                          # South neighbor
        edge_neighbors[2].get_edge_neighbors()[3],  # South-west neighbor
        edge_neighbors[3],                          # West neighbor
        edge_neighbors[0].get_edge_neighbors()[3],  # North-west neighbor
    ]

    for cell in surrounding_neighbors:
        neighbors.add(cell)
        i = 1
        for cell2 in cell.get_edge_neighbors():
            print i            
            neighbors.add(cell2)
            i = i+1

    return sorted(neighbors)

def printCells(cellList):
    i= 0
    for c in cellList:        
        print "{:2d} ---->LVL: {} ID: {} TKN: {}".format(i+1, c.level(), c.id(), c.to_token())
        i =  i + 1
        
if __name__ == "__main__":
        
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(module)10s] [%(levelname)5s] %(message)s')

    print "google s2 testing"
    location = "24.800114 120.989195"
    pos = map(float, location.split(" "))

    #pos = [24.800114, 120.989195]
    print "get_cell_ids"
    cellIds = get_cell_ids(pos[0], pos[1])
    printCells(cellIds)

    print "getNeighbors"
    neighbors = getNeighbors(pos[0], pos[1])
    printCells(neighbors)