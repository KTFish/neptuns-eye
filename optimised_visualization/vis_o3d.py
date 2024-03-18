import numpy as np
import laspy
import open3d as o3d


def vis_o3d(file_path, batch_size=10000):
    las = laspy.read(file_path)

    points = np.vstack((las.x, las.y, las.z)).transpose()
    colors = np.vstack((las.red, las.green, las.blue)).transpose() / 65535.0

    pcd = o3d.geometry.PointCloud()

    vis = o3d.visualization.Visualizer()
    vis.create_window()

    total_points = len(points)
    for start_idx in range(0, total_points, batch_size):
        end_idx = min(start_idx + batch_size, total_points)

        new_points = o3d.utility.Vector3dVector(points[start_idx:end_idx])
        new_colors = o3d.utility.Vector3dVector(colors[start_idx:end_idx])
        if start_idx == 0:
            pcd.points = new_points
            pcd.colors = new_colors
            vis.add_geometry(pcd)
        else:
            pcd.points = o3d.utility.Vector3dVector(np.vstack((np.asarray(pcd.points), np.asarray(new_points))))
            pcd.colors = o3d.utility.Vector3dVector(np.vstack((np.asarray(pcd.colors), np.asarray(new_colors))))
            vis.update_geometry(pcd)

        vis.update_renderer()
        vis.poll_events()

        print(f'Points displayed: {end_idx}/{total_points} --- {((end_idx / total_points) * 100):.1f}%')
        if end_idx == total_points:
            print('Done!')

    vis.run()


vis_o3d('USER AREA.las')
