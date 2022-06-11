from typing import Union

from fastapi import APIRouter, Query

from core.response import default_responses, response_404, response_428
from files.flight import flights
from repository.flight import FlightRepo

from .model import MultiFlightResponseModel, NoFlightResponseModel, SingleFlightResponseModel

router = APIRouter(prefix="", tags=['Flight'], responses=default_responses)


@router.get(
    '/',
    response_model=Union[SingleFlightResponseModel, MultiFlightResponseModel, NoFlightResponseModel],
    responses={
        **response_404('airport'),
        **response_428('lack of start or destination')
    }
)
async def flight_route_search(
    _from: str = Query(default=None, alias='from'), to: str = None
) -> Union[SingleFlightResponseModel, MultiFlightResponseModel, NoFlightResponseModel]:
    flight_map, airport_map = FlightRepo.make_flight_and_airport_map(flight_list=flights)
    FlightRepo.check_query_params_are_valid(airport_map=airport_map, start_node=_from, end_node=to)
    flight_routes = FlightRepo.build_flight_routes_between_two_airports(
        airport_map=airport_map, flight_map=flight_map, start_node=_from, end_node=to
    )
    return FlightRepo.convert_flight_routes_to_model(flight_routes=flight_routes)
