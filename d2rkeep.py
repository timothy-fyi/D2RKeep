from time_keeper import time_keeper
from time_graph import time_graph

print(f"""D2RKeep: A time keeping utility for Diablo 2: Resurrected.\n\nMake your selection:
1. Time Keeper
2. Time Graph
0. Exit
""")

while True:
    choice = input("Selection: ")
    if choice in ("1","2","0"):
        break
    print("\nInvalid selection. Please enter a number corresponding to the option you wish to use.\n")

if choice == "1":
    time_keeper()
if choice == "2":
    time_graph()
if choice == "0":
    exit()
