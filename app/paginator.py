from math import ceil
from werkzeug.exceptions import abort


def paginate(query, page=None, per_page=None):
    if page < 1:
        abort(404)

    total = query.order_by(None).count()
    per_page = min(per_page, total) if per_page > 0 and total > 0 else 20
    total_pages = int(ceil(total / float(per_page)))
    next_page = page + 1 if page < total_pages else None
    prev_page = page - 1 if page > 1 else None

    items = query.limit(per_page).offset((page - 1) * per_page).all()

    if not items and page != 1:
        abort(404)

    return {
        "page": page,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "per_page": per_page,
        "total": total,
        "items": [i.as_dict() for i in items]
    }
