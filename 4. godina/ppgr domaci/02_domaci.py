# -*- coding: utf-8 -*-
"""ppgr_domaci2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CCavpAUpxhJQxjubxL2ab93HFNIS72Au

Dodatno: \\
4') (do 8 bodova) Napisati funkciju koja učitava dve fotografije i od njih pravi panoramu. Korisnik identifikuje određen broj  (>= 4) tačaka  koje su "iste" na obe fotografije i na osnovu toga se računa projektivno preslikavanje koje "lepi" fotografije. Alternativno, može se koristiti SIFT biblioteka za odredjivanje tačaka. Implementacija RANSAC algoritma, ko želi.
"""

import numpy as np
import matplotlib.pyplot as plt

def draw(src_p, dst_p):
    xs = [p[0] for p in src_p]
    ys = [p[1] for p in src_p]
    xs.append(src_p[0][0])
    ys.append(src_p[0][1])

    xd = [p[0] for p in dst_p]
    yd = [p[1] for p in dst_p]
    xd.append(dst_p[0][0])
    yd.append(dst_p[0][1])

    plt.plot(xs, ys)
    plt.plot(xd, yd)
    plt.legend(['original', 'slika'])
    plt.show()

# originalne tacke
src_points = [[1, 1, 1],
              [5, 2, 1],
              [6, 4, 1],
              [-1, 7, 1]]

# slike tacaka
dst_points = [[0, 0, 1],
              [10, 0, 1],
              [10, 5, 1],
              [0, 5, 1]]

# Graficki prikaz
draw(src_points, dst_points)

"""***1. NAIVNI ALGORITAM***"""

def find_matrix(pts):
    matrix = np.array([ # A, B, C
        [pts[0][0], pts[1][0], pts[2][0]],
        [pts[0][1], pts[1][1], pts[2][1]],
        [pts[0][2], pts[1][2], pts[2][2]]
    ])

    D = np.array([pts[3][0], pts[3][1], pts[3][2]])

    # D = alpha*A + beta*B + gamma*C
    result = np.linalg.solve(matrix, D)

    alpha = result[0]
    beta = result[1]
    gamma = result[2]

    column1= np.array([alpha*pts[0][0], alpha*pts[0][1], alpha*pts[0][2]])
    column2= np.array([beta*pts[1][0], beta*pts[1][1], beta*pts[1][2]])
    column3= np.array([gamma*pts[2][0], gamma*pts[2][1], gamma*pts[2][2]])

    P = np.column_stack([column1, column2, column3])

    return P

def naive_algorithm(src_p, dst_p):

    P1 = find_matrix(src_p)
    P2 = find_matrix(dst_p)

    # P = P2*inv(P1)
    P = np.dot(P2, np.linalg.inv(P1))

    return P

# Matrica projektivnog preslikavanja
P_naive = naive_algorithm(src_points, dst_points)
P_naive = P_naive.round(5)
print(P_naive)

# Za DLT i modifikovani DLT (vise od 4 korespodencije)

# originalne tacke
src_points = [[-3, -1, 1],
              [3, -1, 1],
              [1, 1, 1],
              [-1, 1, 1],
              [1, 2, 3],
              [-8, -2, 1]]

# slike tacaka
dst_points = [[-2, -1, 1],
              [2, -1, 1],
              [2, 1, 1],
              [-2, 1, 1],
              [2, 1, 4],
              [-16, -5, 4]]

# draw(src_points, dst_points)

"""***2. DLT ALGORITAM***"""

def dlt(src_p, dst_p):
    x = src_p[0][0]
    y = src_p[0][1]
    z = src_p[0][2]

    u = dst_p[0][0]
    v = dst_p[0][1]
    w = dst_p[0][2]

    A = np.array([
        [0, 0, 0, -w*x, -w*y, -w*z, v*x, v*y, v*z],
        [w*x, w*y, w*z, 0, 0, 0, -u*x, -u*y, -u*z]
    ])

    for i in range(1, len(src_p)):
        x = src_p[i][0]
        y = src_p[i][1]
        z = src_p[i][2]

        u = dst_p[i][0]
        v = dst_p[i][1]
        w = dst_p[i][2]

        row1 = np.array([0, 0, 0, -w*x, -w*y, -w*z, v*x, v*y, v*z])
        row2 = np.array([w*x, w*y, w*z, 0, 0, 0, -u*x, -u*y, -u*z])

        A = np.vstack((A, row1))
        A = np.vstack((A, row2))

    # print(A.shape)
    # print(A)

    # SVD dekompozicija
    U, S, V = np.linalg.svd(A)

    P = V[-1].reshape(3,3)
    
    return P

