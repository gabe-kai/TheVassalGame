# planet_generator/plot.py

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from planet_generator import config


def draw_planet(vertices, faces, face_colors, qi_pool_coords=None):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1, 1, 1])

    # Draw terrain mesh
    poly_collection = Poly3DCollection(
        vertices[faces],
        alpha=1,
        edgecolor='k' if config.show_edges else None,
        facecolors=face_colors
    )
    ax.add_collection3d(poly_collection)

    # Optional: Qi Pool dots
    if qi_pool_coords is not None:
        ax.scatter(
            qi_pool_coords[:, 0],
            qi_pool_coords[:, 1],
            qi_pool_coords[:, 2],
            color='purple',
            s=10,
            zorder=10
        )

    # Labels & limits
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('Icosphere Planet')

    r_limit = config.radius * 1.2
    ax.set_xlim([-r_limit, r_limit])
    ax.set_ylim([-r_limit, r_limit])
    ax.set_zlim([-r_limit, r_limit])

    plt.tight_layout()
    plt.show()
