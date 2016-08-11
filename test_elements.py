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
