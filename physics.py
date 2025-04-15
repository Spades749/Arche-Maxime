from maths_utils import somme_vect, prod_vect_scal, vect

def translation(m, F, G, vG, h):
    SF = [0, 0, 0]
    for force in F:
        SF = somme_vect(SF, force[0])
    aG = prod_vect_scal(SF, 1/m)
    newG = somme_vect(G, prod_vect_scal(vG, h))
    newvG = somme_vect(vG, prod_vect_scal(aG, h))
    return newG, newvG

def translate(W, G, newG):
    W_new = []
    GnewG = vect(G, newG)
    for i in range(len(W[0])):
        W_new.append(somme_vect([W[0][i], W[1][i], W[2][i]], GnewG))
    return [ [p[i] for p in W_new] for i in range(3) ]
