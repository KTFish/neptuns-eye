import matplotlib.pyplot as plt

def visualize_predictions(las, predictions):
    x, y, z = las.x, las.y, las.z

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(x, y, z, c=predictions, cmap='viridis', marker='.')

    legend1 = ax.legend(*scatter.legend_elements(), title="Classes")
    ax.add_artist(legend1)
    ax.set_title('3D Visualization of Predictions')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.savefig('point_cloud_n5.png')
    # plt.show()
