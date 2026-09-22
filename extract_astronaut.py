import struct, json, random

COMPONENT_TYPES = {
    5120: ('b', 1),  # BYTE
    5121: ('B', 1),  # UNSIGNED_BYTE
    5122: ('h', 2),  # SHORT
    5123: ('H', 2),  # UNSIGNED_SHORT
    5125: ('I', 4),  # UNSIGNED_INT
    5126: ('f', 4),  # FLOAT
}
TYPE_COUNTS = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4, 'MAT4': 16}


def load_glb(path):
    with open(path, 'rb') as f:
        data = f.read()
    offset = 12
    chunk_len, chunk_type = struct.unpack('<I4s', data[offset:offset + 8])
    assert chunk_type == b'JSON'
    gltf = json.loads(data[offset + 8:offset + 8 + chunk_len])
    offset += 8 + chunk_len
    chunk_len, chunk_type = struct.unpack('<I4s', data[offset:offset + 8])
    assert chunk_type == b'BIN\x00'
    bin_data = data[offset + 8:offset + 8 + chunk_len]
    return gltf, bin_data


def read_accessor(gltf, bin_data, accessor_index):
    acc = gltf['accessors'][accessor_index]
    bv = gltf['bufferViews'][acc['bufferView']]
    comp_fmt, comp_size = COMPONENT_TYPES[acc['componentType']]
    n_comp = TYPE_COUNTS[acc['type']]
    count = acc['count']
    elem_size = comp_size * n_comp
    stride = bv.get('byteStride', elem_size)
    base = bv.get('byteOffset', 0) + acc.get('byteOffset', 0)
    out = []
    for i in range(count):
        start = base + i * stride
        vals = struct.unpack_from('<' + comp_fmt * n_comp, bin_data, start)
        out.append(vals if n_comp > 1 else vals[0])
    return out


def extract(path, target_total_edges=650, seed=11):
    gltf, bin_data = load_glb(path)
    r = random.Random(seed)

    per_mesh = []  # (verts:list[(x,y,z)], edges:list[(i,j)])
    total_raw_edges = 0
    for mesh in gltf['meshes']:
        prim = mesh['primitives'][0]
        if 'POSITION' not in prim['attributes'] or 'indices' not in prim:
            continue
        verts = read_accessor(gltf, bin_data, prim['attributes']['POSITION'])
        indices = read_accessor(gltf, bin_data, prim['indices'])
        edge_set = set()
        for t in range(0, len(indices) - 2, 3):
            a, b, cc = indices[t], indices[t + 1], indices[t + 2]
            for u, v in ((a, b), (b, cc), (cc, a)):
                key = (u, v) if u < v else (v, u)
                edge_set.add(key)
        edges = list(edge_set)
        per_mesh.append((mesh.get('name', ''), verts, edges))
        total_raw_edges += len(edges)

    # proportional downsample per mesh to hit the target total
    combined_verts = []
    combined_edges = []
    for name, verts, edges in per_mesh:
        frac = target_total_edges / max(total_raw_edges, 1)
        keep_n = max(4, int(len(edges) * frac))
        keep_n = min(keep_n, len(edges))
        sampled = edges if keep_n >= len(edges) else r.sample(edges, keep_n)

        remap = {}
        for (a, b) in sampled:
            for idx in (a, b):
                if idx not in remap:
                    remap[idx] = len(combined_verts)
                    combined_verts.append(verts[idx])
            combined_edges.append((remap[a], remap[b]))

    # normalize: centroid at origin, scale to fit a unit-ish sphere (max radius ~1)
    n = len(combined_verts)
    cx = sum(v[0] for v in combined_verts) / n
    cy = sum(v[1] for v in combined_verts) / n
    cz = sum(v[2] for v in combined_verts) / n
    centered = [(x - cx, y - cy, z - cz) for x, y, z in combined_verts]
    max_r = max((x * x + y * y + z * z) ** 0.5 for x, y, z in centered)
    norm = [(x / max_r, y / max_r, z / max_r) for x, y, z in centered]

    return norm, combined_edges


if __name__ == '__main__':
    verts, edges = extract('/mnt/user-data/uploads/horror_game_astronaut.glb')
    print('vertices:', len(verts), 'edges:', len(edges))
    with open('/home/claude/astronaut/astronaut_mesh.json', 'w') as f:
        json.dump({'verts': verts, 'edges': edges}, f)
    print('wrote astronaut_mesh.json')
