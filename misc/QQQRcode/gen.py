import qrcode
import numpy as np
import random

def m(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=0,
    )
    qr.add_data(data)
    qr.make(fit=False)
    return np.array(qr.get_matrix())

def dump(box):
    with open("dump.txt", "w") as f:
        for z in range(21):
            for x in range(21):
                for y in range(21):
                    f.write(str(box[x][y][z]))

m1 = m("Azure")  # xoy
m2 = m("Assassin")  # xoz
m3 = m("Alliance")  # yoz

box = np.zeros((21, 21, 21))

box += m1[:, :, np.newaxis]
box += m2[:, np.newaxis, :]
box += m3[np.newaxis, :, :]
box[10][7][10] = 3

box = (box==3).astype(int)

choices = [[x,y,z] for x in range(21) for y in range(21) for z in range(21) if box[x][y][z]]
random.shuffle(choices)

xoy = (box.sum(axis=2)).astype(int)
xoz = (box.sum(axis=1)).astype(int)
yoz = (box.sum(axis=0)).astype(int)

for i,j,k in choices:
    if box[i][j][k] and xoy[i][j] > 1 and xoz[i][k] > 1 and yoz[j][k] > 1:
        box[i][j][k] = 0
        xoy[i][j] -= 1
        xoz[i][k] -= 1
        yoz[j][k] -= 1

dump(box)