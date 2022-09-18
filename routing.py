import picar_4wd as fc
import numpy as np
import sys
import time
import picar_4wd as fc

us_step = 5
scan_angle_max = 90
scan_angle_max = -90

speed = 10
cur_dir = "forward"
cur_pos = [20,200]
cur_dir_int = 0
dir_dict = {0:"forward",1:"right",2:"back",3:"left"}



def main():

    rmap = np.zeros(500,500)
    
    if len(sys.argv) ==3:
        end_point = [sys.argv[1],sys.argv[2]]
    else: end_point = [300,150]
    
    rmap = map_space(rmap,cur_pos,cur_dir)
    
    pdict,aend = A_star(cur_pos,end_point,rmap)
    
    bt = backtrack(pdict,aend)
    
    step_count =0
    
    prev_t = time.tim()
    
    while len(bt)>0:
    
    
        st = time.time()
        scan_list = fc.scan_step(20)
        #if not scan_list:
         #   continue
        tmp = scan_list[3:7]
        print(tmp)
        
        # re calculate map if within 10cm or 20cm and haven't looked in 20 steps
        if 1 in tmp or 0 in tmp:
            
            if 0 in tmp or step_count>20:
            
                if 0 in tmp:
                    move_back()
                
                rmap = map_space(rmap,cur_pos,cur_dir)
                pdict,aend = A_star(cur_pos,end_point,rmap)
                bt = backtrack(pdict,aend)
                step_count = 0
        
        else:
            
            print("time")
            print(time.time()-st)
            step_count = step_count+1
            move_step(bt[0])
            bt.pop(0)
            
def test_step(np_l):
    sc =0
    for np in np_l:
        sc = sc+1
        print(sc)
        st = time.time()
        scan_list = fc.scan_step(20)
        move_step(np)
        print(time.time()-st)
    fc.stop()
        
        
def ct_left():
    fc.turn_right(speed)
    time.sleep(2)
    cur_dir_int = (cur_dir_int-1)%4
    cur_dir = dir_dict[cur_dir_int]
    fc.forward(speed)
    
def ct_right():
    fc.turn_left(speed)
    time.sleep(2)
    cur_dir_int = (cur_dir_int+1)%4
    cur_dir = dir_dict[cur_dir_int]
    fc.forward(speed)
    
def move_back():
    step_time = .5/15
    
    fc.back(speed)
    time.delay(step_time*5)
    
    fc.stop()
    
    set_pos(5,(cur_dir_int+2)%4)

def set_pos(ns,nd):

    ns = int(ns)

    if nd == 0:
        ns = [0,ns]
    elif nd == 1:
        ns = [ns,0]
    elif nd == 2:
        ns = [0,-ns]
    elif nd == 3:
        ns = [-ns,0]
        
    cur_pos = [cur_pos[0]+ns[0],cur_pos[1] + ns[1]]
    
def move_step(np):

    next_move = [np[0]-cur_pos[0],np[1]-cur_pos[1]]
    
    if next_move[1]>0:
        next_move_dir = 0
    elif next_move[0]>0:
        next_move_dir = 1
        
    elif next_move[0]<0:
        next_move_dir = 3
        
    elif next_move[1]<0:
        next_move_dir = 2
        
    
    next_order = (next_move_dir-cur_dir_int)%4
    
    if next_order == 0:
        fc.forward(speed)
    if next_order == 1:
        ct_right()
        fc.forward(speed)
    if next_order == 3:
        ct_left()
        fc.forward(speed)
    if next_order == 2:
        fc.back(speed)        
        
        
'''       
def get_distance_at(angle):
    global angle_distance
    fc.servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    angle_distance = [angle, distance]
    return distance
'''   
    
def scan_step_dist(scan_angle_max = 90,scan_angle_min = -90,scan_step =5):

    fc.stop()
    
    scan_angle_max = min([scan_angle_max,90])
    scan_angle_min = max([scan_angle_min,-90])
    
    dist_list = []
    
    for ang in range(scan_angle_min,scan_angle_max, scan_step):
        
        cdt = fc.get_distance_at(ang)# get distance
        xy = [cdt*np.cos(ang),cdt*np.sin(ang)] # convert to grid
        dist_list.append(xy)
    
    return (dist_list)

    
