import PIL
import math


class Camera():

    def __init__(self, res=(3840,2160),sens=36,foclen=50):
        self.res = res #in pixels
        if res[0] >= res[1]: #determines sensor orientation based on rather resolution is landscape or portrait
            self.size = (sens,sens*(res[1]/res[0])) #in mm
        else:
            self.size = (sens*(res[0]/res[1]),sens) #in mm
        self.focallen = foclen #in mm
        self.horfov = math.atan(self.size[0]/(foclen*2)) #in radians
        self.vertfov = math.atan(self.size[1]/(foclen*2)) #in radians
        self.num = foclen*res[0]/self.size[0] #the camera constant in pixels


def forshortening(camnum, len, px_dist): # parameters: camera number, length in meters, px/dist value in pixels/meters
    return camnum*len/px_dist
        

class Box():

    def __init__(self, pos:tuple, dist:float, case:int, res:tuple, rot:tuple, dim:tuple):
        self.case = case                                            # determines which vertex of the box is the origin of transformation
        self.pos = pos                                              # the position of the origin on canvas in pixels
        self.dist = dist                                            # the distance of the origin from the camera
        self.cpos = (int(pos[0]-res[0]//2),-int(pos[1]-res[1]//2))  # the position of the origin relative to the center
        self.rot = rot                                              # the rotation of the origin in order of pitch, yaw, and roll, in radian
        self.dim = dim

    def get_wire_frame(self):
        match self.case:        # origin at:
            case 0:
                self.case_c()   # center
            case 1:
                self.case_ftl() # front top left
            case 2:
                self.case_ftr() # front top right
            case 3:
                self.case_fbl() # front bottom left
            case 4:
                self.case_fbr() # front bottom right
            case 5:
                self.case_btl() # back top left
            case 6:
                self.case_btr() # back top right
            case 7:
                self.case_bbl() # back bottom left
            case 8:
                self.case_bbr() # back bottom right


    class Vert():

        def __init__(self, pos:tuple, dist:float):
            self.pos = pos      # in pixels
            self.dist = dist    # in meters


    def case_c():

    def case_ftl():

    def case_ftr():

    def case_fbl():

    def case_fbr():

    def case_btl():

    def case_btr():

    def case_bbl():

    def case_bbr():



def main():
    pass

if __name__ == "__main__":
    main()