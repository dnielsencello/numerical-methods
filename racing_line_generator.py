import time
import sys
import math
sys.path.append('/home/nate/misc/nate/vybase/ui/example_RacingLine/harness')

import racing_line

def generate(race: racing_line.Race, max_solve_time):

    start = race.centerline.state(0) # Get the state of the vehicle on the path at length = 0 (Initial state of the path)
    x = race.centerline.get_curvature_length_list()
    centerPath = racing_line.makeArcPath(start.x, start.y, start.heading, x)
    centerPathRace = racing_line.Race(centerPath, race.half_width, race.max_acceleration,race.max_speed, race.max_centripetal_acc,race.mud_speed,race.score_delta_length )
    nomtime, nomsegments = centerPathRace.score(centerPath)
    temprace1 = centerPathRace
    temporaryx = []
    temporaryx2 = []
    temporaryx.append(x[0])
    temporaryx2.append(x[0])
    temporaryx.append(x[1])
    temporaryx2.append(x[1])
    tol = 100
    for i in range(0, len(x)-2, 2):
        addToTempx(temporaryx, temporaryx2, x, i)
        temprace2path = racing_line.makeArcPath(start.x, start.y, start.heading, temporaryx2)
        temprace2 = racing_line.Race(temprace2path, race.half_width, race.max_acceleration, race.max_speed,
                                          race.max_centripetal_acc, race.mud_speed, race.score_delta_length)
        besttime, bestOptimization = temprace2.score(temprace2path)


        a = 0
        b = race.half_width
        n = 0
        c = (a + b) / 2
        hey = True
        while hey:
            tol = abs(a - b)
            reset(temporaryx, x, i)


            optimize(temporaryx, temporaryx2, i, x, c)
            temprace1 = racing_line.makeArcPath(start.x, start.y, start.heading, temporaryx)
            optimizedTime, optimizedSegements = temprace2.score(temprace1)
            #centerPathRace.plot_track(0.1, temprace1, [nomsegments, optimizedSegements])
            if optimizedTime >= besttime:
                b = c
            if optimizedTime < besttime:
                a = c
                besttime = optimizedTime
            if tol < 0.01:
                hey = False
                reset(temporaryx, x, i)
                optimize(temporaryx, temporaryx2, i, x, c)
                for p in range(len(temporaryx)):
                    x[p] = temporaryx[p]
            c = (a + b) / 2

    time, segments = centerPathRace.score(centerPath)
    return racing_line.makeArcPath(start.x, start.y, start.heading, x)

    # Make sure you return someting in less than max_solve_time, otherwise it won't be scored!

def reset(temporaryx, x, i):
    for n in range(len(temporaryx)):
        temporaryx[n] = x[n]
    hey = 0


def addToTempx(temporaryx, temporaryx2, x, i):
        temporaryx.append(x[i+2])
        temporaryx.append(x[i+3])
        temporaryx2.append(x[i+2])
        temporaryx2.append(x[i+3])
def optimize(temporaryx, temporaryx2, i, x, width):

    if temporaryx[i] > 0:
        newradius = 1/temporaryx[i] - width
        temporaryx[i] = 1 / newradius
        temporaryx[i + 1] = temporaryx[i + 1] * temporaryx2[i] / temporaryx[i]
    if temporaryx[i] < 0:
        newradius = 1/temporaryx[i] + width
        temporaryx[i] = 1 / newradius
        temporaryx[i + 1] = temporaryx[i+1]*temporaryx2[i]/temporaryx[i]
    if temporaryx[i] == 0:
        temporaryx[i+1] -= width

    return(temporaryx,temporaryx2)

def example_test():
    # As an example in class Monday I will generate an instance of the "Race" class
    centerline = racing_line.makeArcPath(0, 0, 0,
                                         [0,100,-0.01,314,0,100,-0.01,314])
    race_1 = racing_line.Race(centerline, 5, 4, 10, 4, 1, 0.5)
    max_solve_time = 5
    my_brilliant_students_path = generate(race_1, max_solve_time)

    nomtime, nomsegments = race_1.score(centerline)
    time, segments = race_1.score(my_brilliant_students_path)
    print("My brilliant student completed the course in {} seconds (nominal {} seconds)".format(time,nomtime))

    # And maybe visualize it
    race_1.plot_track(0.1, my_brilliant_students_path,[nomsegments,segments])

if __name__ == '__main__':
    example_test()