import numpy as np
import matplotlib.pyplot as plt
import laspy


def vis_plt(file_path, batch_size=5000):
    las = laspy.read(file_path)

    points = np.vstack((las.x, las.y, las.z)).transpose()
    colors = np.vstack((las.red, las.green, las.blue)).transpose() / 65535.0  # Normalize colors to [0, 1]

    points = points[::10]
    colors = colors[::10]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

    total_points = len(points)
    displayed_points = 0

    for start_idx in range(0, total_points, batch_size):
        end_idx = min(start_idx + batch_size, total_points)
        displayed_points = end_idx

        ax.scatter(points[start_idx:end_idx, 0], points[start_idx:end_idx, 1], points[start_idx:end_idx, 2],
                   c=colors[start_idx:end_idx], s=0.2)

        if 'counter_text_obj' in locals():
            counter_text_obj.remove()

        counter_text = f'Points displayed: {displayed_points}/{total_points} --- {((end_idx / total_points) * 100):.1f}%"'
        if displayed_points == total_points:
            print('Done!')
        counter_text_obj = ax.text2D(0.05, 0.95, counter_text, transform=ax.transAxes)

        plt.draw()
        plt.pause(0.1)

    plt.show()


vis_plt('USER AREA.las')
