import numpy as np

from superverse.geometry.core import Point


def get_polygon_center(polygon: np.ndarray) -> Point:
    """
    Calculate the center of a polygon. The center is calculated as the center
    of the solid figure formed by the points of the polygon

    Parameters:
        polygon (np.ndarray): A 2-dimensional numpy ndarray representing the
            vertices of the polygon.

    Returns:
        Point: The center of the polygon, represented as a
            Point object with x and y attributes.

    Raises:
        ValueError: If the polygon has no vertices.

    Examples:
        ```python
        import numpy as np
        import superverse as sv

        polygon = np.array([[0, 0], [0, 2], [2, 2], [2, 0]])
        sv.get_polygon_center(polygon=polygon)
        # Point(x=1, y=1)
        ```
    """

    # This is one of the 3 candidate algorithms considered for centroid calculation.
    # For a more detailed discussion, see PR #1084 and commit eb33176

    if len(polygon) == 0:
        raise ValueError("Polygon must have at least one vertex.")

    shift_polygon = np.roll(polygon, -1, axis=0)
    signed_areas = np.cross(polygon, shift_polygon) / 2
    if signed_areas.sum() == 0:
        center = np.mean(polygon, axis=0).round()
        return Point(x=center[0], y=center[1])
    centroids = (polygon + shift_polygon) / 3.0
    center = np.average(centroids, axis=0, weights=signed_areas).round()

    return Point(x=center[0], y=center[1])
