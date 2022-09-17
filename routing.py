import picar_4wd as fc
import numpy as np
import pandas as pd


import picar_4wd as fc
speed = 10
us_step = 5
scan_angle_max = 90
scan_angle_max = -90

def main():
    while True:
        scan_list = fc.scan_step(35)
    if not scan_list:
        continue
    tmp = scan_list[3:7]
    print(tmp)
    if tmp != [2,2,2,2]:
        fc.turn_right(speed)
    else:
        fc.forward(speed)
    
    
if __name__ == "__main__":
    try:
        main()
    finally:
        fc.stop()
        
        
        
def get_distance_at(angle):
    global angle_distance
    servo.set_angle(angle)
    time.sleep(0.04)
    distance = us.get_distance()
    angle_distance = [angle, distance]
    return distance
    
    
def scan_step_dist(scan_angle_max = 90,scan_angle_min = -90,scan_step =5):

    fc_stop
    
    scan_angle_max = min([scan_angle_max,90])
    scan_angle_min = max([scan_angle_min,-90])
    
    dist_list = []
    
    for ang in range(scan_angle_min,scan_angle_max, scan_step):
        
        cdt = get_distance_at(current_angle)# get distance
        xy = [cdt*np.cos(ang),cdt*np.sin(ang)] # convert to grid
        dist_list.append(xy)
    
    return (dist_list)

    
    
#def map_space():
   # dl = scan_step_dist


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