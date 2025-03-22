# planet_generator/export.py

import os
from pathlib import Path
from planet_generator import config
from planet_generator.coloring import apply_ocean_coloring


def posterize_color(rgb, levels):
    """Rounds each RGB component to the nearest step in the range [0,1]."""
    step = 1.0 / (levels - 1)
    return tuple(round(c / step) * step for c in rgb)


def rgb_to_mtl_name(rgb):
    """Generates a material name from RGB values."""
    return f"mat_{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}"


def export_obj_and_mtl(vertices, faces, face_colors, ocean_vertices=None, ocean_faces=None):
    """Writes .obj and .mtl files to the configured export directory."""
    export_path = Path(config.export_dir)
    export_path.mkdir(exist_ok=True)

    obj_file = export_path / "planet.obj"
    mtl_file = export_path / "planet.mtl"

    # Posterize face colors to reduce material count
    posterized_colors = [posterize_color(c, config.posterize_levels) for c in face_colors]

    # Generate ocean face colors if ocean mesh is provided
    if ocean_vertices is not None and ocean_faces is not None:
        ocean_colors = apply_ocean_coloring(ocean_vertices, ocean_faces)
        posterized_ocean_colors = [posterize_color(c, config.posterize_levels) for c in ocean_colors]
    else:
        posterized_ocean_colors = []

    # Write MTL file
    unique_colors = {}
    with open(mtl_file, "w") as mtl:
        for color in posterized_colors + posterized_ocean_colors:
            mtl_name = rgb_to_mtl_name(color)
            if mtl_name not in unique_colors:
                unique_colors[mtl_name] = color
                mtl.write(f"newmtl {mtl_name}\n")
                mtl.write(f"Kd {color[0]:.4f} {color[1]:.4f} {color[2]:.4f}\n")
                mtl.write("Ka 0.0000 0.0000 0.0000\n")
                mtl.write("Ks 0.0000 0.0000 0.0000\n\n")

    # Write OBJ file
    with open(obj_file, "w") as obj:
        obj.write(f"mtllib {mtl_file.name}\n")
        for v in vertices:
            if config.convert_to_y_up:
                converted_v = [v[0], v[2], -v[1]]  # Z-up to Y-up
            else:
                converted_v = v
            obj.write(f"v {converted_v[0]:.6f} {converted_v[1]:.6f} {converted_v[2]:.6f}\n")

        last_mtl = None
        for i, tri in enumerate(faces):
            mtl_name = rgb_to_mtl_name(posterized_colors[i])
            if mtl_name != last_mtl:
                obj.write(f"usemtl {mtl_name}\n")
                last_mtl = mtl_name
            obj.write(f"f {tri[0]+1} {tri[1]+1} {tri[2]+1}\n")

        if ocean_vertices is not None and ocean_faces is not None:
            obj.write("o OceanSphere\n")
            v_offset = len(vertices)
            for v in ocean_vertices:
                if config.convert_to_y_up:
                    converted_v = [v[0], v[2], -v[1]]  # Z-up to Y-up
                else:
                    converted_v = v
                obj.write(f"v {converted_v[0]:.6f} {converted_v[1]:.6f} {converted_v[2]:.6f}\n")
            last_mtl = None
            for i, tri in enumerate(ocean_faces):
                mtl_name = rgb_to_mtl_name(posterized_ocean_colors[i])
                if mtl_name != last_mtl:
                    obj.write(f"usemtl {mtl_name}\n")
                    last_mtl = mtl_name
                obj.write(f"f {tri[0]+1+v_offset} {tri[1]+1+v_offset} {tri[2]+1+v_offset}\n")

    print(f"Exported OBJ: {obj_file}")
    print(f"Exported MTL: {mtl_file}")
