#!/usr/local/bin/python3
#
# Authors: Naga Anjaneyulu, Ruthvik Parvat , Prudhvi Vajja
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019


from PIL import Image
from numpy import * 
import numpy as np
from scipy.ndimage import filters
import sys
import imageio
import math
import copy

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

# main program
    
def part1(edge_strength,emmission_prob):
    simple_ridge = []    
    simple_ridge = argmax(emmission_prob,axis=0)
    #simple_ridge = argmax(edge_strength,axis=0)
    return simple_ridge




def part2(edge_strength,emmission_prob,gt_row,gt_col,part3_flag):
    viterbi_ridge = []
    viterbi_dict ={}
    v0_dict = {}
    if part3_flag :
        emmission_prob[:,gt_col-1:gt_col+1] = -log(math.inf)
        emmission_prob[gt_row,gt_col-1:gt_col+1] = log(pow(10,5))
        
    for i in range(0,edge_strength.shape[0]):
        v0_dict[i] =  emmission_prob[i][0]
    viterbi_dict["v0"] = v0_dict
    for i in range(1,edge_strength.shape[1]):
        v_dict = {}
        for j in range(0,edge_strength.shape[0]):
            max_trans = -math.inf
            trans_prob = 0
            prob_sum = 1
            for k in range(0,emmission_prob.shape[0]):
                if prob_sum > 0:
                    if abs(k-j) <= 3 :
                        trans_prob = 0.1
                        prob_sum -= trans_prob
                    elif 3 < abs(k-j) <= 5:
                        trans_prob = 0.074999925       #0.06666666666 , 4
                        prob_sum -= trans_prob
                    else:
                        trans_prob = 3e-7/(edge_strength.shape[0] - 11) #4.0000003e-11 ,11
                        prob_sum -= trans_prob
                    max_trans = max(max_trans, viterbi_dict["v"+str(i-1)][k] + log(trans_prob))
            v_dict[j] = emmission_prob[j][i] + max_trans
        viterbi_dict["v"+str(i)] = v_dict

    for viterbi,value in viterbi_dict.items():
        max_v = -math.inf
        row_value =0
        for row,value in value.items():
            if value > max_v:
                max_v = value
                row_value = row
        viterbi_ridge.append(row_value)
  
    return viterbi_ridge
    

#Command line arguments
if __name__ =='__main__':
    (input_filename, gt_row, gt_col) = sys.argv[1:]

    # load in image 
    input_image = Image.open(input_filename)
    input_image1 = copy.deepcopy(input_image)
    input_image2 = copy.deepcopy(input_image)
    input_image3 = copy.deepcopy(input_image)
    
    # compute edge strength mask
    edge_strength = edge_strength(input_image)
    imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))
    # You'll need to add code here to figure out the results! For now,
    # just create a horizontal centered line.
    emmission_prob = zeros((edge_strength.shape[0],edge_strength.shape[1]))
    for i in range(0,edge_strength.shape[1]):
            pixel_sum = sum([ pixel for pixel in edge_strength[:,i]])        
            for j in range(0,edge_strength.shape[0]):
                if edge_strength[j][i] > 0:
                    emmission_prob[j][i] = log(edge_strength[j][i]/pixel_sum)
                else :
                    emmission_prob[j][i] = -log(math.inf)
    simple_ridge = part1(edge_strength,emmission_prob)
    viterbi_ridge = part2(edge_strength,emmission_prob,0,0,False)
    man_ridge = part2(edge_strength,emmission_prob,int(gt_row),int(gt_col),True)
    imageio.imwrite("output_simple.jpg", draw_edge(input_image1, simple_ridge, (0, 0, 255), 5))
    imageio.imwrite("output_map.jpg", draw_edge(input_image2, viterbi_ridge, (255, 0, 0), 5))
    imageio.imwrite("output_human.jpg", draw_edge(input_image3, man_ridge, (0, 255, 0), 5))




    
        

            

