import cv2
import numpy as np


cap = cv2.VideoCapture('push-up1.mp4')


def up_arrow(img):
    cv2.polylines(img, [np.array([[185, 600], [140, 545], [130, 550]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)   # 5
    cv2.polylines(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[44, 398], [88, 380], [95, 350], [46, 368]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[47, 361], [96, 343], [108, 307], [57, 320]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[58, 314], [110, 301], [124, 270], [72, 280]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    cv2.polylines(img, [np.array([[62, 275], [107, 260], [140, 270], [120, 230]])], isClosed=True,
                  color=(0, 255, 0), thickness=2)
    return img


def down_arrow(img):
    cv2.polylines(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1213, 428], [1173, 450], [1169, 482], [1213, 457]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1214, 462], [1169, 487], [1159, 526], [1208, 500]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1207, 505], [1158, 531], [1149, 563], [1200, 538]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)
    cv2.polylines(img, [np.array([[1213, 538], [1168, 570], [1130, 570], [1165, 605]])], isClosed=True,
                  color=(0, 0, 255), thickness=2)

    return img


def colorful_up_arrow(img, percentage):
    if percentage < 5:
        cv2.polylines(img, [np.array([[185, 600], [140, 545], [130, 550]])], isClosed=True,
                      color=(0, 255, 0), thickness=2)

    elif percentage <= 9:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))

    elif percentage <= 18:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))

    elif percentage <= 27:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))

    elif percentage <= 36:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))

    elif percentage <= 45:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))

    elif percentage <= 54:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))

    elif percentage <= 63:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))

    elif percentage <= 72:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], color=(0, 255, 0))

    elif percentage <= 81:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[44, 398], [88, 380], [95, 350], [46, 368]])], color=(0, 255, 0))

    elif percentage <= 90:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[44, 398], [88, 380], [95, 350], [46, 368]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[47, 361], [96, 343], [108, 307], [57, 320]])], color=(0, 255, 0))

    elif percentage <= 99:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[44, 398], [88, 380], [95, 350], [46, 368]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[47, 361], [96, 343], [108, 307], [57, 320]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[58, 314], [110, 301], [124, 270], [72, 280]])], color=(0, 255, 0))

    elif percentage == 100:
        cv2.fillPoly(img, [np.array([[185, 600], [140, 545], [130, 550]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[127, 547], [138, 541], [132, 532], [119, 539]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[115, 535], [130, 527], [123, 515], [105, 524]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[101, 520], [120, 510], [113, 496], [91, 507]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[87, 503], [111, 491], [104, 475], [77, 488]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[73, 483], [102, 469], [96, 450], [63, 465]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[60, 460], [94, 445], [90, 420], [52, 437]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[50, 431], [88, 414], [88, 386], [46, 404]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[44, 398], [88, 380], [95, 350], [46, 368]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[47, 361], [96, 343], [108, 307], [57, 320]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[58, 314], [110, 301], [124, 270], [72, 280]])], color=(0, 255, 0))
        cv2.fillPoly(img, [np.array([[62, 275], [107, 260], [140, 270], [120, 230]])], color=(0, 255, 0))

    return img


def colorful_down_arrow(img, percentage):

    if percentage < 5:
        cv2.polylines(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], isClosed=True,
                      color=(0, 0, 255), thickness=2)

    elif percentage <= 9:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))

    elif percentage <= 18:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))

    elif percentage <= 27:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))

    elif percentage <= 36:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))

    elif percentage <= 45:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))

    elif percentage <= 54:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))

    elif percentage <= 63:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))

    elif percentage <= 72:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], color=(0, 0, 255))

    elif percentage <= 81:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1213, 428], [1173, 450], [1169, 482], [1213, 457]])], color=(0, 0, 255))

    elif percentage <= 90:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1213, 428], [1173, 450], [1169, 482], [1213, 457]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1214, 462], [1169, 487], [1159, 526], [1208, 500]])], color=(0, 0, 255))

    elif percentage <= 99:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1213, 428], [1173, 450], [1169, 482], [1213, 457]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1214, 462], [1169, 487], [1159, 526], [1208, 500]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1207, 505], [1158, 531], [1149, 563], [1200, 538]])], color=(0, 0, 255))

    elif percentage == 100:
        cv2.fillPoly(img, [np.array([[1070, 230], [1115, 285], [1125, 280]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1128, 283], [1117, 289], [1123, 298], [1136, 291]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1140, 295], [1125, 303], [1132, 315], [1150, 304]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1154, 310], [1135, 322], [1142, 336], [1164, 323]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1167, 328], [1145, 341], [1152, 358], [1178, 344]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1181, 349], [1155, 363], [1162, 382], [1192, 366]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1195, 371], [1164, 387], [1169, 412], [1204, 393]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1206, 397], [1170, 417], [1172, 445], [1212, 423]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1213, 428], [1173, 450], [1169, 482], [1213, 457]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1214, 462], [1169, 487], [1159, 526], [1208, 500]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1207, 505], [1158, 531], [1149, 563], [1200, 538]])], color=(0, 0, 255))
        cv2.fillPoly(img, [np.array([[1213, 538], [1168, 570], [1130, 570], [1165, 605]])], color=(0, 0, 255))
    return img

# while True:
#     success, img = cap.read()
#
#     img = cv2.resize(img, (1280, 720))
#
#     up_arrow(img=img)
#     down_arrow(img=img)
#     colorful_up_arrow(img=img, percentage=0)
#     colorful_down_arrow(img=img, percentage=100)
#
#     cv2.imshow("Image", img)
#     cv2.waitKey(0)

