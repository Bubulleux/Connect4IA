import PlyVsPly
import PlyVsIA
import TrainModel
import TrainNeat

while True:
    print("1) Ply Vs Ply \n2) Ply Vs IA \n3) Train IA\n4) Train Neat")
    choise = input("Your Choise: ")
    if choise == "1":
        PlyVsPly.launch_game()
    elif choise == "2":
        PlyVsIA.launch_game()
    elif choise == "3":
        TrainModel.train()
    elif choise == "4":
        TrainNeat.Train()
    else:
        print("You Can't Choise That")
        continue
