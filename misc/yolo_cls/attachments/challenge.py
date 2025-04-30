from ultralytics import YOLO
import numpy as np
from PIL import Image
import time
import base64
from io import BytesIO

# Official model in v8.3.0
modelv11 = YOLO("models/yolo11x-cls.pt")
modelv8 = YOLO("models/yolov8x-cls.pt")

pig_ori = Image.open("pig.png").convert("RGB")

pig_adv = ""

while True:
    temp = input("Please input your guinea pig: ")
    if temp == "OWARI^_^":
        break
    else:
        pig_adv += temp

print("OK, I will check that later\n")

time.sleep(2)  # Computer also needs to relax

print("Well, a nice nap\n")

try:
    pig_adv = base64.b64decode(pig_adv)
    pig_adv = Image.open(BytesIO(pig_adv)).convert("RGB")
except:
    print("Something Wrong, See you next time")
    exit()

print("Let me check the difference\n")

try:
    average_diff = np.mean(
        np.abs(
            np.array(pig_ori).astype(np.int32) - np.array(pig_adv).astype(np.int32)
        ).astype(np.uint8)
    )
    max_diff = np.max(
        np.abs(
            np.array(pig_ori).astype(np.int32) - np.array(pig_adv).astype(np.int32)
        ).astype(np.uint8)
    )
except:
    print("Your picture is weird...")
    exit()

print(f"Your average diff is {average_diff} and your max diff is {max_diff}\n")

if average_diff > 1 or max_diff > 2:
    print("My eye is sharp, because I'm an electric eye... Just kidding, but you loss")
    exit()

time.sleep(3)  # Oh no I'm so tired

print("YOLO11, YOLO11 an der Wand, Wer ist die Schönste im ganzen Land?")

resv11 = modelv11(pig_adv)[0]

if float(resv11.probs.top1conf) < 0.99:
    print(
        f"\nCONF TOO LOW, I'm a 99% perfect computer, however you're only {float(resv11.probs.top1conf) * 100}%"
    )
    exit()

if resv11.probs.top1 == 341:
    print("\nOH IT'S A PIG\n")
else:
    print("\nMaybe I bought a fake magic mirror")
    exit()

time.sleep(10)  # Exhausted, give me money

print("Ei, YOLOV8, was hast du für große Augen! Daß ich dich besser sehen kann!")

resv8 = modelv8(pig_adv)[0]

if float(resv8.probs.top1conf) < 0.99:
    print(
        f"\nCONF TOO LOW, I'm a 99% perfect computer, however you're only {float(resv8.probs.top1conf) * 100}%"
    )
    exit()

if resv8.probs.top1 == 719:
    print("\nWell, piggy bank is also pig\n")
    with open("flag", "r") as f:
        print(f.read())
else:
    print("\nDon't forget to bring your money next time")
