from pydantic import BaseModel, Field


class RetrieveFlightModel(BaseModel):
    id_: str = Field(alias='id')
    from_: str = Field(alias='from')
    to_: str = Field(alias='to')


class SingleFlightResponseModel(BaseModel):
    single_direct_flight: list[RetrieveFlightModel]


class MultiFlightResponseModel(BaseModel):
    multi_leg_flight: list[RetrieveFlightModel]


class NoFlightResponseModel(BaseModel):
    no_flight_path: list[RetrieveFlightModel] = Field(default_factory=list)
