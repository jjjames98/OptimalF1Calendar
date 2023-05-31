from geopy import Nominatim
from geopy import distance


def main():
    # Read in circuits from file and convert them to appropriate format
    circuits = read_circuits()
    circuits_gc = get_locations(circuits)

    # Initialise optimal list with first circuit in list (e.g. the starting point)
    optimal = [circuits_gc[0]]
    circuit = circuits_gc[0]
    circuits_gc.remove(circuit)
    for x in range(len(circuits_gc)):
        shortest_dist = 100000
        closest_circuit = ""
        for c in circuits_gc:
            if circuit != c:
                dist = distance.distance((circuit.latitude, circuit.longitude), (c.latitude, c.longitude)).km
                if dist < shortest_dist:
                    # If new shortest distance, set this as the next circuit
                    shortest_dist = dist
                    closest_circuit = c

        # At end of loop, add circuit with the shortest distance from previous circuit as the next circuit
        # and set the next circuit to be compared with the remaining circuits in the list
        optimal.append(closest_circuit)
        circuits_gc.remove(closest_circuit)
        circuit = closest_circuit

    for circuit in optimal:
        print(circuit)

    print("The original distance travelled is " + str(calculate_distance(get_locations(circuits))) + " kms")
    print("The optimal calendar distance travelled is " + str(calculate_distance(optimal)) + " kms")


# Geocode locations given
def get_locations(list):
    geolocator = Nominatim(user_agent="OptimalF1Calendar")
    locations = []
    for circuit in list:
        location = geolocator.geocode(circuit)
        if location is None:
            print(circuit + "cannot be found. Please consider using the closest city/town for this circuit.")
            exit()
        else:
            locations.append(location)
    return locations


# Get distance it would take to travel between each circuit in the list using the order given
def calculate_distance(circuits):
    dist = 0
    for x in range(len(circuits)-1):
        dist += distance.distance(
            (circuits[x].latitude, circuits[x].longitude), (circuits[x+1].latitude, circuits[x+1].longitude)
        ).km
    return dist


# Read the list of circuits, in order, from Circuits.txt
def read_circuits():
    list = []
    f = open("Circuits.txt")
    for circuit in f:
        list.append(circuit)

    f.close()
    return list


if __name__ == '__main__':
    main()
