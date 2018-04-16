import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #even tho idk about drawing bounding here
# perhaps can just get good perspective, and open image in matlab to draw ... ?
from math import sin, cos
from matplotlib.widgets import Slider, Button, RadioButtons

hz = 3
hy = 10
hx = 10
theta = 0.5

'''store video properties in a class to have unified access '''
class Video_Properties:
    height = 0
    width = 0
    time_range = []
    def __init__(self, height,width,time_range):
        self.height = height+1 #idk really if this is right ... 
        self.width = width+1 
        self.time_range = time_range

""" proj_func are user defined functions to calculate x' and y' on dataframe """        
def proj_func_x(x,y,t):
    global hz, hy, hx, theta,my_vid_properties
    myt = np.where(my_vid_properties.time_range == t)
    xprime = x - (myt[0][0]+1)*(hx + (hz+1)*(cos(theta)*x-sin(theta)*y) -x) #do x10 to exxag differences in height
    return xprime

def proj_func_y(x,y,t):
    global hz, hy, hx, theta,my_vid_properties
    myt = np.where(my_vid_properties.time_range == t)
    yprime = y - (myt[0][0]+1)*(hy + (hz+1)*(cos(theta)*x+sin(theta)*y) -y)
    return yprime

def display_frames_stack(df,my_vid_properties):
    global hx,hy,theta,hz
    mint = my_vid_properties.time_range[0]
    maxt = my_vid_properties.time_range[1000]
    mytime_df = df.loc[(df["time"] >= mint) & (df["time"] <= maxt)]
    mytime_df['x_prime'] = mytime_df.apply(lambda d: proj_func_x(d['x'],d['y'],d['time']),axis=1)
    mytime_df['y_prime'] = mytime_df.apply(lambda d: proj_func_y(d['x'],d['y'],d['time']),axis=1)
    #print mytime_df
    return mytime_df

def calc_proj_list(x_list,y_list,t_list):
    xproj_list = [proj_func_x(x,y,t) for x,y,t in zip(x_list,y_list,t_list)]
    yproj_list = [proj_func_y(x,y,t) for x,y,t in zip(x_list,y_list,t_list)]
    return xproj_list,yproj_list

def update(val):
    global hz, hy, hx, theta
    hx = hx_slider.val
    hy = hy_slider.val
    hz = hz_slider.val
    theta = theta_slider.val

    
    w = my_vid_properties.width
    h = my_vid_properties.height
    tmin = my_vid_properties.time_range[0]
    tmax = my_vid_properties.time_range[1000] #make this variable
    """
    #x_list = [0,0,w,w,0,  0, 0,0,0, w,w,w, w,w,w, 0,0]
    #y_list = [0,h,h,0,0,  0, h,h,h h,h,h, 0,0,0, 0,0]
    #t_list = [tmin,tmin,tmin,tmin,tmin,
              #tmax, tmax,tmin,tmax, tmax,tmin,tmax, tmax,tmin,tmax, tmax,tmin]
    """
    x_list = [0,0,w,w,0,  0, 0, w, w, 0]
    y_list = [0,h,h,0,0,  0, h, h, 0, 0]
    t_list = [tmin,tmin,tmin,tmin,tmin, tmax,tmax,tmax,tmax,tmax]
    xproj_list,yproj_list = calc_proj_list(x_list,y_list,t_list)
    #box.set_ydata(yproj_list)
    #box.set_xdata(xproj_list)
    print xproj_list
    ax.set_ylim([min(yproj_list),max(yproj_list)])
    ax.set_xlim([min(xproj_list),max(xproj_list)])
    

    mytime_df = display_frames_stack(df,my_vid_properties)
    #print(mytime_df)
    x = mytime_df["x_prime"].tolist()
    y = mytime_df["y_prime"].tolist()
    xx = np.vstack((x,y))
    l.set_offsets(xx.T) 
    fig.canvas.draw_idle()
    
    
def main():
    # reading/setting up data
    #df = pd.read_csv("datasets/yosemite.txt", sep =" ",header=None)
    chunksize = 10 ** 6
    i = 0
    for chunk in pd.read_csv("events.txt", sep = " ", header=None, chunksize=chunksize):
        i += 1
        if i ==2:
            break
    df = chunk
    
    df.columns = ["time","x","y","light_change"]
    df = df.drop(labels="light_change",axis=1) #remove light change data for now
    
    height = df['y'].max() # this is not necessarily correct .... but how else to tell?
    width = df['x'].max()
    time_range = df["time"].unique()
    my_vid_properties = Video_Properties(height,width,time_range)

    #showing layers of frames with dif parameters
    global hz, hy, hx, theta
    # i really dont think these globals are a good idea but whatever i guess
    global fig, ax, hx_slider, hy_slider,hz_slider,theta_slider, df, my_vid_properties, l , box

    fig,ax = plt.subplots()
    fig.subplots_adjust(left=0.25, bottom=0.25)
    axis_color = 'lightgoldenrodyellow'
    
    # make sliders
    hx_slider_ax  = fig.add_axes([0.25, 0.2, 0.65, 0.03], axisbg=axis_color)
    hy_slider_ax = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color)
    hz_slider_ax  = fig.add_axes([0.25, 0.1, 0.65, 0.03], axisbg=axis_color)
    theta_slider_ax = fig.add_axes([0.25, 0.05, 0.65, 0.03], axisbg=axis_color)
    hx_slider = Slider(hx_slider_ax, 'hx', -1000, 1000.0, valinit=hx)
    hy_slider = Slider(hy_slider_ax, 'hy', -1000, 1000.0, valinit=hy)
    hz_slider = Slider(hz_slider_ax, 'hz', -0.1, 100.0, valinit=hz)
    theta_slider = Slider(theta_slider_ax, 'theta', -0.1, 7.0, valinit=theta)
    hx_slider.on_changed(update)
    hy_slider.on_changed(update)
    hz_slider.on_changed(update)
    theta_slider.on_changed(update)
    mytime_df = display_frames_stack(df,my_vid_properties)
    l = ax.scatter(mytime_df["x_prime"],mytime_df["y_prime"],c=mytime_df["time"])

    """
    w = my_vid_properties.width
    h = my_vid_properties.height
    tmin = my_vid_properties.time_range[0]
    tmax = my_vid_properties.time_range[1000] #make this variable
    x_list = [0,0,w,w,0,  0,0,w,w,0]
    y_list = [0,h,h,0,0,  0,h,h,0,0]
    t_list = [tmin,tmin,tmin,tmin,tmin,
              tmax,tmax,tmax,tmax,tmax]

    xproj_list,yproj_list = calc_proj_list(x_list,y_list,t_list)
    ax.set_ylim([min(yproj_list),max(yproj_list)])
    ax.set_xlim([min(xproj_list),max(xproj_list)])
    box, = ax.plot(xproj_list,yproj_list)
    """
    
    plt.show()

    
if __name__ == "__main__":
    main()
    
