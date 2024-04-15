from evolutie import *

if __name__ == "__main__":
    myEvo = Evolution((-1, -5, -7), 20, (-10, 10), 10, (0.25, 0.2), 500, 0)
    newEvo = myEvo
    while newEvo is not None:
        print(myEvo)
        newEvo = myEvo.evolve()
        if newEvo is not None:
            myEvo = newEvo

    print(f"Best chromosome is: {myEvo.select_elite_member().get_value()} with a value of {myEvo.evaluate_chromosome(myEvo.select_elite_member())}")