import math
from matplotlib import pyplot as plt

SMALL_ANGLE = 0.001
VERY_SMALL_CURVATURE = 1e-6
EPSILON = 1e-12
SATURATE_ACCELERATION = 0.0001
def pimod(q):
  return ( q + math.pi) % (2 * math.pi ) - math.pi

def sign(q):
  return 0 if q == 0 else( 1 if q > 0 else -1)

def percentAlongLineSegment(x0, y0, x1, y1, x, y):
    dpx = x1 - x0
    dpy = y1 - y0
    distance_squared = dpx*dpx + dpy*dpy
    # If segment is too short to check return a value (2) outside range 0-1
    return 2 if (distance_squared == 0) else ((x - x0)*dpx + (y - y0)*dpy)/distance_squared

class State:
    def __init__(self,x,y,heading,curvature):
        self.x = x
        self.y = y
        self.heading = heading
        self.curvature = curvature

    def __str__(self):
        return 'x={} y={} heading={} curvature={}'.format(self.x, self.y, self.heading, self.curvature)

class Arc:
    def __init__(self,start_x, start_y, start_heading, curvature, distance):
        self.start_x = start_x
        self.start_y = start_y
        self.start_heading = start_heading
        self.curvature = curvature
        self.distance = distance

    def __str__(self):
        return 'start_x={} start_y={} start_heading={} curvature={} distance={}'.format(
            self.start_x, self.start_y, self.start_heading, self.curvature, self.distance)

    def length(self):
        return abs(self.distance)
    
    def state(self,distance):
        cosine_initial_heading = math.cos(self.start_heading)
        sine_initial_heading = math.sin(self.start_heading)
        if abs(self.curvature) < VERY_SMALL_CURVATURE:
            x = self.start_x + cosine_initial_heading*distance
            y = self.start_y + sine_initial_heading*distance
        elif abs(self.curvature * distance) < SMALL_ANGLE:
            segment_scalar = self.curvature * distance / 2
            x = self.start_x + (cosine_initial_heading - segment_scalar*sine_initial_heading)*distance
            y = self.start_y + (sine_initial_heading + segment_scalar * cosine_initial_heading)*distance
        else:
            x = self.start_x + (math.sin(self.start_heading + self.curvature*distance) - sine_initial_heading)/self.curvature
            y = self.start_y + (cosine_initial_heading - math.cos(self.start_heading + self.curvature * distance))/self.curvature

        return State(x,y,self.start_heading + self.curvature*distance,self.curvature)

    def endState(self):
        return self.state(self.distance)

    def center(self):
        return {'x':self.start_x - math.sin(self.start_heading)/self.curvature,
            'y':self.start_y + math.cos(self.start_heading)/self.curvature}

    def percentAlong(self, x, y):
        if abs(self.curvature) < VERY_SMALL_CURVATURE:
            final_state = self.endState()
            return percentAlongLineSegment(self.start_x, self.start_y, final_state.x, final_state.y, x, y)
        center = self.center()
        arc_center_x_to_test_x = x - center['x']
        arc_center_y_to_test_y = y - center['y']
        arc_delta_heading = self.curvature*self.distance
        if abs(arc_delta_heading) <= EPSILON:
            return 2; # arc is too short to check, just return a value outside the range 0 - 1
        angle_from_arc_center_to_test_point = math.atan2(arc_center_y_to_test_y, arc_center_x_to_test_x)
        angle_from_arc_center_to_arc_midpoint = self.start_heading + arc_delta_heading/2 + \
            (-math.pi/2 if (self.curvature > 0) else math.pi/2)
        angle_from_arc_center_to_arc_midpoint = pimod(angle_from_arc_center_to_arc_midpoint)

        delta_angle = angle_from_arc_center_to_test_point - angle_from_arc_center_to_arc_midpoint
        qdistc = pimod(delta_angle) / arc_delta_heading
        qdistc_opposite = pimod(delta_angle + math.pi) / arc_delta_heading;
        if abs(qdistc) <= 0.5:
            return qdistc + 0.5; # Line goes from center point of arc to (x,y) to point on arc
        elif abs(qdistc_opposite) <= 0.5:
            return qdistc_opposite + 0.5; # Line goes from (x,y) to center of arc to point on arc
        else:
            # Can't draw a line from (x,y) to center point of arc to arc
            arc_end_x = center['x'] + math.sin(self.start_heading + arc_delta_heading)/self.curvature
            arc_end_y = center['y'] - math.cos(self.start_heading + arc_delta_heading)/self.curvature
            checkside = math.hypot(self.start_x - x, self.start_y - y) < math.hypot(arc_end_x - x, arc_end_y - y)
            choice = [qdistc + 0.5, qdistc_opposite + 0.5]
            return min(choice) if (checkside) else max(choice); # return outside region

    def plot(self):
        l = self.length()
        x = []
        y = []
        for ii in range(100):
            s = self.state(ii/99*l)
            x.append(s.x)
            y.append(s.y)
        return (x,y)

