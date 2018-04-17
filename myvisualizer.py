import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos
from matplotlib.widgets import Slider, Button, RadioButtons
from optparse import OptionParser
import sys

'''store video properties in a class '''
class Video_Properties:
    height = 0
    width = 0
    time_range = []
    def __init__(self, height,width,time_range):
        self.height = height+1  
        self.width = width+1 
        self.time_range = time_range
       
class MyVisualizer:
    param_dict = {"hx":0, "hy":0, "hz":0, "theta":0}
    mint_ind = 0
    maxt_ind = 100
    my_vid_properties = None
    df = None
    hx_slider = None
    hy_slider = None
    hz_slider = None
    theta_slider = None
    fig = None
    ax = None
    my_scatter = None

    def __init__(self,df,param_dict = None, mint_ind = 0, maxt_ind=100):
        if param_dict != None:
            self.param_dict = param_dict

        self.mint_ind = mint_ind
        self.maxt_ind = maxt_ind
        
        # making my_vid_properties
        height = df['y'].max()
        width = df['x'].max()
        time_range = df["time"].unique()
        self.my_vid_properties = Video_Properties(height,width,time_range)
        
        self.df = df
        self.init_plot_items()
        
    def init_plot_items(self):
        # define plot look
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(left=0.25, bottom=0.25)
        axis_color = 'lightgoldenrodyellow'

        # make sliders
        # give position on plot
        hx_slider_ax  = self.fig.add_axes([0.25, 0.2, 0.65, 0.03], axisbg=axis_color)
        hy_slider_ax = self.fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axis_color)
        hz_slider_ax  = self.fig.add_axes([0.25, 0.1, 0.65, 0.03], axisbg=axis_color)
        theta_slider_ax = self.fig.add_axes([0.25, 0.05, 0.65, 0.03], axisbg=axis_color)
        # define start and end etc
        self.hx_slider = Slider(hx_slider_ax, 'hx', -10.0, 10.0, valinit=self.param_dict["hx"])
        self.hy_slider = Slider(hy_slider_ax, 'hy', -50.0, 50.0, valinit=self.param_dict["hy"])
        self.hz_slider = Slider(hz_slider_ax, 'hz', -50.0, 50.0, valinit=self.param_dict["hz"])
        self.theta_slider = Slider(theta_slider_ax, 'theta', -3.5, 3.5, valinit=self.param_dict["theta"])
        # update graph when slider changes
        self.hx_slider.on_changed(self.update)
        self.hy_slider.on_changed(self.update)
        self.hz_slider.on_changed(self.update)
        self.theta_slider.on_changed(self.update)

        # display original scatter plot
        mytime_df = self.get_event_cloud()
        self.my_scatter = self.ax.scatter(mytime_df["x_prime"],mytime_df["y_prime"],c=mytime_df["time"])
        plt.show() 
        
    """ proj_func are user defined functions to calculate x' and y' on dataframe """        
    def proj_func_x(self,x,y,t):
        xprime = x -t*(self.param_dict["hx"] + (self.param_dict["hz"]+1)*(cos(self.param_dict["theta"])*x-sin(self.param_dict["theta"])*y) -x) 
        return xprime

    def proj_func_y(self,x,y,t):
        yprime = y - t*(self.param_dict["hy"] + (self.param_dict["hz"]+1)*(cos(self.param_dict["theta"])*x+sin(self.param_dict["theta"])*y) -y)
        return yprime

    """ gets the projection coordinates of all points in our time range """
    def get_event_cloud(self):
        mint = self.my_vid_properties.time_range[self.mint_ind]
        maxt = self.my_vid_properties.time_range[self.maxt_ind]
        mytime_df = self.df.loc[(self.df["time"] >= mint) & (self.df["time"] <= maxt)]
        mytime_df['x_prime'] = mytime_df.apply(lambda d: self.proj_func_x(d['x'],d['y'],d['eq_sep_time']),axis=1)
        mytime_df['y_prime'] = mytime_df.apply(lambda d: self.proj_func_y(d['x'],d['y'],d['eq_sep_time']),axis=1)
        return mytime_df

    def calc_bound_proj_list(self):
        # allow us to always be in bounds,showing good area
        w = self.my_vid_properties.width
        h = self.my_vid_properties.height
        x_list = [0,0,w,w,0,  0,0,w,w,0]
        y_list = [0,h,h,0,0,  0,h,h,0,0]
        t_list = [self.mint_ind,self.mint_ind,self.mint_ind,self.mint_ind,self.mint_ind,
                  self.maxt_ind,self.maxt_ind,self.maxt_ind,self.maxt_ind,self.maxt_ind,]
        xproj_list = [self.proj_func_x(x,y,t) for x,y,t in zip(x_list,y_list,t_list)]
        yproj_list = [self.proj_func_y(x,y,t) for x,y,t in zip(x_list,y_list,t_list)]
        return xproj_list,yproj_list

    def update(self, val):
        self.param_dict["hx"] = self.hx_slider.val
        self.param_dict["hy"] = self.hy_slider.val
        self.param_dict["hz"] = self.hz_slider.val
        self.param_dict["theta"] = self.theta_slider.val

        # reset axis limits to scale with projections
        xproj_list,yproj_list = self.calc_bound_proj_list()
        self.ax.set_ylim([min(yproj_list),max(yproj_list)])
        self.ax.set_xlim([min(xproj_list),max(xproj_list)])

        #display other perspective
        mytime_df = self.get_event_cloud()
        x = mytime_df["x_prime"].tolist()
        y = mytime_df["y_prime"].tolist()
        xx = np.vstack((x,y))
        self.my_scatter.set_offsets(xx.T) 
        self.fig.canvas.draw_idle()
    
    
def main():
    # reading/setting up data
    chunksize = 10 ** 6
    for chunk in pd.read_csv("yosemite.txt", sep = " ", header=None, chunksize=chunksize):
        break
    df = chunk
    
    # putting data into format we'd like
    df.columns = ["time","x","y","light_change"]
    df = df.drop(labels="light_change",axis=1) 
    df = df.assign(eq_sep_time=(df['time']).astype('category').cat.codes) #make new column id to tell time in constant growing manner


    # do optparse things
    start_time_ind  = 0
    end_time_ind = 50
    parser = OptionParser()
    parser.add_option("-s","--start_ind",action="store", type ="int",dest = "mint_ind")
    parser.add_option("-e","--end_ind",action="store", type ="int",dest = "maxt_ind")
    (options,args) = parser.parse_args(sys.argv[1:])
    mint_ind = options.mint_ind
    maxt_ind = options.maxt_ind
    if mint_ind == None:
        mint_ind = 0
    if maxt_ind == None:
        maxt_ind = 50
    
    my_visualizer = MyVisualizer(df,param_dict = {"hx":0, "hy":0, "hz":0, "theta":0}, mint_ind = mint_ind,maxt_ind = maxt_ind)
    
if __name__ == "__main__":
    main()
    
