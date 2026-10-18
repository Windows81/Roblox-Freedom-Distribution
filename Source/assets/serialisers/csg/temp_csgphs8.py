'''
Credit to https://github.com/Salenware/HYDROXIDE/blob/136fb36eb204c9dcd3926d040ab2bb2ce1319bad/DEPENDENCIES/Captcha.lua# for writing another implementation of CSGPHS8 that I could copy from.
'''

import math
import struct


def u32(r):
    value = struct.unpack("<I", r['data'][r['at']:][:4])[0]
    r['at'] += 4
    return value


def f32(r):
    value = struct.unpack("<f", r['data'][r['at']:][:4])[0]
    r['at'] += 4
    return value


def vec3(r):
    return (f32(r), f32(r), f32(r))


def readRawHulls(r):
    faceRangeCount = u32(r)
    faceRanges = [0]*faceRangeCount
    for i in range(faceRangeCount):
        faceRanges[i] = u32(r)

    faceValueCount = faceRanges[-1] or 0
    faces = [0]*faceValueCount
    for i in range(faceValueCount):
        faces[i] = u32(r)

    posRangeCount = u32(r)
    posRanges = [0]*posRangeCount
    for i in range(posRangeCount):
        posRanges[i] = u32(r)

    positionValueCount = posRanges[-1] or 0
    positions = []
    for i in range(positionValueCount):
        positions.append(f32(r))

    return faceRanges, faces, posRanges, positions


def bitReader(r, byteCount, bitCount):
    cache, cached = 0, 0
    finish = r['at'] + byteCount

    def result(count):
        nonlocal cache, cached, finish, bitCount
        value = 0
        while count > 0:
            if cached == 0:
                cache = u32(r)
                cached = min(bitCount, 32)
                bitCount -= cached

            take = min(count, cached)
            cached -= take
            value = value * (2**take) + (cache >> cached) % (2**take)
            count -= take
        return value

    return result


def decodeFaces(r, byteCount, bitCount, hullCount, faceCount):
    bits = bitReader(r, byteCount, bitCount)
    adjacency = [-3] * (faceCount * 3)
    indices = [0] * (faceCount * 3)
    faceRanges, posRanges = [0], [0]
    currentFace, vertexOffset = 0, 0

    def nextEdge(edge):
        return math.floor(edge / 3) * 3 + (edge + 1) % 3

    def prevEdge(edge):
        return math.floor(edge / 3) * 3 + (edge + 2) % 3

    def zipBoundary(current):
        while adjacency[current] == -2:
            candidate = nextEdge(current)
            while adjacency[candidate] >= 0:
                candidate = nextEdge(adjacency[candidate])
            if adjacency[candidate] != -1:
                break

            adjacency[current], adjacency[candidate] = candidate, current
            current = prevEdge(current)
            previous = current
            candidatePrevious = prevEdge(candidate)
            indices[prevEdge(current)] = indices[candidatePrevious]

            connected = adjacency[current]
            while connected >= 0 and candidate != previous:
                previous = prevEdge(connected)
                indices[prevEdge(previous)] = indices[candidatePrevious]
                connected = adjacency[previous]
            while adjacency[current] >= 0 and current != candidate:
                current = prevEdge(adjacency[current])

    for _ in range(hullCount):
        firstEdge = currentFace * 3
        adjacency[firstEdge:firstEdge+3] = (-1, -3, -1)
        indices[firstEdge:firstEdge+3] = (0, 1, 2)
        currentFace += 1
        vertexCount = 3

        def decode(cursor):
            nonlocal currentFace, vertexCount, faceRanges, posRanges
            while True:
                edge0 = currentFace * 3
                edge1, edge2 = edge0 + 1, edge0 + 2
                adjacency[edge0], adjacency[edge1], adjacency[edge2] = cursor, -3, -3
                currentFace += 1
                adjacency[cursor] = edge0
                indices[edge1] = indices[prevEdge(cursor)]
                indices[edge2] = indices[nextEdge(cursor)]
                cursor = edge1

                if bits(1) == 0:
                    symbol = 0  # Continue
                else:
                    symbol = bits(2) + 1  # Split, Left, Right, End

                if symbol == 0:
                    indices[edge0] = vertexCount
                    adjacency[nextEdge(cursor)] = -1
                    vertexCount += 1
                elif symbol == 1:
                    decode(cursor)
                    cursor = nextEdge(cursor)
                elif symbol == 2:
                    adjacency[cursor] = -2
                    cursor = nextEdge(cursor)
                elif symbol == 3:
                    next = nextEdge(cursor)
                    adjacency[next] = -2
                    zipBoundary(next)
                else:
                    adjacency[cursor] = -2
                    next = nextEdge(cursor)
                    adjacency[next] = -2
                    zipBoundary(next)
                    return

        decode(firstEdge + 1)
        vertexOffset += vertexCount
        faceRanges.append(currentFace * 3)
        posRanges.append(vertexOffset * 3)

    return faceRanges, indices, posRanges


