import sys
import copy


class Street:
    def __init__(self, text):
        self.start_intersection, self.end_intersection, self.name, self.time = text.split(' ')
        self.time = int(self.time)
        self.car_number = 0
        self.weight = 0

    def evaluate_streets(self, cars):
        for car in cars:
            if self.name in car.text_streets:
                self.car_number += 1
                self.weight += car.weight


class Intersection:
    def __init__(self, id):
        self.id = id
        self.incoming_streets = []
        self.light_interval = {}

    def add_street(self, street):
        self.incoming_streets.append(street)

    def evaluate_interval(self, streets):
        weight_map = {}

        for incoming_street in self.incoming_streets:
            weight_map[incoming_street] = int(streets[incoming_street].car_number)

        filtered_map = dict(filter(lambda x: x[1] != 0, weight_map.items()))

        lesser = 1

        if len(filtered_map):
            lesser = min(filtered_map.values())

        for k, v in weight_map.items():
            self.light_interval[k] = int(int(v) / (int(lesser))) or 1


class Car:
    def __init__(self, text):
        self.nbr_streets, *self.text_streets = text.split(' ')
        self.weight = 0

    def evaluate_weight(self, streets):
        for text_street in self.text_streets:
            self.weight += streets[text_street].time


def read_file(file_name):
    file = open(file_name, "r")
    lines = [line.rstrip() for line in file.readlines()]
    file.close()

    instructions = lines.pop(0)

    return instructions, lines


def main():
    instructions, lines = read_file(sys.argv[1])

    duration, intersections_number, streets_number, cars_number, score = instructions.split(' ')

    streets = {}
    intersections = {}
    cars = []

    for i in range(0, int(streets_number)):
        line = lines.pop(0)
        line_arr = line.split(' ')

        if not line_arr[1] in intersections.keys():
            intersections[line_arr[1]] = Intersection(line_arr[1])
            intersections[line_arr[1]].add_street(line_arr[2])
        else:
            intersections[line_arr[1]].add_street(line_arr[2])

        street = Street(line)

        streets[street.name] = street

    for i in range(0, int(cars_number)):
        cars.append(Car(lines.pop(0)))

    for car in cars:
        car.evaluate_weight(streets)

    for street in streets.values():
        street.evaluate_streets(cars)

    for intersection in intersections.values():
        intersection.evaluate_interval(streets)

    file = open("result_" + sys.argv[1], "w")

    file.write(str(len(intersections.keys())) + "\n")
    for k, v in intersections.items():
        if not v.light_interval:
            continue
        file.write(v.id + "\n")
        file.write(str(len(v.light_interval.keys())) + "\n")
        for i, j in v.light_interval.items():
            file.write(i + " {0}".format(j) + "\n")

    file.close()


if __name__ == "__main__":
    main()
