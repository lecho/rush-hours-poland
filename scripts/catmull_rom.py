import numpy

def interpolateCatmulRomeSegment(P0, P1, P2, P3, nPoints=20):
    """
    P0, P1, P2, and P3 should be (x,y) point pairs that define the Catmull-Rom spline.
    nPoints is the number of points to include in this curve segment.
    """
    # Convert the points to numpy so that we can do array multiplication
    P0, P1, P2, P3 = map(numpy.array, [P0, P1, P2, P3])

    # Calculate t0 to t4
    t0 = 0
    t1 = calculateT(t0, P0, P1)
    t2 = calculateT(t1, P1, P2)
    t3 = calculateT(t2, P2, P3)

    # Only calculate points between P1 and P2
    t = numpy.linspace(t1,t2,nPoints)

    # Reshape so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    t = t.reshape(len(t),1)

    A1 = (t1-t)/(t1-t0)*P0 + (t-t0)/(t1-t0)*P1
    A2 = (t2-t)/(t2-t1)*P1 + (t-t1)/(t2-t1)*P2
    A3 = (t3-t)/(t3-t2)*P2 + (t-t2)/(t3-t2)*P3

    B1 = (t2-t)/(t2-t0)*A1 + (t-t0)/(t2-t0)*A2
    B2 = (t3-t)/(t3-t1)*A2 + (t-t1)/(t3-t1)*A3

    curve  = (t2-t)/(t2-t1)*B1 + (t-t1)/(t2-t1)*B2
    # Convert list of numpy arrays to list of tuples
    return list(map(tuple, curve))

def calculateT(ti, Pi, Pj, alpha=0.5):
    xi, yi = Pi
    xj, yj = Pj
    return ( ( (xj-xi)**2 + (yj-yi)**2 )**0.5 )**alpha + ti

def interpolateCatmulRomeSpline(points):
    """
    Calculate Catmull Rom for a chain of points and return the combined curve.
    """
    pointsLen = len(points)

    # The curve curve(C) will contain an array of (x,y) points.
    curve = []
    for i in range(pointsLen-3):
        segment = interpolateCatmulRomeSegment(points[i], points[i+1], points[i+2], points[i+3])
        curve.extend(segment)

    return curve