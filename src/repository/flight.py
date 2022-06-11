from collections import defaultdict

from apps.flight.model import MultiFlightResponseModel, NoFlightResponseModel, RetrieveFlightModel, \
    SingleFlightResponseModel
from core.exception import EmptyQueryParamsException, ResourceNotFoundException


class FlightRepo:

    @staticmethod
    def make_flight_and_airport_map(flight_list: list[dict]):
        airport_map: dict[str, int] = defaultdict()
        _key = 0
        for flight in flight_list:
            if flight['from'] not in airport_map.keys():
                airport_map[flight['from']] = _key
                _key += 1
            if flight['to'] not in airport_map.keys():
                airport_map[flight['to']] = _key
                _key += 1

        flight_map = [['' for i in range(len(airport_map))] for j in range(len(airport_map))]

        for flight in flight_list:
            flight_map[airport_map[flight['from']]][airport_map[flight['to']]] = flight['id']
        return flight_map, airport_map

    @staticmethod
    def convert_flights_to_return_model(_id: str, _from: str, _to: str):
        return RetrieveFlightModel(**{'id': _id, 'from': _from, 'to': _to})

    @staticmethod
    def check_query_params_are_valid(airport_map: dict[str, int], start_node: str, end_node: str):
        if not start_node or not end_node:
            raise EmptyQueryParamsException('both start airport and destination airport are required')

        if airport_map.get(start_node, None) == None:
            raise ResourceNotFoundException(f'start {start_node} airport not found')

        if airport_map.get(end_node, None) == None:
            raise ResourceNotFoundException(f'destination {end_node} airport not found')

    @staticmethod
    def convert_flight_routes_to_model(flight_routes: list[RetrieveFlightModel]):
        if len(flight_routes) == 0:
            return NoFlightResponseModel()
        elif len(flight_routes) == 1:
            return SingleFlightResponseModel(single_direct_flight=flight_routes)
        else:
            return MultiFlightResponseModel(multi_leg_flight=flight_routes)

    @staticmethod
    def build_flight_routes_between_two_airports(
        airport_map: dict[str, int], flight_map: list[list], start_node: str, end_node: str
    ):
        queue, visited = [], set()
        head, tail, stop = 0, 1, False

        queue.append({'airport': start_node, 'routes': []})
        visited.add(start_node)

        while head < tail:
            transfer_node = queue[head]['airport']
            for next_node, next_node_id in airport_map.items():
                route = queue[head]['routes'].copy()
                if flight_map[airport_map[transfer_node]][next_node_id] != '' and next_node not in visited:
                    route.append(
                        FlightRepo.convert_flights_to_return_model(
                            _id=flight_map[airport_map[transfer_node]][next_node_id],
                            _from=transfer_node,
                            _to=next_node
                        )
                    )
                    queue.append({'airport': next_node, 'routes': route})
                    tail += 1
                    visited.add(next_node)

                if queue[tail - 1]['airport'] == end_node:
                    stop = True
                    break

            if stop == True:
                break
            head += 1

        return queue[tail - 1]['routes']