class Arcs:
    def __init__(self, arcs):
        self.arcs = arcs
        
    def __str__(self):
        return 'Arcs:\n   - ' + '\n   - '.join([str(a) for a in self.arcs])

    def _lengthAtFirstPerpendicularPointonPath(self, x, y, lstart):
        # assuming "arcs" are a (close to) continuous path of lines/arcs then:
        # lengthAtFirstPerpendicularPointonPath will return the length of the first point on "arcs"
        # that is perpendicular to (x,y) Second tuple item is true if (x,y) is not perpendicular
        # to any point on arcs (and x,y is closer to the end than the start of all segments)
        lpast = 0
        for arc in self.arcs:
            if lpast + arc.length() < lstart:
                lpast += arc.length()
                continue
            prcnt = arc.percentAlong(x, y)
            if prcnt <= 1 and prcnt >= 0:
                return (lpast + prcnt*arc.length(), False)
            elif prcnt < 0:
                return (lpast, False)
            lpast += arc.length()
        return (lpast, True)

    def linspace(self,n):
        L = sum([a.distance for a in self.arcs])
        l = [float(dd)/float(n-1)*L for dd in range(n)]
        return [self.state(d) for d in l]

    def state(self, distance):
        for arc in self.arcs:
            if distance < arc.length():
                return arc.state(distance)
            distance -= arc.length()
        if len(self.arcs) > 0:
            return self.arcs[-1].state(distance+self.arcs[-1].length())
        return None

    def getNearestPoint(self, x, y, lstart=0, pop=False):
        l,finished = self._lengthAtFirstPerpendicularPointonPath(x,y, lstart)
        if pop:
            while len(self.arcs) > 1 and l > self.arcs[0].length(): # pop a segment
                l -= self.arcs[0].length()
                self.arcs.pop(0)
        return l,finished

    def isempty(self):
        return len(self.arcs) == 0

    def length(self):
        return sum([a.length() for a in self.arcs])

    def get_curvature_length_list(self):
        return [item for arc in self.arcs for item in [arc.curvature, arc.distance]]

    def plot(self, dl, ox=0, oy=0):
        x = [];    y = []
        l = 0
        L = self.length()
        while l < L:
            s = self.state(l)
            cq = math.cos(s.heading)
            sq = math.sin(s.heading)
            x.append(s.x + cq*ox - sq*oy)
            y.append(s.y + sq*ox + cq*oy)
            l += dl
        return (x,y)

class Race:
    def __init__(self, centerline, half_width, acceleration, max_speed, max_centripetal_acc, mud_speed, score_delta_length):
        self.centerline = centerline
        self.half_width = half_width
        self.max_acceleration = acceleration
        self.max_speed = max_speed
        self.max_centripetal_acc = max_centripetal_acc
        self.path_length = centerline.length()
        self.score_delta_length = score_delta_length
        self.mud_speed = mud_speed
    
    def score(self, path_):
        startstate = path_.state(0)
        cl = self.centerline.state(0)
        path = makeArcPath(cl.x, cl.y, startstate.heading, path_.get_curvature_length_list())
        L = path.length()
        l = 0
        ref_l = 0
        speed0 = 0
        # TODO Check continuity
        segments = []
        finished = False
        time = 0
        while True:
            s = path.state(l)
            ref_l, finished = self.centerline.getNearestPoint(s.x, s.y, lstart=ref_l)
            sref = self.centerline.state(ref_l)
            max_speed = min(self.max_speed, math.sqrt(abs(self.max_centripetal_acc/s.curvature))) if s.curvature != 0 else self.max_speed
            violation = math.hypot(s.x-sref.x, s.y-sref.y) - self.half_width
            dli = ref_l - self.path_length if finished else self.score_delta_length
            if violation > 1:
                speed1 = min(speed0,self.mud_speed)
            elif max_speed <= speed0:
                speed1 = max_speed
            else:
                dlmax = (max_speed*max_speed - speed0*speed0)/2/self.max_acceleration
                speed1 = max_speed if dlmax < dli else math.sqrt(speed0*speed0 + 2*self.max_acceleration*dli)
                dli = min(dlmax,dli)
            l += dli
            if dli > 0:
                acc = (speed1**2 - speed0**2)/2/dli
                time += (speed1 - speed0)/acc if (abs(acc) > SATURATE_ACCELERATION) else abs(dli/speed0)
            segments.append({'speed0':speed0, 'speed1':speed1, 'dl':dli, 'x':s.x, 'y':s.y,'l':ref_l,'time':time})
            if finished:
                break
            elif l > L: # past end of path but not finished with centerline. add a fake cost
                time += abs(self.path_length-l) / (0.1*self.max_speed)
                break
            speed0 = speed1

        return time,segments

    def plot_track(self,dl,path,segments_list):
        # plt.ion()
        (x1, y1) = self.centerline.plot(dl, oy=-self.half_width)
        (x2, y2) = self.centerline.plot(dl, oy=self.half_width)
        (x3, y3) = self.centerline.plot(dl)
        (x4, y4) = path.plot(dl)
        fig, axs = plt.subplots(2)
        axs[0].plot(x1, y1, 'b-', x2, y2, 'b-', x3, y3, 'r-', x4, y4, 'g-')
        axs[0].axis('equal')
        for segs in segments_list:
            t = []
            l = []
            L = 0
            for seg in segs:
                t.append(seg['time'])
                l.append(seg['l'])
            axs[1].plot(t,l)
        plt.show()

def makeArcPath(x0,y0,q0,path):
    segment_start = State(x0,y0,q0,0)
    arcs = []
    for p in range(int(len(path)/2)):
        arc = Arc(segment_start.x, segment_start.y, segment_start.heading, path[p*2], path[p*2+1])
        arcs.append(arc)
        segment_start = arc.endState()
    return Arcs(arcs)

def test1():
    path = makeArcPath(0,0,0,[0,50,  0.1,15,   0,50,  0.1,15,  0,50,  0.1,15,   0,50])
    l = 0
    dl = 1
    finished = False
    x = []
    y = []
    while not finished:
        s = path.state(l)
        x.append(s.x)
        y.append(s.y)
        ll,finished = path.getNearestPoint(s.x,s.y,lstart=l)
        l += dl

    # plt.ion()
    plt.plot(x, y, 'bo')
    plt.show()

if __name__ == '__main__':
    test1()
    