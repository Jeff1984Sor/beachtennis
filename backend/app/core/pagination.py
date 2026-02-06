from typing import Iterable


def clamp_limit(limit: int, max_limit: int = 100) -> int:
    return max(1, min(limit, max_limit))


def paginate(query, limit: int, offset: int):
    return query.limit(limit).offset(offset)