import math

class Circle:
    def __init__(self, c, r, b):
        self.c = c
        self.r = r
        self.b = b
    def point_in(self, x, y):
        return math.sqrt((x - self.c[0])**2 + (y - self.c[1])**2) <= self.r
    def check_rect_collision(self, quad_list):
        #https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection
        for quad in quad_list:
            circleDistance = abs(self.c[0] - quad.c[0]), abs(self.c[1] - quad.c[1])

            if (circleDistance[0] > (quad.w/2 + self.r)):
                continue
            if (circleDistance[1] > (quad.h/2 + self.r)):
                continue

            if (circleDistance[0] <= (quad.w/2)):
                return True
            if (circleDistance[1] <= (quad.h/2)):
                return True

            cornerDistance_sq = (circleDistance[0] - quad.w/2)**2 + (circleDistance[1] - quad.h/2)**2

            if cornerDistance_sq <= (self.r**2):
                return True
        return False


class Quad:
    def __init__(self, c, w, h, r, b):
        tr = (w, h)
        tl = (-w, h)
        br = (w, -h)
        bl = (-w, -h)

        #https://stackoverflow.com/questions/2259476/rotating-a-point-about-another-point-2d
        sin = math.sin(r)
        cos = math.cos(r)
        
        tr = (tr[0] * cos - tr[1] * sin, tr[0] * sin + tr[1] * cos)
        tl = (tl[0] * cos - tl[1] * sin, tl[0] * sin + tl[1] * cos)
        br = (br[0] * cos - br[1] * sin, br[0] * sin + br[1] * cos)
        bl = (bl[0] * cos - bl[1] * sin, bl[0] * sin + bl[1] * cos)

        self.tr = (tr[0]+c[0],tr[1]+c[1])
        self.tl = (tl[0]+c[0],tl[1]+c[1])
        self.br = (br[0]+c[0],br[1]+c[1])
        self.bl = (bl[0]+c[0],bl[1]+c[1])
        
        self.c = c
        self.r = r
        self.b = b
        self.w = w
        self.h = h
    def move(self, x, y, quad_list):
        c = self.c[0] + x, self.c[1] + y
        for quad in quad_list:
            if quad.point_in(self.tr[0] + x, self.tr[1] + y):
                return self, True, quad
            if quad.point_in(self.tl[0] + x, self.tl[1] + y):
                return self, True, quad
            if quad.point_in(self.br[0] + x, self.br[1] + y):
                return self, True, quad
            if quad.point_in(self.bl[0] + x, self.bl[1] + y):
                return self, True, quad
        return Quad(c, self.w, self.h, self.r, self.b), False

    def point_in(self, x, y):
        #https://math.stackexchange.com/questions/190111/how-to-check-if-a-point-is-inside-a-rectangle?noredirect=1&lq=1
        a = self.tr
        b = self.tl
        c = self.br
        d = self.bl
        p = (x, y)

        #https://math.stackexchange.com/questions/516219/finding-out-the-area-of-a-triangle-if-the-coordinates-of-the-three-vertices-are/516223
        apd = abs(a[0]*(p[1] - d[1]) + p[0]*(d[1] - a[1]) + d[0]*(a[1] - p[1]))/2
        dpc = abs(d[0]*(p[1] - c[1]) + p[0]*(c[1] - d[1]) + c[0]*(d[1] - p[1]))/2
        cpb = abs(c[0]*(p[1] - b[1]) + p[0]*(b[1] - c[1]) + b[0]*(c[1] - p[1]))/2
        pba = abs(p[0]*(b[1] - a[1]) + b[0]*(a[1] - p[1]) + a[0]*(p[1] - b[1]))/2

        tri_area = apd + dpc + cpb + pba
        rect_area = (math.sqrt( ((a[0]-c[0])**2) + ((a[1]-c[1])**2)) )  *  (math.sqrt( ((a[0]-b[0])**2) + ((a[1]-b[1])**2) ))
        return tri_area < rect_area
    def check_circle_collision(self, circle_list):
        #https://stackoverflow.com/questions/401847/circle-rectangle-collision-detection-intersection
        for circle in circle_list:
            circleDistance = abs(circle.c[0] - self.c[0]), abs(circle.c[1] - self.c[1])

            if (circleDistance[0] > (self.w/2 + circle.r)):
                continue
            if (circleDistance[1] > (self.h/2 + circle.r)):
                continue

            if (circleDistance[0] <= (self.w/2)):
                return True
            if (circleDistance[1] <= (self.h/2)):
                return True

            cornerDistance_sq = (circleDistance[0] - self.w/2)**2 + (circleDistance[1] - self.h/2)**2

            if cornerDistance_sq <= (circle.r**2):
                return True
        return False



def Render(resolution, scaler_res, quad_list, camera_pos, padding, extra_info = []):
    scale = (resolution[0]/scaler_res[0])
    fin = ""
    for y in range(-int(resolution[1]/2), int(resolution[1]/2)):
        line = ""
        for x in range(-int(resolution[0]/2), int(resolution[0]/2)):
            char = "  "
            if ((x == -int(resolution[0]/2) or x == int(resolution[0]/2)-1) or (y == -int(resolution[1]/2) or y == int(resolution[1]/2)-1)):
                char = "██"
            else:
                for quad in quad_list:
                    if quad.point_in(int(x/scale+camera_pos[0]),int(-y/scale+camera_pos[1])):
                        char = quad.b
                        break
            line = "".join([line, char])
        fin = "".join([fin, line, "\n"])
    print("".join(["\r", ("\n"*padding), fin, "\n", "\n".join(extra_info), "\r"]), end = "")
