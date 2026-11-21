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

    def __init__(self, pos:tuple, dist:float, case:int, rot:tuple, dim:tuple, cam:Camera):
        self.cam = cam                                                                      # camera object
        self.case = case                                                                    # determines which vertex of the box is the origin of transformation
        self.pos = pos                                                                      # the position of the origin on screen in pixels
        self.dist = dist                                                                    # the distance of the origin from the camera
        self.cpos = (int(pos[0]-self.cam.res[0]//2),-int(pos[1]-self.cam.res[1]//2))        # the position of the origin relative to the screen center in pixels
        self.cord = (forshortening(self.cam.num,px=self.cpos[0],dist=self.dist),            # the coordinate of the origin relative to world origin set at camera focal point in meters
                     forshortening(self.cam.num,px=self.cpos[1],dist=self.dist),    
                     self.dist)
        self.rot = (math.radians(rot[0]),math.radians(rot[1]),math.radians(rot[2]))         # the rotation of the origin in order of pitch, yaw, and roll, in radian
        self.dim = dim                                                                      # the dimension of the box in meters, in order of width, height, and length

    def chng_case(self,ncase):
        self.case = ncase

    def chng_dist(self,ndist):
        self.dist = ndist

    def chng_pos(self,npos):
        self.pos = npos

    def chng_rot(self,nang):
        self.rot = (math.radians(nang[0]),math.radians(nang[1]),math.radians(nang[2]))

    def chng_dim(self,ndim):
        self.dim = ndim

    def get_wireframe(self):
        match self.case:        # origin at:
            case 0:
                self.draw_wireframe(self.case_c())      # center
            case 1:
                self.draw_wireframe(self.case_ftl())    # front top left
            case 2:
                self.draw_wireframe(self.case_ftr())    # front top right
            case 3:
                self.draw_wireframe(self.case_fbl())    # front bottom left
            case 4:
                self.draw_wireframe(self.case_fbr())    # front bottom right
            case 5:
                self.draw_wireframe(self.case_btl())    # back top left
            case 6:
                self.draw_wireframe(self.case_btr())    # back top right
            case 7:
                self.draw_wireframe(self.case_bbl())    # back bottom left
            case 8:
                self.draw_wireframe(self.case_bbr())    # back bottom right

    def draw_wireframe(self,vtcords):
        img = Image.new("RGBA", self.cam.res, (0,0,0,0))
        posls = []
        for cor in vtcords:
            cord = (cor[0]+self.cord[0],cor[1]+self.cord[1],cor[2]+self.cord[2])
            cpos = self.cord_to_cpos(cord)
            pos = self.cpos_to_pos(cpos)
            posls.append(pos)
            d = ImageDraw.Draw(img, "RGBA")
            d.circle(pos, 4, "Black", None, 0)
        d.line([posls[1],posls[2]],"Black",4,None)
        d.line([posls[1],posls[3]],"Black",4,None)
        d.line([posls[1],posls[5]],"Black",4,None)
        d.line([posls[4],posls[2]],"Black",4,None)
        d.line([posls[4],posls[3]],"Black",4,None)
        d.line([posls[4],posls[8]],"Black",4,None)
        d.line([posls[6],posls[5]],"Black",4,None)
        d.line([posls[6],posls[2]],"Black",4,None)
        d.line([posls[6],posls[8]],"Black",4,None)
        d.line([posls[7],posls[5]],"Black",4,None)
        d.line([posls[7],posls[8]],"Black",4,None)
        d.line([posls[7],posls[3]],"Black",4,None)
        ImageShow.show(img,"wireframe")

    def cord_to_cpos(self,cord):    # translates meter coordinate relative to world origin to pixel coordinate ralative to screen center
        x = forshortening(self.cam.num,len=cord[0],dist=cord[2])
        y = forshortening(self.cam.num,len=cord[1],dist=cord[2])
        return (x,y)

    def cpos_to_pos(self,cpos):      # translates center pixel coordinate to standard pixel coordinate with origin at top left corner
        pos = (int(cpos[0]+self.cam.res[0]//2),int(-cpos[1]+self.cam.res[1]//2))
        return pos

    def rotate(self, pos:tuple):
        z = pos[2]
        y = pos[1]
        x = pos[0]
        pitchR = math.sqrt(math.pow(z,2)+math.pow(y,2))
        x_init_ang = math.atan2(y,z)
        x_rot_ang = x_init_ang - self.rot[0]
        y = pitchR*math.sin(x_rot_ang)
        z = pitchR*math.cos(x_rot_ang)
        yawR = math.sqrt(math.pow(x,2)+math.pow(z,2))
        y_init_ang = math.atan2(z,x)
        y_rot_ang = y_init_ang + self.rot[1]
        z = yawR*math.sin(y_rot_ang)
        x = yawR*math.cos(y_rot_ang)
        rollR = math.sqrt(math.pow(x,2)+math.pow(y,2))
        z_init_ang = math.atan2(y,x)
        z_rot_ang = z_init_ang + self.rot[2]
        y = rollR*math.sin(z_rot_ang)
        x = rollR*math.cos(z_rot_ang)
        return (x,y,z)

    def get_rotd_pos(self, verts):
        verts_pos = []
        for vert in verts:
            vert.chng_p(self.rotate(vert.pos))
            verts_pos.append(vert.pos)
        return verts_pos

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
        return self.get_rotd_pos(verts)

    def case_ftl(self):
        c = Vert(pos=(self.dim[0]/2,-self.dim[1]/2,self.dim[2]/2))
        ftl = Vert()
        ftr = Vert(pos=(self.dim[0],0,0))
        fbl = Vert(pos=(0,-self.dim[1],0))
        fbr = Vert(pos=(self.dim[0],-self.dim[1],0))
        btl = Vert(pos=(0,0,self.dim[2]))
        btr = Vert(pos=(self.dim[0],0,self.dim[2]))
        bbl = Vert(pos=(0,-self.dim[1],self.dim[2]))
        bbr = Vert(pos=(self.dim[0],-self.dim[1],self.dim[2]))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_ftr(self):
        c = Vert(pos=(-self.dim[0]/2,-self.dim[1]/2,self.dim[2]/2))
        ftl = Vert(pos=(-self.dim[0],0,0))
        ftr = Vert()
        fbl = Vert(pos=(-self.dim[0],-self.dim[1],0))
        fbr = Vert(pos=(0,-self.dim[1],0))
        btl = Vert(pos=(-self.dim[0],0,self.dim[2]))
        btr = Vert(pos=(0,0,self.dim[2]))
        bbl = Vert(pos=(-self.dim[0],-self.dim[1],self.dim[2]))
        bbr = Vert(pos=(0,-self.dim[1],self.dim[2]))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_fbl(self):
        c = Vert(pos=(self.dim[0]/2,self.dim[1]/2,self.dim[2]/2))
        ftl = Vert(pos=(0,self.dim[1],0))
        ftr = Vert(pos=(self.dim[0],self.dim[1],0))
        fbl = Vert()
        fbr = Vert(pos=(self.dim[0],0,0))
        btl = Vert(pos=(0,self.dim[1],self.dim[2]))
        btr = Vert(pos=(self.dim[0],self.dim[1],self.dim[2]))
        bbl = Vert(pos=(0,0,self.dim[2]))
        bbr = Vert(pos=(self.dim[0],0,self.dim[2]))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_fbr(self):
        c = Vert(pos=(-self.dim[0]/2,self.dim[1]/2,self.dim[2]/2))
        ftl = Vert(pos=(-self.dim[0],self.dim[1],0))
        ftr = Vert(pos=(0,self.dim[1],0))
        fbl = Vert(pos=(-self.dim[0],0,0))
        fbr = Vert()
        btl = Vert(pos=(-self.dim[0],self.dim[1],self.dim[2]))
        btr = Vert(pos=(0,self.dim[1],self.dim[2]))
        bbl = Vert(pos=(-self.dim[0],0,self.dim[2]))
        bbr = Vert(pos=(0,0,self.dim[2]))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_btl(self):
        c = Vert(pos=(self.dim[0]/2,-self.dim[1]/2,-self.dim[2]/2))
        ftl = Vert(pos=(0,0,-self.dim[2]))
        ftr = Vert(pos=(self.dim[0],0,-self.dim[2]))
        fbl = Vert(pos=(0,-self.dim[1],-self.dim[2]))
        fbr = Vert(pos=(self.dim[0],-self.dim[1],-self.dim[2]))
        btl = Vert()
        btr = Vert(pos=(self.dim[0],0,0))
        bbl = Vert(pos=(0,-self.dim[1],0))
        bbr = Vert(pos=(self.dim[0],-self.dim[1],0))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_btr(self):
        c = Vert(pos=(-self.dim[0]/2,-self.dim[1]/2,-self.dim[2]/2))
        ftl = Vert(pos=(-self.dim[0],0,-self.dim[2]))
        ftr = Vert(pos=(0,0,-self.dim[2]))
        fbl = Vert(pos=(-self.dim[0],-self.dim[1],-self.dim[2]))
        fbr = Vert(pos=(0,-self.dim[1],-self.dim[2]))
        btl = Vert(pos=(-self.dim[0],0,0))
        btr = Vert()
        bbl = Vert(pos=(-self.dim[0],-self.dim[1],0))
        bbr = Vert(pos=(0,-self.dim[1],0))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_bbl(self):
        c = Vert(pos=(self.dim[0]/2,self.dim[1]/2,-self.dim[2]/2))
        ftl = Vert(pos=(0,self.dim[1],-self.dim[2]))
        ftr = Vert(pos=(self.dim[0],self.dim[1],-self.dim[2]))
        fbl = Vert(pos=(0,0,-self.dim[2]))
        fbr = Vert(pos=(self.dim[0],0,-self.dim[2]))
        btl = Vert(pos=(0,self.dim[1],0))
        btr = Vert(pos=(self.dim[0],self.dim[1],0))
        bbl = Vert()
        bbr = Vert(pos=(self.dim[0],0,0))
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)
    
    def case_bbr(self):
        c = Vert(pos=(-self.dim[0]/2,self.dim[1]/2,-self.dim[2]/2))
        ftl = Vert(pos=(-self.dim[0],self.dim[1],-self.dim[2]))
        ftr = Vert(pos=(0,self.dim[1],-self.dim[2]))
        fbl = Vert(pos=(-self.dim[0],0,-self.dim[2]))
        fbr = Vert(pos=(0,0,-self.dim[2]))
        btl = Vert(pos=(-self.dim[0],self.dim[1],0))
        btr = Vert(pos=(0,self.dim[1],0))
        bbl = Vert(pos=(-self.dim[0],0,0))
        bbr = Vert()
        verts = [c,ftl,ftr,fbl,fbr,btl,btr,bbl,bbr]
        return self.get_rotd_pos(verts)


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
    cam = Camera((7680,4320),36,24)
    box = Box((3840,2160),forshortening(cam.num,len=1,px=1000),0,(30,10,20),(1,1,1),cam)
    box.get_wireframe()

if __name__ == "__main__":
    main()