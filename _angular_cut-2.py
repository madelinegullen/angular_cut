import numpy as np

from matplotlib import pyplot as plt

def angular_cut(image, angle, center_x = None, center_y = None, increment = None, stop = None, mute_graph = False, v_min = .01e4, v_max = 1e4, num =1000 ):
    
    
    if mute_graph == False:
        fig, axes = plt.subplots(nrows=2, figsize = (10,10))
        if(center_x != None and center_y != None):
                axes[0].scatter(center_x, center_y, s= 50, c='red')
        
    curr = angle
    data = []
    h = image.shape[0]
    w = image.shape[1]
    while True:
        q = -1
        t = image
        height = t.shape[0]
        width = t.shape[1]
        
        theta = curr*(np.pi)/180

        threshold = np.arctan(height/width)

        row0 = 0 #two endpoints of line at angle theta
        col0 = 0

        row1 = 0
        col1 = 0
        if theta >= np.pi:
            theta = theta - np.pi
            #q = -1
        if theta > threshold or theta <= np.pi - threshold:
            row0 = 0
            row1 = height - 1
            col0 = int((width/2)+(height/2)*np.tan((np.pi/2) - theta))
            col1 = int((width/2)-(height/2)*np.tan((np.pi/2) - theta))
            if col1 >= height:
                col1 -= 1
        if theta <= threshold:
            row0 = int((height/2) - (width/2)*np.tan(theta))
            row1 = int((height/2) + (width/2)*np.tan(theta))
            if row1 >= height:
                row1 -= 1
            col0 = width - 1
            col1 = 0

        if theta > np.pi - threshold:
            row0 = int((height/2) + (width/2)*np.tan(theta))
            row1 = int((height/2) - (width/2)*np.tan(theta))
            col0 = 0
            col1 = width - 1


        #print("r0, c0: ",row0,col0)
        #print("r1, c1: ", row1, col1)
        
        r, c = np.linspace(row0, row1, num), np.linspace(col0, col1, num) #sample 1000 points between endpoints
        im_slice = t[r.astype(np.int), c.astype(np.int)]  #extract data from these indexed locations
        im_slice = im_slice[::q]
        radius = []
        grid = radial_grid(center = (center_y, center_x), shape = (h, w))
        
        for i in range(len(r)):
            p1 = int(r[i])
            p2 = int(c[i])
            rad = grid[p1][p2]
            radius.append(rad)
        radius = radius[::q]
        if mute_graph == False:
            axes[0].imshow(t, vmin= v_min,vmax =  v_max)
            axes[0].plot([col0, col1], [row0, row1], 'ro-')
            axes[0].axis('image')

            #if(center_x != None and center_y != None):
               # axes[0].scatter(center_x, center_y, s= 50, c='red')

            #if mute_graph != True:
            axes[1].plot(radius, im_slice)
        
        data.append((curr, im_slice, radius))
        
        if increment == None:
            break
        if curr + increment > stop:
            break
        curr = curr + increment
    
    if(mute_graph==False and center_x != None and center_y != None):
                axes[0].scatter(center_x, center_y, s= 50, c='red')
    plt.show()
    return idata