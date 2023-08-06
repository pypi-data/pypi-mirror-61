from functools import partial
from . import Path, PathOp, op

__all__ = [op.name.lower() for op in PathOp]

def _draw(contours):
    path = Path()
    pen = path.getPen()
    for contour in contours:
        contour.draw(pen)
    return path

def union(contours, outpen, fix_winding=True, keep_starting_points=True):
    if not contours:
        return
    path = _draw(contours)
    path.simplify(
        fix_winding=fix_winding,
        keep_starting_points=keep_starting_points
    )
    path.draw(outpen)

def _do(
    operator,
    subject_contours,
    clip_contours,
    outpen,
    fix_winding=True,
    keep_starting_points=True,
):
    one = _draw(subject_contours)
    two = _draw(clip_contours)
    result = op(one, two, operator, fix_winding, keep_starting_points)
    result.draw(outpen)

# generate self-similar operations
for op in PathOp:
    if op == PathOp.UNION: continue
    globals()[op.name.lower()] = partial(_do, op)