P_dlt = dlt(src_points, dst_points)
print(P_dlt.round(5))

"""***Poredjenje DLT i naivnog algoritma***"""

P_dlt = (P_dlt / P_dlt[0, 0]) * P_naive[0,0]
print(P_dlt.round(5))

P_dlt.round(5) == P_naive.round(5)

"""***3. MODIFIKOVANI DLT ALGORITAM***"""

import math

def normalization(src_p):
    
    # teziste sistema tacaka C(x, y)
    x = sum([p[0]/p[2] for p in src_p]) / len(src_p)
    y = sum([p[1]/p[2] for p in src_p]) / len(src_p)
    
    # srednje rastojanje
    r = 0.0

    for i in range(len(src_p)):
        # translacija u koordinatni pocetak
        tmp1 = float(src_p[i][0]/src_p[i][2]) - x
        tmp2 = float(src_p[i][1]/src_p[i][2]) - y

        r = r + math.sqrt(tmp1**2 + tmp2**2)

    r = r / float(len(src_p))

    # skaliranje
    S = float(math.sqrt(2)) / r

    # vracamo matricu normalizacije 
    return np.array([[S, 0, -S*x], [0, S, -S*y], [0, 0, 1]])

def dlt_normalized(src_p, dst_p):

    # transformacije
    T = normalization(src_p)
    T_prim = normalization(dst_p)

    # normalizovane tacke
    M_line = T.dot(np.transpose(src_p))
    M_prim = T_prim.dot(np.transpose(dst_p))

    M_line = np.transpose(M_line)
    M_prim = np.transpose(M_prim)

    P_line = dlt(M_line, M_prim)

    P = (np.linalg.inv(T_prim)).dot(P_line).dot(T)

    return P

P_dlt_norm = dlt_normalized(src_points, dst_points)
print(P_dlt_norm.round(5))

"""***Poredjenje DLT i modifikovanog DLT algoritma***"""

P_dlt_norm = (P_dlt_norm / P_dlt_norm[0, 0]) * P_dlt[0,0]
print(P_dlt_norm.round(5))

P_dlt_norm.round(5) == P_dlt.round(5)

"""***4. UKLANJANJE PROJEKTIVNE DISTORZIJE***"""

from PIL import Image

img = Image.open('building.jpeg')
img_copy = Image.new('RGB', (img.size[0], img.size[1]), 'black')

def change_photo(src_p, dst_p):
    # P = naive_algorithm(src_p, dst_p)
    # P = dlt(src_p, dst_p)
    P = dlt_normalized(src_p, dst_p)

    P = np.linalg.inv(P)
    cols = img_copy.size[0]
    rows = img_copy.size[1]

    for i in range(cols):        
        for j in range(rows):      
            new_coord = P.dot([i, j, 1]) 
            new_coord = [(x / new_coord[2]) for x in new_coord]
            
            if (new_coord[0] >= 0 and new_coord[0] < cols-1 and new_coord[1] >= 0 and new_coord[1] < rows-1):
                tmp1 = img.getpixel((math.floor(new_coord[0]), math.floor(new_coord[1])))
                tmp2 = img.getpixel((math.ceil(new_coord[0]), math.ceil(new_coord[1])))
                img_copy.putpixel((i, j), tmp2)
        

    fig = plt.figure(figsize=(16, 9))

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title('Pocetna slika:')

    plt.subplot(1, 2, 2)
    plt.imshow(img_copy)
    plt.title('Uklanjanje distorzije:')

    plt.tight_layout()
    plt.show()

# tacke sa originalne slike (building.jpeg)
src_points = [[164, 717, 1],
              [294, 744, 1],
              [293, 147, 1],
              [214, 30, 1]]  

# primer ulaza za ovu sliku:
# dst_points = [[164, 717, 1],
#               [294, 717, 1],
#               [294, 30, 1],
#               [164, 30, 1]] 

dst_points = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0], 
              [0, 0, 0]]

print("Uneti afine koordinate 4 temena pravougaonika:")
for i in range(4):
    dst_points[i][0] = float(input("x koordinata: "))
    dst_points[i][1] = float(input("y koordinata: "))
    dst_points[i][2] = 1

change_photo(src_points, dst_points)