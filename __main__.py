import PlyVsPly
import PlyVsIA
import TrainModel

while True:
    print("1) Ply Vs Ply \n2) Ply Vs IA \n3) Train IA")
    choise = input("Your Choise: ")
    if choise == "1":
        PlyVsPly.LancheGame()
    elif choise == "2":
        PlyVsIA.LancheGame()
    elif choise == "3":
        TrainModel.train()
    else:
        print("You Can't Choise That")
        continue
