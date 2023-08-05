# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PlaceGroupDigestAreaRankingResponse(Model):
    """PlaceGroupDigestAreaRankingResponse.

    :param high_cost: Highest cost for this group
    :type high_cost: float
    :param low_cost: Lowest cost for this group
    :type low_cost: float
    :param average_cost: Average cost for this group
    :type average_cost: float
    :param median_cost: Median cost for this group
    :type median_cost: float
    :param high_use: Highest use for this group
    :type high_use: float
    :param low_use: Lowest use for this group
    :type low_use: float
    :param average_use: Average use for this group
    :type average_use: float
    :param median_use: Median use for this group
    :type median_use: float
    :param high_value: Highest benchmark value for this group
    :type high_value: float
    :param low_value: Lowest benchmark value for this group
    :type low_value: float
    :param median_value: Median benchmark value for this group
    :type median_value: float
    :param total_area: Total area for this group
    :type total_area: float
    :param high_area: Highest area for this group
    :type high_area: float
    :param low_area: Lowest area for this group
    :type low_area: float
    :param median_area: Median area for this group
    :type median_area: float
    :param high_savings_opportunity: The highest savings opportunity for this
     group
    :type high_savings_opportunity: float
    :param results:
    :type results:
     list[~energycap.sdk.models.PlaceGroupDigestAreaRankingChild]
    :param place_group_id:
    :type place_group_id: int
    :param place_group_code:
    :type place_group_code: str
    :param place_group_info:
    :type place_group_info: str
    :param place_group_display: This is the user's preferred way of viewing
     this entity - could be code or info based on the master "data object view"
     setting in DB
    :type place_group_display: str
    :param benchmark_unit: This will provide the benchmark unit eg:MMBTU/ft²
     or $/day
    :type benchmark_unit: str
    :param benchmark_factor_unit: This will provide the unit for the
     benchmarking factor eg:ft² or day
    :type benchmark_factor_unit: str
    :param benchmark_value_unit: This will provide the unit for the benchmark
     value eg:$ for cost/day, MMBTU for annualized use/area
    :type benchmark_value_unit: str
    :param use_unit: The use unit of measure
    :type use_unit: ~energycap.sdk.models.UnitChild
    :param cost_unit: The cost unit of measure
    :type cost_unit: ~energycap.sdk.models.UnitChild
    :param updated: The date and time the data was updated
    :type updated: datetime
    """

    _attribute_map = {
        'high_cost': {'key': 'highCost', 'type': 'float'},
        'low_cost': {'key': 'lowCost', 'type': 'float'},
        'average_cost': {'key': 'averageCost', 'type': 'float'},
        'median_cost': {'key': 'medianCost', 'type': 'float'},
        'high_use': {'key': 'highUse', 'type': 'float'},
        'low_use': {'key': 'lowUse', 'type': 'float'},
        'average_use': {'key': 'averageUse', 'type': 'float'},
        'median_use': {'key': 'medianUse', 'type': 'float'},
        'high_value': {'key': 'highValue', 'type': 'float'},
        'low_value': {'key': 'lowValue', 'type': 'float'},
        'median_value': {'key': 'medianValue', 'type': 'float'},
        'total_area': {'key': 'totalArea', 'type': 'float'},
        'high_area': {'key': 'highArea', 'type': 'float'},
        'low_area': {'key': 'lowArea', 'type': 'float'},
        'median_area': {'key': 'medianArea', 'type': 'float'},
        'high_savings_opportunity': {'key': 'highSavingsOpportunity', 'type': 'float'},
        'results': {'key': 'results', 'type': '[PlaceGroupDigestAreaRankingChild]'},
        'place_group_id': {'key': 'placeGroupId', 'type': 'int'},
        'place_group_code': {'key': 'placeGroupCode', 'type': 'str'},
        'place_group_info': {'key': 'placeGroupInfo', 'type': 'str'},
        'place_group_display': {'key': 'placeGroupDisplay', 'type': 'str'},
        'benchmark_unit': {'key': 'benchmarkUnit', 'type': 'str'},
        'benchmark_factor_unit': {'key': 'benchmarkFactorUnit', 'type': 'str'},
        'benchmark_value_unit': {'key': 'benchmarkValueUnit', 'type': 'str'},
        'use_unit': {'key': 'useUnit', 'type': 'UnitChild'},
        'cost_unit': {'key': 'costUnit', 'type': 'UnitChild'},
        'updated': {'key': 'updated', 'type': 'iso-8601'},
    }

    def __init__(self, high_cost=None, low_cost=None, average_cost=None, median_cost=None, high_use=None, low_use=None, average_use=None, median_use=None, high_value=None, low_value=None, median_value=None, total_area=None, high_area=None, low_area=None, median_area=None, high_savings_opportunity=None, results=None, place_group_id=None, place_group_code=None, place_group_info=None, place_group_display=None, benchmark_unit=None, benchmark_factor_unit=None, benchmark_value_unit=None, use_unit=None, cost_unit=None, updated=None):
        super(PlaceGroupDigestAreaRankingResponse, self).__init__()
        self.high_cost = high_cost
        self.low_cost = low_cost
        self.average_cost = average_cost
        self.median_cost = median_cost
        self.high_use = high_use
        self.low_use = low_use
        self.average_use = average_use
        self.median_use = median_use
        self.high_value = high_value
        self.low_value = low_value
        self.median_value = median_value
        self.total_area = total_area
        self.high_area = high_area
        self.low_area = low_area
        self.median_area = median_area
        self.high_savings_opportunity = high_savings_opportunity
        self.results = results
        self.place_group_id = place_group_id
        self.place_group_code = place_group_code
        self.place_group_info = place_group_info
        self.place_group_display = place_group_display
        self.benchmark_unit = benchmark_unit
        self.benchmark_factor_unit = benchmark_factor_unit
        self.benchmark_value_unit = benchmark_value_unit
        self.use_unit = use_unit
        self.cost_unit = cost_unit
        self.updated = updated
