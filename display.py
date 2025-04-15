import matplotlib.pyplot as plt

def afficher(W):
    X, Y, Z = W
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 50])
    ax.scatter3D(X, Y, Z, c=Z, cmap='plasma')
    plt.show()
