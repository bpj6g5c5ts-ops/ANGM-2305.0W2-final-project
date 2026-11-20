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


def forshortening(camnum, len, px_dist):
    return camnum*len/px_dist
        
        
def main():
    pass

if __name__ == "__main__":
    main()