def appendHulls(output, faceRanges, faces, posRanges, positions):
    for hullIndex in range(1, min(len(faceRanges), len(posRanges))):
        vertices = []
        minX, minY, minZ = +math.inf, +math.inf, +math.inf
        maxX, maxY, maxZ = -math.inf, -math.inf, -math.inf

        for i in range(posRanges[hullIndex - 1], posRanges[hullIndex], 3):
            x, y, z = positions[i + 0], positions[i + 1], positions[i + 2]
            vertices.append(struct.pack('<3f', x, y, z))
            minX, minY, minZ = min(minX, x), min(minY, y), min(minZ, z)
            maxX, maxY, maxZ = max(maxX, x), max(maxY, y), max(maxZ, z)

        triangles = []
        for i in range(faceRanges[hullIndex - 1], faceRanges[hullIndex], 3):
            triangles.append(
                (faces[i+0], faces[i+1], faces[i+2])
            )

        output.append({
            'vertices': vertices,
            'triangles': triangles,
            'center': ((minX + maxX) / 2, (minY + maxY) / 2, (minZ + maxZ) / 2),
            'size': (maxX - minX, maxY - minY, maxZ - minZ),
            'bounds': {
                'min': (minX, minY, minZ),
                'max': (maxX, maxY, maxZ),
            },
        })


def distance2(a, b):
    x, y, z = a[0] - b[0], a[1] - b[1], a[2] - b[2]
    return x * x + y * y + z * z


def makeGroup(hulls, hullIndices):
    group = {
        'hulls': [0]*len(hullIndices),
        'hullIndices': hullIndices,
    }
    minX, minY, minZ = math.inf, math.inf, math.inf
    maxX, maxY, maxZ = -math.inf, -math.inf, -math.inf

    for hullIndex in hullIndices:
        hull = hulls[hullIndex]
        group['hulls'].append(hull)
        minX = min(minX, hull['bounds']['min'][0])
        minY = min(minY, hull['bounds']['min'][1])
        minZ = min(minZ, hull['bounds']['min'][2])
        maxX = max(maxX, hull['bounds']['max'][0])
        maxY = max(maxY, hull['bounds']['max'][1])
        maxZ = max(maxZ, hull['bounds']['max'][2])

    group['bounds'] = {
        'min': (minX, minY, minZ),
        'max': (maxX, maxY, maxZ),
    }
    group['center'] = ((minX + maxX) / 2, (minY + maxY) / 2, (minZ + maxZ) / 2)
    group['size'] = (maxX - minX, maxY - minY, maxZ - minZ)
    return group


def buildConnectedGroups(hulls, epsilon):
    parents = []
    for i in range(len(hulls)):
        parents.append(i)

    def find(index):
        root = index
        while parents[root] != root:
            root = parents[root]
        while parents[index] != index:
            nextIndex = parents[index]
            parents[index] = root
            index = nextIndex
        return root

    def overlaps(a, b):
        return (
            a['bounds']['max'][0] >= b['bounds']['min'][0] - epsilon and
            b['bounds']['max'][0] >= a['bounds']['min'][0] - epsilon and
            a['bounds']['max'][1] >= b['bounds']['min'][1] - epsilon and
            b['bounds']['max'][1] >= a['bounds']['min'][1] - epsilon and
            a['bounds']['max'][2] >= b['bounds']['min'][2] - epsilon and
            b['bounds']['max'][2] >= a['bounds']['min'][2] - epsilon
        )

    for i in range(len(hulls)-1):
        for j in range(i + 1,  len(hulls)):
            if overlaps(hulls[i], hulls[j]):
                rootI, rootJ = find(i), find(j)
                if rootI != rootJ:
                    parents[rootJ] = rootI

    componentsByRoot = {}
    components = []
    for i in range(len(hulls)):
        root = find(i)
        indices = componentsByRoot.get(root)
        if indices is None:
            indices = []
            componentsByRoot[root] = indices
            components.append(indices)
        indices.append(i)

    groups = []
    for i, indices in enumerate(components):
        groups.append(makeGroup(hulls, indices))
    return groups


