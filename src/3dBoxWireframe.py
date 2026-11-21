from PIL import Image,ImageShow,ImageDraw
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


class Vert():

    def __init__(self, pos=(0,0,0)):
        self.pos = pos      # in meters

    def chng_p(self, npos):
        self.pos = npos



class Box():

    def __init__(self, pos:tuple, dist:float, case:int, res:tuple, rot:tuple, dim:tuple, camnum):
        self.case = case                                                    # determines which vertex of the box is the origin of transformation
        self.pos = pos                                                      # the position of the origin on screen in pixels
        self.dist = dist                                                    # the distance of the origin from the camera
        self.cpos = (int(pos[0]-res[0]//2),-int(pos[1]-res[1]//2))          # the position of the origin relative to the center
        self.cord = (forshortening(camnum,px=self.cpos[0],dist=self.dist),  # the coordinate of the origin relative to world origin set at camera focal point in meters
                     forshortening(camnum,px=self.cpos[1],dist=self.dist),
                     self.dist)
        self.rot = rot                                                      # the rotation of the origin in order of pitch, yaw, and roll, in radian
        self.dim = dim                                                      # the dimension of the box in meters, in order of width, height, and length

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

    def rotate(self, pos:tuple):
        z = -pos[2]
        y = pos[1]
        x = pos[0]
        pitchR = math.sqrt(math.pow(z,2)+math.pow(y,2))
        x_init_ang = math.atan(y/z)
        x_rot_ang = x_init_ang + self.rot[0]
        z = pitchR*math.sin(x_rot_ang)
        y = pitchR*math.cos(x_rot_ang)
        yawR = math.sqrt(math.pow(x,2)+math.pow(z,2))
        y_init_ang = math.atan(x/z)
        y_rot_ang = y_init_ang + self.rot[1]
        x = yawR*math.sin(y_rot_ang)
        z = yawR*math.cos(y_rot_ang)
        rollR = math.sqrt(math.pow(x,2)+math.pow(y,2))
        z_init_ang = math.atan(y/x)
        z_rot_ang = z_init_ang + self.rot[2]
        y = rollR*math.sin(z_rot_ang)
        x = rollR*math.cos(z_rot_ang)
        return (x,y,z)


    def case_c(self):
        c = Vert()
        ftl = Vert(pos=(-self.dim[0]/2,self.dim[1]/2,-self.dim[2]/2))
        ftr = Vert(pos=(self.dim[0]/2,self.dim[1]/2,-self.dim[2]/2))
        fbl = Vert(pos=(-self.dim[0]/2,-self.dim[1]/2,-self.dim[2]/2))
        fbr = Vert(pos=(self.dim[0]/2,-self.dim[1]/2,-self.dim[2]/2))
        btl = Vert(pos=(-self.dim[0]/2,self.dim[1]/2,self.dim[2]/2))
        btr = Vert(pos=(self.dim[0]/2,self.dim[1]/2,self.dim[2]/2))
        bbl = Vert(pos=(-self.dim[0]/2,-self.dim[1]/2,self.dim[2]/2))
        bbr = Vert(pos=(self.dim[0]/2,-self.dim[1]/2,self.dim[2]/2))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        verts_pos = []
        for vert in verts:
            vert.chng_p(self.rotate(vert.pos))
            verts_pos += vert.pos
        return verts_pos

    def case_ftl():

    def case_ftr():

    def case_fbl():

    def case_fbr():

    def case_btl():

    def case_btr():

    def case_bbl():

    def case_bbr():


def forshortening(camnum, len=0, px=0, dist=0): # parameters: camera number, length in meters, px/dist value in pixels/meters
    if len == 0:
        return px*dist/camnum
    elif px == 0:
        return camnum*len/dist
    elif dist == 0:
        return camnum*len/px
    else:
        pass


def main():
    pass

if __name__ == "__main__":
    main()