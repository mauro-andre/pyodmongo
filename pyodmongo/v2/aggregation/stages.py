from typing import Any, Dict, List, Optional


def match(expression: Dict[str, Any]) -> Dict[str, Any]:
    return {"$match": expression}


def project(expression: Dict[str, Any]) -> Dict[str, Any]:
    return {"$project": expression}


def group(expression: Dict[str, Any]) -> Dict[str, Any]:
    return {"$group": expression}


def sort(expression: Dict[str, Any]) -> Dict[str, Any]:
    return {"$sort": expression}


def limit(n: int) -> Dict[str, Any]:
    return {"$limit": n}


def skip(n: int) -> Dict[str, Any]:
    return {"$skip": n}


def unwind(path: str) -> Dict[str, Any]:
    return {"$unwind": path}


def add_fields(expression: Dict[str, Any]) -> Dict[str, Any]:
    return {"$addFields": expression}


def lookup(
    from_collection: str,
    local_field: Optional[str] = None,
    foreign_field: Optional[str] = None,
    as_field: Optional[str] = None,
    pipeline: Optional[List[Dict[str, Any]]] = None,
    let: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """
    Implements both simple and pipeline forms of $lookup.
    """
    if pipeline is None:
        # Classic/simple form (must have all 3 fields)
        if not (local_field and foreign_field and as_field):
            raise ValueError(
                "local_field, foreign_field, and as_field are required for simple $lookup"
            )
        return {
            "$lookup": {
                "from": from_collection,
                "localField": local_field,
                "foreignField": foreign_field,
                "as": as_field,
            }
        }
    else:
        # Pipeline form, 'as_field' is required
        if not as_field:
            raise ValueError("as_field is required for pipeline $lookup")
        out = {
            "from": from_collection,
            "pipeline": pipeline,
            "as": as_field,
        }
        if let:
            out["let"] = let
        return {"$lookup": out}
