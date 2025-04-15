from maxim import ArcheMaxim

if __name__ == "__main__":
    arche = ArcheMaxim()
    force_propulsion = [[[0, 0, 200], [0, 0, -3]]]
    h = 0.5
    n = 10

    for i in range(n):
        print(f"Step {i+1}")
        arche.afficher()
        arche.step(force_propulsion, h)
