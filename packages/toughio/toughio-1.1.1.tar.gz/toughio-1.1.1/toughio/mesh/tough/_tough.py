from __future__ import division, unicode_literals, with_statement

import logging

import numpy

from .._common import meshio_data

__all__ = [
    "read",
    "write",
]


_eos_to_neq = {
    "eos1": 2,
    "eos2": 3,
    "eos3": 3,
    "eos4": 3,
    "eos5": 3,
    "eos7": 3,
    "eos8": 3,
    "eos9": 1,
    "eosmvoc": 4,
    "eoswasg": 4,
    "eco2n": 4,
    "eco2n_v2": 4,
    "eco2m": 4,
}


def block(keyword):
    """
    Decorator for block writing functions.
    """

    def decorator(func):
        from functools import wraps

        header = "----1----*----2----*----3----*----4----*----5----*----6----*----7----*----8"

        @wraps(func)
        def wrapper(f, *args):
            f.write("{}{}\n".format(keyword, header))
            func(f, *args)
            f.write("\n")

        return wrapper

    return decorator


def read(filename):
    """
    Read TOUGH MESH file is not supported yet. MESH file does not store
    any geometrical information except node centers.
    """
    raise NotImplementedError("Reading TOUGH MESH file is not supported.")


def write(filename, mesh, nodal_distance, material_name, material_end, incon_eos):
    """
    Write TOUGH MESH file.
    """
    assert nodal_distance in {"line", "orthogonal"}
    assert material_name is None or isinstance(material_name, dict)
    assert material_end is None or isinstance(material_end, (str, list, tuple))
    assert (
        incon_eos is None or incon_eos in _eos_to_neq.keys()
    ), "EOS '{}' is unknown or not supported.".format(incon_eos)

    # Required variables for blocks ELEME and CONNE
    num_cells = mesh.n_cells
    labels = numpy.concatenate(mesh.labels)
    nodes = numpy.concatenate(mesh.centers)
    materials = numpy.concatenate(mesh.materials)
    volumes = numpy.concatenate(mesh.volumes)
    boundary_conditions = (
        numpy.concatenate(mesh.cell_data["boundary_condition"])
        if "boundary_condition" in mesh.cell_data.keys()
        else numpy.zeros(num_cells, dtype=int)
    )
    points = mesh.points
    connections = numpy.concatenate(mesh.connections)
    gravity = numpy.array([0.0, 0.0, 1.0])

    # Define parameters related to faces
    faces = numpy.concatenate(mesh.faces)
    faces_dict, faces_cell = _get_faces(faces)
    face_normals, face_areas = _get_face_normals_areas(mesh, faces_dict, faces_cell)

    # Required variables for block INCON
    primary_variables = None
    porosities = None
    permeabilities = None
    if incon_eos:
        primary_variables = (
            numpy.concatenate(mesh.cell_data["initial_condition"])
            if "initial_condition" in mesh.cell_data.keys()
            else primary_variables
        )
        porosities = (
            numpy.concatenate(mesh.cell_data["porosity"])
            if "porosity" in mesh.cell_data.keys()
            else porosities
        )
        permeabilities = (
            numpy.concatenate(mesh.cell_data["permeability"])
            if "permeability" in mesh.cell_data.keys()
            else permeabilities
        )

    # Write MESH and INCON files
    write_buffer(
        filename,
        num_cells,
        labels,
        nodes,
        materials,
        volumes,
        boundary_conditions,
        points,
        connections,
        gravity,
        faces,
        face_normals,
        face_areas,
        primary_variables,
        porosities,
        permeabilities,
        nodal_distance,
        material_name,
        material_end,
        incon_eos,
    )


def write_buffer(
    filename,
    num_cells,
    labels,
    nodes,
    materials,
    volumes,
    boundary_conditions,
    points,
    connections,
    gravity,
    faces,
    face_normals,
    face_areas,
    primary_variables,
    porosities,
    permeabilities,
    nodal_distance,
    material_name,
    material_end,
    incon_eos,
):
    material_name = material_name if material_name else {}
    material_end = material_end if material_end else []
    material_end = [material_end] if isinstance(material_end, str) else material_end

    # Check INCON inputs and show warnings if necessary
    if incon_eos and primary_variables is None:
        logging.warning(
            ("Initial conditions are not defined. " "Writing INCON will be ignored.")
        )

    if porosities is not None:
        if not incon_eos:
            logging.warning("Porosity is only exported if incon_eos is provided.")
        else:
            assert (
                len(porosities) == num_cells and porosities.ndim == 1
            ), "Inconsistent porosity array."

    if permeabilities is not None:
        if not incon_eos:
            logging.warning(
                "Permeability modifiers are only exported if incon_eos is provided."
            )
        else:
            assert permeabilities.ndim in {1, 2}
            assert (
                permeabilities.shape == (num_cells, 3)
                if permeabilities.ndim == 2
                else len(permeabilities) == num_cells
            ), "Inconsistent permeability modifiers array."

    # Write MESH file
    with open(filename, "w") as f:
        _write_eleme(
            f,
            labels,
            nodes,
            materials,
            volumes,
            boundary_conditions,
            material_name,
            material_end,
        )
        _write_conne(
            f,
            labels,
            nodes,
            points,
            connections,
            gravity,
            boundary_conditions,
            faces,
            face_normals,
            face_areas,
            nodal_distance,
        )

    # Write INCON file
    if incon_eos and primary_variables is not None:
        import os

        head = os.path.split(filename)[0]
        with open(head + ("/" if head else "") + "INCON", "w") as f:
            _write_incon(
                f, incon_eos, labels, primary_variables, porosities, permeabilities,
            )