def point_transform(point,dirc,cur_p):

    if dirc=="forward":
        return(point)
    elif dirc=="right":
        new_point = [point[1],-point[0]]
        return new_point
    elif dirc=="back":
        new_point = [-point[0],-point[1]]
        return new_point
    elif dirc=="left":
        new_point = [-point[1],point[0]]
        return new_point
    
    
def map_space(rmap, cur_p,dirc="forward" ):
    fc.stop()
    dl = scan_step_dist()
    
    prev = [1000,1000]
    for p in d1:
        #skip if blank space
        if p != [1000,1000]:
            prev = p
            continue
            
        # transform point based on current dirction
        else:
            p = point_transform(p,dirc)
            p = [p[0] + cur_p[0],p[1]+cur_p[1]]
            
            #give 10 point boudry
            
            minx = max(0,int(p[0]-10))
            maxx = min(rmap.shape[0]-1,int(p[0]+10))
            miny= max(0,int(p[1]-10))
            maxy = min(rmap.shape[1]-1,int(p[1]+10))
            
            rmap[minx:maxx,miny:maxy] = 1
            
            # draw boundry between the prev points
            if prev != [1000,1000]:
              
            
                # get all points in between 2 lines
                
                slope = (p[1]-prev[1])/(p[0]-prev[0])
                
                intc = p[1]-(slope*p[0])


                # make line between point and add 10
                stx = int(max(0,min(p[0],prev[0])-10))
                enx = int(min(rmap.shape[0],max(p[0],prev[0])+10))
                for pi in range(stx,enx):
                    piy= int(pix*slope+intc)
                    piymax = int(min(piy+10,rmap.shape[1]))
                    piminy = int(max(piy-10,0))
                    rmap[pi,piminy:pimaxy]=1
                
                prev = p
    return rmap
            
            
        
        
        


def man_dist (p1,p2):
    return(abs(p1[0]-p2[0])+abs(p1[1]-p2[1]))
    

def backtrack(prev_dict,end_n):
    cn = tuple(end_n[:2])
    bt = []
    
    while cn!=(0,0):
        bt = [cn] +bt
        if cn not in prev_dict.keys():
            break
        else:
            cn = prev_dict[cn]
    
    return bt
    
def A_star(start, end, rmap, debug=False,trace = False):
    
    cur_node = start + [0,man_dist(start,end)]
    
    if trace: rmap_copy = rmap.copy()
    
    open_list = [cur_node]
    closed_list = []
    prev_dict = {tuple(start):(0,0)}
    
    found = False
    
    
    while not found and len(open_list)>0:
        
        cur_node = open_list[0]
        open_list.pop(0)
        closed_list.append(cur_node[:2])
        
        if trace: rmap_copy[cur_node[0],cur_node[1]]=3
        
        if debug: print(cur_node)
        
        for n_add in [[0,1],[1,0],[-1,0],[0,-1]]:
            new_cord = [cur_node[0] + n_add[0],cur_node[1]+n_add[1]]
            if debug: print(new_cord)
            
            if new_cord in closed_list:
                continue
            curr_neigh = new_cord+[cur_node[2]+1, man_dist(new_cord,end)+cur_node[2]+1]
            prev_dict[tuple(new_cord)] = tuple(cur_node[:2])
            
            # check if new cord is a wall put in closed
            if  0<=new_cord[0] < rmap.shape[0] and 0<=new_cord[1] < rmap.shape[1]:
                
                if rmap[new_cord[0],new_cord[1]] ==1:
                    closed_list.append(new_cord)
                    continue
                    
                elif trace:
                    rmap_copy[new_cord[0],new_cord[1]]=2
            

            if new_cord == end:
                cur_node = curr_neigh
                found=True
                break
            
            if len(open_list)==0:
                open_list.append(curr_neigh)
                continue
            
            if open_list[0][3] > curr_neigh[3]:
                open_list= [curr_neigh] + open_list
                continue
            else:
                open_list.append(curr_neigh)
                
    if not trace:      
        return (prev_dict,cur_node)
    else:
        bt = backtrack(prev_dict,cur_node)
        
        for c in bt:
            if  0<=c[0] < rmap.shape[0] and 0<=c[1] < rmap.shape[1]:
                rmap_copy[c[0],c[1]] =4
        return(rmap_copy)
        
        
if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()