def mergeExtraGroups(hulls, groups):
    groups.sort(key=lambda x: -x['hullIndices'])
    assignments = [[], []]
    for hullIndex in groups[0].hullIndices:
        assignments[0].append(hullIndex)
    for hullIndex in groups[1].hullIndices:
        assignments[1].append(hullIndex)

    centers = [groups[0]['center'], groups[1]['center']]
    for i in range(2, len(groups)):
        target = (
            0
            if distance2(groups[i]['center'], centers[0]) <= distance2(groups[i]['center'], centers[1])
            else 1
        )
        for hullIndex in groups[i].hullIndices:
            assignments[target].append(hullIndex)
    return [
        makeGroup(hulls, assignments[0]),
        makeGroup(hulls, assignments[1]),
    ]


def kMeansFallback(hulls):
    farthestA, farthestB, farthestDistance = 1, 2, -1
    for i in range(len(hulls)-1):
        for j in range(i + 1,  len(hulls)):
            distance = distance2(hulls[i]['center'], hulls[j]['center'])
            if distance > farthestDistance:
                farthestA, farthestB, farthestDistance = i, j, distance

    centers = [hulls[farthestA]['center'], hulls[farthestB]['center']]
    assignments = [0] * len(hulls)
    for _ in range(50):
        changed = False
        sums = [
            {'x': 0, 'y': 0, 'z': 0, 'count': 0},
            {'x': 0, 'y': 0, 'z': 0, 'count': 0},
        ]
        for i, hull in enumerate(hulls):
            target = (
                0
                if distance2(hull['center'], centers[0]) <= distance2(hull['center'], centers[1])
                else 1
            )
            if assignments[i] != target:
                assignments[i], changed = target, True
            sum = sums[target]
            sum['x'] += hull['center'][0]
            sum['y'] += hull['center'][1]
            sum['z'] += hull['center'][2]
            sum['count'] += 1
        for i, sum in enumerate(sums):
            if sum['count'] > 0:
                centers[i] = (
                    sum['x'] / sum['count'],
                    sum['y'] / sum['count'],
                    sum['z'] / sum['count'],
                )
        if not changed:
            break

    indices = [[], []]
    for i, target in enumerate(assignments):
        indices[target].append(i)
    return [
        makeGroup(hulls, indices[0]),
        makeGroup(hulls, indices[1]),
    ]


def separateHulls(hulls):
    for epsilon in {0.001, 0.0001, 0}:
        groups = buildConnectedGroups(hulls, epsilon)
        if len(groups) == 2:
            return groups
        elif len(groups) > 2:
            return mergeExtraGroups(hulls, groups)

    return kMeansFallback(hulls)


def decodePayload(payload, geomType):
    r = {'data': payload, 'at': 0}
    hullCount, positionCount, faceCount = u32(r), u32(r), u32(r)
    u32(r)  # first hull position count
    u32(r)  # first hull face count
    rawLength = u32(r)
    clersBitCount, clersLength = u32(r), u32(r)
    u32(r)  # positions byte length
    bounds = {'min': vec3(r), 'max': vec3(r)}

    rawFaceRanges, rawFaces, rawPosRanges, rawPositions = None, None, None, None
    if rawLength != 0:
        rawFaceRanges, rawFaces, rawPosRanges, rawPositions = readRawHulls(r)

    clersAt = r['at']
    r['at'] += clersLength
    positionValueCount = positionCount * 3
    positions = []
    for i in range(positionValueCount):
        positions.append(f32(r))

    faceRanges, faces, posRanges = decodeFaces(
        {'data': payload, 'at': clersAt}, clersLength, clersBitCount, hullCount, faceCount)

    hulls = []
    if rawFaceRanges:
        appendHulls(hulls, rawFaceRanges, rawFaces, rawPosRanges, rawPositions)
    rawHullCount = len(hulls)
    appendHulls(hulls, faceRanges, faces, posRanges, positions)
    groups = separateHulls(hulls)

    return {
        'version': 8,
        'geomType': geomType,
        'bounds': bounds,
        'rawHullCount': rawHullCount,
        'hulls': hulls,
        'groups': groups,
        'models': groups,
    }