@block("ELEME")
def _write_eleme(
    f,
    labels,
    nodes,
    materials,
    volumes,
    boundary_conditions,
    material_name,
    material_end,
):
    """
    Write ELEME block.
    """
    # Apply time-independent Dirichlet boundary conditions
    volumes *= numpy.where(boundary_conditions, 1.0e50, 1.0)

    # Write ELEME block
    fmt = "{:5.5}{:>5}{:>5}{:>5}{:10.4e}{:>10}{:>10}{:10.3e}{:10.3e}{:10.3e}\n"
    ending = []
    iterables = zip(labels, materials, volumes, nodes)
    for label, material, volume, node in iterables:
        mat = material_name[material] if material in material_name.keys() else material
        record = fmt.format(
            label,  # ID
            "",  # NSEQ
            "",  # NADD
            mat,  # MAT
            volume,  # VOLX
            "",  # AHTX
            "",  # PMX
            node[0],  # X
            node[1],  # Y
            node[2],  # Z
        )
        if material not in material_end:
            f.write(record)
        else:
            ending.append(record)

    # Append ending cells at the end of the block
    if material_end:
        for record in ending:
            f.write(record)


@block("CONNE")
def _write_conne(
    f,
    labels,
    nodes,
    points,
    connections,
    gravity,
    boundary_conditions,
    faces,
    face_normals,
    face_areas,
    nodal_distance,
):
    """
    Write CONNE block.
    """
    # Define unique connection variables
    cell_list = set()
    clabels, centers, int_points, int_normals, areas, bounds = [], [], [], [], [], []
    for i, connection in enumerate(connections):
        if (connection >= 0).any():
            for iface, j in enumerate(connection):
                if j >= 0 and j not in cell_list:
                    # Label
                    clabels.append("{:5.5}{:5.5}".format(labels[i], labels[j]))

                    # Nodal points
                    centers.append([nodes[i], nodes[j]])

                    # Common interface defined by single point and normal vector
                    face = faces[i, iface]
                    int_points.append(points[face[face >= 0][0]])
                    int_normals.append(face_normals[i][iface])

                    # Area of common face
                    areas.append(face_areas[i][iface])

                    # Boundary conditions
                    bounds.append((boundary_conditions[i], boundary_conditions[j]))
        else:
            logging.warning(
                "Element '{}' is not connected to the grid.".format(labels[i])
            )
        cell_list.add(i)

    centers = numpy.array(centers)
    int_points = numpy.array(int_points)
    int_normals = numpy.array(int_normals)
    bounds = numpy.array(bounds)

    # Calculate remaining variables not available in itasca module
    lines = numpy.diff(centers, axis=1)[:, 0]
    isot = _isot(lines)
    angles = numpy.dot(lines, gravity) / numpy.linalg.norm(lines, axis=1)

    if nodal_distance == "line":
        fp = _intersection_line_plane(centers[:, 0], lines, int_points, int_normals)
        d1 = numpy.where(
            bounds[:, 0], 1.0e-9, numpy.linalg.norm(centers[:, 0] - fp, axis=1)
        )
        d2 = numpy.where(
            bounds[:, 1], 1.0e-9, numpy.linalg.norm(centers[:, 1] - fp, axis=1)
        )
    elif nodal_distance == "orthogonal":
        d1 = _distance_point_plane(centers[:, 0], int_points, int_normals, bounds[:, 0])
        d2 = _distance_point_plane(centers[:, 1], int_points, int_normals, bounds[:, 1])

    # Write CONNE block
    fmt = "{:10.10}{:>5}{:>5}{:>5}{:>5g}{:10.4e}{:10.4e}{:10.4e}{:10.3e}\n"
    iterables = zip(clabels, isot, d1, d2, areas, angles)
    for label, isot, d1, d2, area, angle in iterables:
        record = fmt.format(
            label,  # ID1-ID2
            "",  # NSEQ
            "",  # NAD1
            "",  # NAD2
            isot,  # ISOT
            d1,  # D1
            d2,  # D2
            area,  # AREAX
            angle,  # BETAX
        )
        f.write(record)


