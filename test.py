############## MAIN SETTINGS ##################
w,h = 600,400
scale = 100
eye_separation = 0.0
eye_distance = 6
###############################################
######### Import the libraries we need ########
try:
    # Python2
    from Tkinter import Tk, Canvas, PhotoImage, mainloop
except ImportError:
    # Python3 - Note Tkinter has become tkinter!!
    from tkinter import Tk, Canvas, PhotoImage, mainloop

############## FUNCTION DEFINITIONS ###########

def triangle(a,b,c,colour,img):
    #a,b,c are points (given as (x,y) coordinates
    #colour is a string '#aabbcc', where aa is the red intensity, bb is green, and cc is blue
    #intensities are between 0 and 255 given in hexadecimal
    #img is the image to add the triangle to

    #Slightly improved - now it draws a whole line at a time, rather than every point.
    vertices=[a,b,c]
    vertices.sort(key=lambda t: t[1])
    for y in range (vertices[0][1],vertices[1][1]):
        x1 = int((y-vertices[0][1])*(vertices[1][0]-vertices[0][0])/(vertices[1][1]-vertices[0][1])+vertices[0][0])
        x2 = int((y-vertices[0][1])*(vertices[2][0]-vertices[0][0])/(vertices[2][1]-vertices[0][1])+vertices[0][0])
        length=(max(x1,x2)-min(x1,x2))
        if length>0:
            line = '{' + " ".join([colour] * length) + '}'
            img.put(line,(min(x1,x2),y))
        img.put('#000000',(x1,y))
        img.put('#000000',(x2,y))           
        img.put('#000000',(x1+1,y))
        img.put('#000000',(x2+1,y))           
    for y in range (vertices[1][1],vertices[2][1]):
        x1 = int((y-vertices[1][1])*(vertices[2][0]-vertices[1][0])/(vertices[2][1]-vertices[1][1])+vertices[1][0])
        x2 = int((y-vertices[0][1])*(vertices[2][0]-vertices[0][0])/(vertices[2][1]-vertices[0][1])+vertices[0][0])
        length=(max(x1,x2)-min(x1,x2))
        if length>0:
            line = '{' + " ".join([colour] * length) + '}'
            img.put(line,(min(x1,x2),y))
        img.put('#000000',(x1,y))
        img.put('#000000',(x2,y))           
        img.put('#000000',(x1+1,y))
        img.put('#000000',(x2+1,y))
    # the last two elements add vertical boundary lines if needed
    if vertices[0][1]==vertices[1][1]:
        for x in range(min(vertices[0][0],vertices[1][0]),max(vertices[0][0],vertices[1][0])):
            img.put('#000000',(x,vertices[0][1]))            
    if vertices[2][1]==vertices[1][1]:
        for x in range(min(vertices[2][0],vertices[1][0]),max(vertices[2][0],vertices[1][0])):
            img.put('#000000',(x,vertices[1][1]))
    
            
def project_point(a,eye):
    # turn xyz coordinates into xy projection at z=0
    # a is a point given as (x,y,z)
    # eye is left or right, which affects the projection
    (x,y,z)=(a[0],a[1],a[2])
    projected_y=h/2+int(y*scale*eye_distance/(z+eye_distance))
    if eye == 'left':
        projected_x=w/2+int(((x+eye_separation)*eye_distance/(z+eye_distance)-eye_separation)*scale)
    else:
        projected_x=w/2+int(((x-eye_separation)*eye_distance/(z+eye_distance)+eye_separation)*scale)
    return (int(projected_x),int(projected_y))



############## MAIN CODE ######################
window = Tk()
canvas = Canvas(window, width=w, height=h, bg='White')
canvas.pack()

# Create 3 blank images size w by h
left_image = PhotoImage(width=w, height=h)
right_image = PhotoImage(width=w, height=h)
combined_image = PhotoImage(width=w, height=h)
left_image.put("{White}", to=(1,1,w,h))
right_image.put("{White}", to=(1,1,w,h))

# The data for the cube
# vertices are (x,y,z) tuples
# triangles are (a,t,u,v) tuples - a will be used later,
# t,u,v are the indices of the three verticies making the corners of the triangle.
vertices = [(-1.0,-1.0,-1.0),(-1.0,-1.0,1.0),(-1.0,1.0,1.0),(-1.0,1.0,-1.0),(1.0,-1.0,-1.0),(1.0,-1.0,1.0),(1.0,1.0,1.0),(1.0,1.0,-1.0)]
triangles = [(3,0,1,2),(3,0,2,3),(3,2,3,7),(3,2,7,6),(3,1,2,5),(3,2,5,6),(3,0,1,4),(3,1,4,5),(3,4,5,6),(3,4,6,7)]

# Call our function to draw each triangle
for t in triangles:
    (a,b,c)=(vertices[t[1]],vertices[t[2]],vertices[t[3]])
    triangle(project_point(a,'left'),project_point(b,'left'),project_point(c,'left'),'#%02x%02x%02x' % (200,200,200),left_image)
    triangle(project_point(a,'right'),project_point(b,'right'),project_point(c,'right'),'#%02x%02x%02x' % (200,200,200),right_image)

# merge the images and display them
pixel_grid=''
for y in range(h):
    row_colours="{ " # this will be a list of colours for each row of the image
    for x in range(w):
        left=left_image.get(x,y)# this gets the colour of the (x,y) pixel in the left image
        right=right_image.get(x,y)# this gets the colour of the (x,y) pixel in the right image
        row_colours=row_colours+'#%02x%02x%02x' % (int(left[0]),int(right[1]),int(right[2]))+' ' # this combines the red from the left and the green and blue from the right
    row_colours=row_colours+"} "
    pixel_grid=pixel_grid+row_colours # add the row of colours to our grid   
combined_image.put(pixel_grid) #put all the combined pixel colours on the image
canvas.create_image((w/2, h/2), image=combined_image, state="normal") # add the image to the canvas
mainloop()
