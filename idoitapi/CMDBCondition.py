from enum import StrEnum
from idoitapi.Request import Request


class ComparisonOperators(StrEnum):
    """
    Available comparison operators for conditions
    """
    EQUAL = "="
    NOT_EQUAL = "!="
    LIKE = "like"
    NOT_LIKE = "not_like"
    GREATER = ">"
    GREATER_OR_EQUAL = ">="
    SMALLER = "<"
    SMALLER_OR_EQUAL = "<="


class ComparisonCondition():
    """
    Helper class to define a condition
    """
    
    def __init__(self, category: str, attribute: str, comparison: ComparisonOperators, value: str):
        self._property = f"{category}-{attribute}"
        self._comparison = comparison
        self._value = value
    
    @property
    def idoit_property(self):
        return self._property
    
    @property
    def comparison(self):
        return self._comparison
    
    @property
    def value(self):
        return self._value
    
    def to_dict(self) -> dict:
        return {
            "property": self._property,
            "comparison": self._comparison.value,
            "value": self._value
        }

class CMDBCondition(Request):
    """
    Requests for API namespace 'cmdb.condition'
    """

    def read(self, conditions: list[ComparisonCondition]):
        """
        Read common informations for the objects, that match the given criteria
        :param conditions: A list of conditions, that the objects should fullfill 
        :return: List with objects meeting the defined conditions.
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        condition_list: list[dict] = []
        for condition in conditions:
            condition_list.append(condition.to_dict())
        return self._api.request(
            'cmdb.condition.read',
            {
                "conditions": condition_list
            }
        )
        