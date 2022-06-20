# ToucanPi: We wanted to visualize the tracjectory of ISS with its orientation.
# This is partially completed.

#This part is something we are playing with but does not work on collaboratory. It is based on
# https://chart-studio.plotly.com/~empet/15666/roll-pitch-and-yaw-motion-of-an-airplan/#/

#But fails at the last step. We wanted to animate an aeroplane based on Yaw.

#this change allows it to work:
#from plotly.offline import iplot
#iplot(fig, filename='yaw-roll-motion')

 
import plotly.express as px
import plotly.graph_objs as go
#general
import numpy as np
import math

myfilename="../toucanpi/toucandata_20220513_201103.csv"
import pandas as pd
mydata = pd.read_csv(myfilename,parse_dates={ 'newdate': ['Date/Time'] })


#!pip install meshio
import meshio
from numpy import pi, cos, sin, sqrt

def rotx(t):
    return np.array([[1, 0, 0], [0, cos(t), -sin(t)], [0, sin(t), cos(t)]])

def roty(t):
    return np.array([[cos(t), 0, sin(t)],  [0, 1, 0],[-sin(t), 0, cos(t)]])   
    
def rotz(t):
    return np.array([[cos(t), -sin(t), 0], [sin(t), cos(t), 0], [0, 0, 1]])
from urllib.request import urlopen
url = 'http://people.sc.fsu.edu/~jburkardt/data/ply/airplane.ply'
data = urlopen(url)


mesh = meshio.read(data, file_format='ply')  
points = rotz(5*pi/6).dot(mesh.points.T)
points.shape
from  IPython.display import Image
Image(url='https://raw.githubusercontent.com/empet/Datasets/master/Images/plane-1.png')
D = np.array([-1283.45876179,  -431.01578484,    63])
x0, y0, z0 = D
u1 = np.array([sqrt(3)/2, -0.5, 0 ])
u2 = np.array([0.5, sqrt(3)/2, 0])
u3 = np.cross(u1, u2)
A = np.array([u1,u2,u3]) #T_{B'B}   B'=(u1, u2, u3), A is the matrix of transition from 
                         #the orthonormal basis, B', to the standard basis in the 3d space
A

def rotate(points, D, A,  phi, rot=rotz):
    #points - array of shape (n, 3); they give the initial position of the airplane points
    #D - aray of shape (3,), the origin of the linear frae tied to the airplane; D was defined aboeve
    # A - array of shape (3, 3);  A = np.array([u1,u2,u3])
    # phi - the angle of rotation in radians
    # rot - one of the functions rotx, roty, rotz that returns  the rotation matrix of angle phi;
    # rotx, roty, roz define respectively: the roll, pitch and yaw motion
    
    points_n = np.dot(A, (points-D).T) # express the airplane points with respect to the linear frame (D; u1, u2, u3)
    p_rotated = rot(phi).dot(points_n) #airplane points rotated and expressed with respect to (D; u1, u2, u3)
    return ((A.T).dot(p_rotated)).T  + D   # returns rotated points of shape (n, 3)) and of coords 
                                           # with respect to the standard linear frame (O; i, j, k)
   
x, y, z = points
I, J, K = mesh.cells[0].data.T
gr= [[0, 'rgb(150, 150, 150)'], 
     [1, 'rgb(150, 150, 150)']]
fig = go.Figure(go.Mesh3d(
            x=x,
            y=y, 
            z=z, 
            i=I, 
            j=J, 
            k=K, 
            colorscale=gr,
            showscale=False,
            intensity=z,
            lighting=dict(ambient=0.5,
                          diffuse=1,
                          fresnel=4,        
                          specular=0.5,
                          roughness=0.5),
            lightposition=dict(x=100,
                               y=100,
                               z=1000
            )))


fig.update_layout(title_text='', title_x=0.5, title_y=0.8, 
                  width=800, height=800,scene_aspectmode='data', 
                  scene_xaxis_visible=False,  scene_yaxis_visible=False,
                  scene_zaxis_visible=False,
                  scene_camera_eye=dict(x=1.35,y=1.35, z=0.5));

frames=[]
#mylist = range(0,len(mydata.OrientYaw),100) #to use a smaller subset
mylist = range(0,len(mydata.OrientYaw),1)
for k in range(len(mylist)):
    x, y, z = rotate(points.T, D, A,  mydata.OrientYaw[k]*180/math.pi, rot=rotz).T
    frames.append(go.Frame(data=[go.Mesh3d(x=x,y=y,z=z)],
                           layout=dict(title_text='Yaw motion at ' + 'Lat ' + str(mydata.Lat[k]) + '& Long ' + str(mydata.Long[k])),
                           traces=[0]))

print(k)

fig.update_layout(updatemenus=[dict(type='buttons',
                                  showactive=False,
                                  y=0.1,
                                  x=1.05,
                                  xanchor='left',
                                  yanchor='top',
                                  #pad=dict(t=1),
                                  buttons=[dict(label='Play',
                                                method='animate',
                                                args=[None, dict(frame=dict(duration=50, redraw=True), 
                                                                 transition_duration=0,
                                                                 fromcurrent=True,
                                                                 mode='immediate'
                                                                 )])
                                          ]
                                  )])   
fig.update(frames=frames);

#!pip install chart-studio 

#import chart_studio.plotly as pyc
from plotly.offline import iplot
#cf.go_offline() #will make cufflinks offline
#cf.set_config_file(offline=False, world_readable=True)
#pyc.iplot(fig, filename='yaw-roll-motion')
iplot(fig, filename='yaw-roll-motion')

