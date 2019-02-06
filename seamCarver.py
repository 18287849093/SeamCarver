#Colin Evans
#Seam Carving Algorithm for compressing images

from skimage import filters, util, io, color
import numpy as np
import math as m
from matplotlib import pyplot as plt

#Finds the energy of each pixel and returns that in a 2d array so that the least energy seam can be found
def dual_gradient_energy(img):
    #Returns a W x H array of floats, the energy at each pixel in img
    
    #vertical and horizontal filters combined
    energy_h = filters.sobel_h(img)
    energy_v = filters.sobel_v(img)
    
    #gets the numbers for the size of the image
    height, width = energy_h.shape
    
    #computes the combined sobel filter for the image
    energy = [[m.sqrt((energy_h[j][i] ** 2) + (energy_v[j][i] ** 2)) for i in range(width)] for j in range(height)]
    
    return energy
        
    
    
#using the energy provided, finds the seam that has the smallest amount of energy
#Returns an array of the indexes of each pixel in that row to be removed.
def find_seam(img):
    #Returns an array of H integers, for each row return the column of the seam
    height = len(img)
    width = len(img[0])
    
    #Creates the list for the seam
    seam = [-1 for _ in range(height)]
    
    
    #Finds the minimum for that pixel
    for y in range(2, height - 1): #because it's padded
        for x in range(1, width - 1): #because it's padded
            #calculates the cumulative sum of energies leading up to and including that pixel
            minimum = min([img[y-1][max(x-1, 1)], img[y-1][x], img[y-1][min(x+1, width - 2)]])
            img[y][x] = img[y][x] + minimum
            
            
    
    #Gets the minimum value for the last (non-padded) row
    mini = min(img[height - 2][1:width - 1])
    seam[height - 1] = img[height - 2].index(mini)
    #copies over the second to last row into the last row so that you don't forget about the padding pixel when removing
    seam[height - 2] = seam[height - 1]
    
    #backtracking up the list so that we can find the seam
    for y in reversed(range(1, height - 2)):
        minim = min([img[y][max(seam[y + 1] - 1, 1)], img[y][seam[y + 1]], img[y][min(seam[y + 1] + 1, width - 2)]])
        
        #finds all occurances of the minimum in the list
        indices = [i for i, x in enumerate(img[y]) if x == minim]
        for i in indices:
            #Checks to see if that value is above or diagonal of the one we added to the seam
            if seam[y + 1] == i - 1 or seam[y + 1] == i or seam[y + 1] == i + 1:
                seam[y] = i
    #Adds the value in index 1 to index 0 to deal with the padding    
    seam[0] = seam[1]
    
    return seam
    
    
        

#Provides a visual representation of what the image looks like initially, what it looks like
#after the seam has been decided, and then an image of what the energy of the image looks like
def plot_seam(img, seam):
    #your own visualization of the seam, img, and energy fuc.
   
    #Creates a copy of the image that will remain without the seam showing
    imgNoSeam = img.copy()
    #turns the image into greyscale to run the energy function
    greyImg = color.rgb2gray(img)
    #gets the energy so we can display it to the user
    energy = dual_gradient_energy(greyImg)
    #turns the image into an np array to work in the loop below
    energy = np.array(energy)
       
    #adds the seam to the image
    for i in reversed(range(len(img) - 2)):
        img[i][seam[i]] = np.array([1,0,0])
    
    
    #creates a list of images to be displayed
    images = [imgNoSeam, img, energy]
    
    cols = 1
    titles = ['Image (%d) ' % i for i in range(1, 4)]
    fig = plt.figure()
    num_images = len(images)
    
    #loops through each image adding a title and displaying it to the user
    for n, (image, title) in enumerate(zip(images, titles)):
        a = fig.add_subplot(cols, np.ceil(num_images/float(cols)), n + 1)
        if image.ndim == 2:
            plt.gray()
        plt.imshow(image)
        a.set_title(title)
    fig.set_size_inches(np.array(fig.get_size_inches()) * num_images)
    plt.show()   

    

#removes the seam of pixels from the image
def remove_seam(img, seam):
    #modify img in-place and returns a W-1 x H X 3 slice
    # use del, index by row
    new_img = img.tolist()
    height = len(img)
    
    for i in range(height):
        del new_img[i][seam[i]]
        
    return np.array(new_img)
    
    
def main():
    img = io.imread('test.jpg')

#    grey = color.rgb2gray(io.imread('test.jpg'))
#    energy = dual_gradient_energy(grey)
#    seam = find_seam(energy)
#    plot_seam(img, seam)

    
#    plt.imshow(img, cmap='gray')
#    plt.show()
    
    #removes 10 seams
    for i in range(10):
        grey1 = color.rgb2gray(img)
        energy1 = dual_gradient_energy(grey1)
        seam1 = find_seam(energy1)
        img = remove_seam(img, seam1)
    
    plt.imshow(img, cmap='gray')
    plt.show()
    

if __name__ == '__main__':
    main()
