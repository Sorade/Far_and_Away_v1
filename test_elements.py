'''a class which enables to return weighted quadrants based on the
inverse amount of occurences in the given quadrant.
eg. if occurences are TP,TR,BR,BL = 1,1,0,2
the return weight would be 1,1,2,0
the angle list returns the angles determining the quadrant with the weighted value
[(angle_min,angle_max,weight),...]

class Quad(object):
    ref_x,ref_y = (0,0)
    conts = [0,0,0,0]
    weights = [0,0,0,0]
    angle_list = [0,0,0,0]
    @staticmethod    
    def get_content(ref_pt,pts_list):
        Quad.conts = [0,0,0,0]
        Quad.ref_x,Quad.ref_y = ref_pt
        for x,y in pts_list:
            if x < Quad.ref_x and y <= Quad.ref_y:
                Quad.conts[0] += 1 #TL
            elif x >= Quad.ref_x and y < Quad.ref_y:
                Quad.conts[3] += 1 #TR
            elif x > Quad.ref_x and y >= Quad.ref_y:
                Quad.conts[2] += 1 #BL
            else:
                Quad.conts[1] += 1 #BR
                
    @staticmethod            
    def get_weights():
        cont_max = max(Quad.conts)
        counter = 0
        for cont in Quad.conts:
            Quad.weights[counter] = cont_max - cont
            counter += 1
        #checks for none 0 max weight value
        if max(Quad.weights) == 0:
            for x in range(len(Quad.weights)):
                Quad.weights[x] = 1
                
        #builds an assigned list
        counter = 0
        for w in Quad.weights:
            Quad.angle_list[counter] = (counter*np.pi/2,(counter+1)*np.pi/2,w)
            counter += 1
        
            
Quad.get_content((0,0),[(-10,-10),(10,-10),(-10,10),(-10,10)])    
Quad.get_weights()    
print Quad.angle_list




'''takes a list of tulpe values and plots them in a graph
of which the bottom left corner is set as o_pos and has 
a width and height defined by the dim tulpe = to (w,h)'''
def show_graph(list,o_pos,dim):
    ox,oy = o_pos
    w,h = dim
    dx = float(w)/max([x-1 for x,y in list])
    dy = float(h)/max([y for x,y in list])
    pts = [(int(ox+(x-1)*dx),int(oy-y*dy)) for x,y in list]
    #need to add a bg here
    
    #y axis labels
    ylab_pts = [(ox,int(oy-y*dy),y) for x,y in list] # (x,y,val)
    #x axis labels
    xlab_pts = [(int(ox+(x-1)*dx),oy,x) for x,y in list]
    #blits labels
    for pt in ylab_pts + xlab_pts:
        'a'#blit(str(pt[2]) at pos (pt[0],pt[1]))
    return pts
