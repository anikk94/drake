#!/usr/bin/env python3
"""
Filter a VTK Unstructured Grid file to keep only tetrahedral cells (CELL_TYPE 10).
Usage:
  python3 filter_vtk_keep_tets.py input.vtk output_only_tets.vtk
"""
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: filter_vtk_keep_tets.py input.vtk output.vtk")
        sys.exit(1)
    inp, outp = sys.argv[1], sys.argv[2]
    with open(inp, 'r') as f:
        lines = f.readlines()
    # find CELLS and CELL_TYPES headers
    cells_idx = None
    cell_types_idx = None
    for i, ln in enumerate(lines):
        if ln.startswith('CELLS '):
            cells_idx = i
        if ln.startswith('CELL_TYPES '):
            cell_types_idx = i
            break
    if cells_idx is None or cell_types_idx is None:
        print('Could not find CELLS or CELL_TYPES in file')
        sys.exit(2)
    header = lines[:cells_idx]
    cells_header = lines[cells_idx].strip()
    # parse cell lines
    cell_lines = lines[cells_idx+1:cell_types_idx]
    # parse cell types
    cell_types_header = lines[cell_types_idx].strip()
    types_lines = lines[cell_types_idx+1:]
    # convert types to ints until we exhaust the number declared
    # read declared number from header
    try:
        declared_cells = int(cells_header.split()[1])
    except Exception:
        declared_cells = None
    try:
        declared_types = int(cell_types_header.split()[1])
    except Exception:
        declared_types = None
    # Trim types_lines to declared_types if present
    if declared_types is not None:
        types = [int(x.strip()) for x in types_lines[:declared_types]]
        tail_lines = types_lines[declared_types:]
    else:
        types = [int(x.strip()) for x in types_lines]
        tail_lines = []
    if declared_cells is not None and len(cell_lines) > declared_cells:
        cell_lines = cell_lines[:declared_cells]
    # Keep only tetrahedra (type 10)
    keep_indices = [i for i,t in enumerate(types) if t == 10]
    kept_cells = [cell_lines[i] for i in keep_indices]
    # compute new CELLS header: number of kept cells and total ints = sum(1 + npts)
    total_ints = 0
    for cl in kept_cells:
        parts = cl.strip().split()
        if len(parts) == 0:
            continue
        # first number is number of points
        npts = int(parts[0])
        total_ints += 1 + npts
    new_cells_header = f"CELLS {len(kept_cells)} {total_ints}\n"
    # new cell types header
    new_cell_types_header = f"CELL_TYPES {len(keep_indices)}\n"
    # write output
    with open(outp, 'w') as f:
        f.writelines(header)
        f.write(new_cells_header)
        f.writelines(kept_cells)
        f.write(new_cell_types_header)
        for _ in keep_indices:
            f.write('10\n')
        # write remaining tail lines (if any) e.g., POINT_DATA or other fields
        f.writelines(tail_lines)
    print(f'Wrote {outp}: kept {len(kept_cells)} tetrahedral cells')

if __name__ == '__main__':
    main()
