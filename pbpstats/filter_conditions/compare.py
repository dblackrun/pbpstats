from enum import Enum


class ComparisonType(str, Enum):
    equals = "eq"
    gte = "gte"  # greater than or equal to
    lte = "lte"  # less than or equal to
    gt = "gt"  # greater than
    lt = "lt"  # less than


def meets_comparision_conditions(
    comparison_type: ComparisonType, comparison_value: int, value_to_compare: int
) -> bool:
    if comparison_type == ComparisonType.equals:
        return value_to_compare == comparison_value
    elif comparison_type == ComparisonType.gte:
        return value_to_compare >= comparison_value
    elif comparison_type == ComparisonType.lte:
        return value_to_compare <= comparison_value
    elif comparison_type == ComparisonType.gt:
        return value_to_compare > comparison_value
    elif comparison_type == ComparisonType.lt:
        return value_to_compare < comparison_value
    return False