@block("INCON")
def _write_incon(
    f, incon_eos, labels, primary_variables, porosities, permeabilities,
):
    """
    Write INCON block.
    """
    # Check initial pore pressures
    cond = numpy.logical_and(
        primary_variables[:, 0] > -1.0e9, primary_variables[:, 0] < 0.0,
    )
    if cond.any():
        logging.warning("Negative pore pressures found in 'INCON'.")

    # Write label, porosity and permeability
    buffer = ["{:5.5}".format(label) for label in labels]

    if porosities is not None:
        buffer = [
            buf + "{:10}{:15.9e}".format("", phi)
            for buf, phi in zip(buffer, porosities)
        ]
    else:
        buffer = [buf + "{:10}{:15}".format("", "") for buf in buffer]

    if permeabilities is not None:
        if permeabilities.ndim == 1:
            buffer = [
                buf + "{:10.3e}{:10}{:10}".format(k, "", "")
                for buf, k in zip(buffer, permeabilities)
            ]
        else:
            buffer = [
                buf + "{:10.3e}{:10.3e}{:10.3e}".format(*k)
                for buf, k in zip(buffer, permeabilities)
            ]
    else:
        buffer = [buf + "{:10}{:10}{:10}".format("", "", "") for buf in buffer]

    # Write INCON block
    for pvar, buf in zip(primary_variables, buffer):
        if (pvar > -1.0e9).any():
            f.write(buf + "\n")
            for v in pvar:
                f.write("{:20.4e}".format(v) if v > -1.0e9 else "{:20}".format(""))
            f.write("\n")


def _get_faces(faces):
    """
    Return a face dictionary.
    """
    faces_dict = {"triangle": [], "quad": []}
    faces_cell = {"triangle": [], "quad": []}
    numvert_to_face_type = {3: "triangle", 4: "quad"}

    for i, face in enumerate(faces):
        numvert = (face >= 0).sum(axis=-1)
        for f, n in zip(face, numvert):
            if n > 0:
                face_type = numvert_to_face_type[n]
                faces_dict[face_type].append(f[:n])
                faces_cell[face_type].append(i)

    # Stack arrays or remove empty cells
    faces_dict = {
        k: numpy.sort(numpy.vstack(v), axis=1) for k, v in faces_dict.items() if len(v)
    }
    faces_cell = {k: v for k, v in faces_cell.items() if len(v)}

    return faces_dict, faces_cell


def _get_triangle_normals(mesh, faces, islice=[0, 1, 2]):
    """
    Calculate normal vectors of triangular faces.
    """

    def cross(a, b):
        return a[:, [1, 2, 0]] * b[:, [2, 0, 1]] - a[:, [2, 0, 1]] * b[:, [1, 2, 0]]

    triangles = numpy.vstack([c[islice] for c in faces])
    triangles = mesh.points[triangles]

    return cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0])


def _get_face_normals_areas(mesh, faces_dict, faces_cell):
    """
    Calculate face normal vectors and areas.
    """
    # Face normal vectors
    normals = numpy.concatenate(
        [_get_triangle_normals(mesh, v) for k, v in faces_dict.items()]
    )
    normals_mag = numpy.linalg.norm(normals, axis=-1)
    normals /= normals_mag[:, None]

    # Face areas
    areas = numpy.array(normals_mag)
    if len(faces_dict["quad"]):
        tmp = numpy.concatenate(
            [
                _get_triangle_normals(mesh, v, [0, 2, 3])
                if k == "quad"
                else numpy.zeros((len(v), 3))
                for k, v in faces_dict.items()
            ]
        )
        areas += numpy.linalg.norm(tmp, axis=-1)
    areas *= 0.5

    # Reorganize outputs
    face_normals = [[] for _ in range(mesh.n_cells)]
    face_areas = [[] for _ in range(mesh.n_cells)]
    iface = numpy.concatenate([v for v in faces_cell.values()])
    for i, normal, area in zip(iface, normals, areas):
        face_normals[i].append(normal)
        face_areas[i].append(area)

    return face_normals, face_areas


def _intersection_line_plane(center, lines, int_points, int_normals):
    """
    Calculate intersection point between a line defined by a point and a
    direction vector and a plane defined by one point and a normal vector.
    """
    tmp = _dot(int_points - center, int_normals) / _dot(lines, int_normals)
    return center + lines * tmp[:, None]


def _distance_point_plane(center, int_points, int_normals, mask):
    """
    Calculate orthogonal distance of a point to a plane defined by one
    point and a normal vector.
    """
    return numpy.where(mask, 1.0e-9, numpy.abs(_dot(center - int_points, int_normals)))


def _isot(lines):
    """
    Determine anisotropy direction given the direction of the line
    connecting the cell centers.
    Note
    ----
    It always returns 1 if the connection line is not colinear with X, Y or Z.
    """
    mask = lines != 0.0
    return numpy.where(mask.sum(axis=1) == 1, mask.argmax(axis=1) + 1, 1)


def _dot(A, B):
    """
    Custom dot product when arrays A and B have the same shape.
    """
    return (A * B).sum(axis=1)
