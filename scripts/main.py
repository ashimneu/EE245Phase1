#!/usr/bin/env python
import rospy
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from Tkinter import *
import subprocess



class Gui_Main:

    def __init__(self, master):
        # Master Setup
        self.master = master
        self.master.title("Qudrotor Project: Phase 1")
        self.master.bind("<Escape>",quit)
        self.master.bind("1",self.launch_quad2d_window)
        self.master.bind("2",self.launch_quad3d_window)

        # Frame 1 setup
        self.frame1 = Frame(self.master, width=300, height=75)
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.grid_rowconfigure(0, weight=1)
        self.frame1.grid_columnconfigure(0, weight=1)

        # Frame 2 Setup
        self.frame2 = Frame(self.master, width=300, height=75)
        self.frame2.grid_propagate(False)
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame2.grid_rowconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(0, weight=1)

        # Layout Setup
        self.b1 = Button(self.frame1, text="Launch 2D Quadrotor", command=self.launch_quad2d_window)
        self.b1.grid(sticky="we")

        self.b2 = Button(self.frame2, text="Launch 3D Quadrotor", command=self.launch_quad3d_window)
        self.b2.grid(stick="we")



    def launch_quad2d_window(self,*args):
        self.newWindow = Toplevel(self.master)
        childWindow1 = quad2d_class(self.newWindow)
        self.master.withdraw()

    def launch_quad3d_window(self,*args):
        self.newWindow = Toplevel(self.master)
        childWindow2 = quad3d_class(self.newWindow)
        self.master.withdraw()


class quad2d_class():

    def __init__(self, master):
        # Master Setup
        self.master = master
        self.master.title("2D Quadrotor Simulator")
        #self.master.overrideredirect(1) # Disables title bar
        self.master.geometry("800x500")
        self.master.bind("<Escape>",quit)
        self.master.bind("`", self.return2Main)

       # Frame Setup
        self.frame1 = Frame(self.master,bg="White", width=8020, height=800, pady = 80, padx = 20)
        self.frame1.grid(row=0, column=0)
        self.frame1.grid_propagate(False)

        # Layout Setup
        self.btnBack = Button(self.master, text="Back", command=self.return2Main)
        self.btnBack.place(x=0,y=0)
        self.btnQuit = Button(self.master, text="Quit", command=quit)
        self.btnQuit.place(x=743,y=0)

        self.lbl_suggestion0 = Label(self.frame1, text="Input Format:", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion0.place(x=500,y=15)

        self.lbl_initialpose = Label(self.frame1, text="Initial Pose: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_initialpose.place(x=30,y=50)

        self.lbl_tkfheight = Label(self.frame1, text="Takeoff Height: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_tkfheight.place(x=30,y=85)

        self.lbl_hoverpose = Label(self.frame1, text="Hover Pose: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_hoverpose.place(x=30,y=120)

        self.lbl_hovertime = Label(self.frame1, text="Hover Time: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_hovertime.place(x =30, y=155)

        self.lbl_suggestion1 = Label(self.frame1, text=u"y,z,\u03A6", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion1.place(x=500,y=50)

        self.lbl_suggestion2 = Label(self.frame1, text="z", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion2.place(x=500,y=85)

        self.lbl_suggestion3 = Label(self.frame1, text="y,z", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion3.place(x=500,y=120)

        self.lbl_suggestion4 = Label(self.frame1, text="time", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion4.place(x=500,y=155)


        self.entry_initialpose = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_initialpose.place(x =250, y=50)

        self.entry_tkfheight = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_tkfheight.place(x =250, y=85)

        self.entry_hoverpose = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_hoverpose.place(x =250, y=120)

        self.entry_hovertime = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_hovertime.place(x =250, y=155)

        self.btnOk = Button(self.frame1, text="Simulate", command=self.extractInputs, height=5, width=8)
        self.btnOk.place(x=600,y=300)

        # User Inputs for Quadrotor Waypoints
        self.initialpose = 0
        self.tkfheight = 0
        self.hoverpose = 0
        self.hovertime = 0

    def extractInputs(self,*args):
        tmp_initialpose = self.entry_initialpose.get().strip()
        tmp_tkfheight = self.entry_tkfheight.get().strip()
        tmp_hoverpose = self.entry_hoverpose.get().strip()
        tmp_hovertime = self.entry_hovertime.get().strip()

        try:
            self.initialpose = [float(x) for x in tmp_initialpose.split(',')]
            self.tkfheight = float(tmp_tkfheight)
            self.hoverpose = [float(x) for x in tmp_hoverpose.split(',')]
            self.hovertime = float(tmp_hovertime)

            #launch_quad2d([0, 0, 0], 5, [5, 15], 3)
            launch_quad2d(self.initialpose, self.tkfheight, self.hoverpose, self.hovertime)



        except:
            print('One or more inputs are incorrect. Please follow the specified input formats.')

    def return2Main(self,*args):
        print('Exiting 2D Quadrotor Window.')
        root.deiconify()
        self.master.withdraw()


class quad3d_class():

    def __init__(self, master):
        # Master Setup
        self.master = master
        self.master.title("3D Quadrotor Simulator")
        #self.master.overrideredirect(1) # Disables title bar
        self.master.geometry("800x500")
        self.master.bind("<Escape>",quit)
        self.master.bind("`", self.return2Main)

        # Frame Setup
        self.frame1 = Frame(self.master,bg="White", width=8020, height=800, pady = 80, padx = 20)
        self.frame1.grid(row=0, column=0)
        self.frame1.grid_propagate(False)

        # Layout Setup
        self.btnBack = Button(self.master, text="Back", command=self.return2Main)
        self.btnBack.place(x=0,y=0)
        self.btnQuit = Button(self.master, text="Quit", command=quit)
        self.btnQuit.place(x=743,y=0)

        self.lbl_suggestion0 = Label(self.frame1, text="Input Format:", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion0.place(x=500,y=15)

        self.lbl_initialpose = Label(self.frame1, text="Initial Pose: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_initialpose.place(x=30,y=50)

        self.lbl_tkfheight = Label(self.frame1, text="Takeoff Height: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_tkfheight.place(x=30,y=85)

        self.lbl_hoverpose = Label(self.frame1, text="Hover Pose: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_hoverpose.place(x=30,y=120)

        self.lbl_hovertime = Label(self.frame1, text="Hover Time: ", fg="black", font=("Courier", 18), width=17)
        self.lbl_hovertime.place(x =30, y=155)

        self.lbl_suggestion1 = Label(self.frame1, text=u"x,y,z,\u03A6,\u03F4,\u03A8", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion1.place(x=500,y=50)

        self.lbl_suggestion2 = Label(self.frame1, text="z", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion2.place(x=500,y=85)

        self.lbl_suggestion3 = Label(self.frame1, text=u"x,y,z,\u03A8", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion3.place(x=500,y=120)

        self.lbl_suggestion4 = Label(self.frame1, text="time", bg="white", fg="black", font=("Courier", 18), width=17)
        self.lbl_suggestion4.place(x=500,y=155)


        self.entry_initialpose = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_initialpose.place(x =250, y=50)

        self.entry_tkfheight = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_tkfheight.place(x =250, y=85)

        self.entry_hoverpose = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_hoverpose.place(x =250, y=120)

        self.entry_hovertime = Entry(self.frame1, fg="black", font=("Courier", 18))
        self.entry_hovertime.place(x =250, y=155)

        self.btnOk = Button(self.frame1, text="Simulate", command=self.extractInputs, height=5, width=8)
        self.btnOk.place(x=600,y=300)

        # User Inputs for Quadrotor Waypoints
        self.initialpose = 0
        self.tkfheight = 0
        self.hoverpose = 0
        self.hovertime = 0

    def extractInputs(self,*args):
        tmp_initialpose = self.entry_initialpose.get().strip()
        tmp_tkfheight = self.entry_tkfheight.get().strip()
        tmp_hoverpose = self.entry_hoverpose.get().strip()
        tmp_hovertime = self.entry_hovertime.get().strip()

        try:
            self.initialpose = [float(x) for x in tmp_initialpose.split(',')]
            self.tkfheight = float(tmp_tkfheight)
            self.hoverpose = [float(x) for x in tmp_hoverpose.split(',')]
            self.hovertime = float(tmp_hovertime)
            rospy.set_param('/quad3d/initialpose', self.initialpose)
            rospy.set_param('/quad3d/tkfheight', self.tkfheight)
            rospy.set_param('/quad3d/hoverpose', self.hoverpose)
            rospy.set_param('/quad3d/hovertime', self.hovertime)
            launch_Quad3D()
        except:
            print('One or more inputs are incorrect. Please follow the specified input formats.')


    def return2Main(self,*args):
        print('Exiting 3D Quadrotor Window.')
        root.deiconify()
        self.master.withdraw()

def launch_Quad3D():
    global nodeQuad3D
    nodeQuad3D = subprocess.Popen(["rosrun", "phase1", "Quad3D.py"])
def kill_Quad3D():
    global nodeQuad3D
    nodeQuad3D.kill()

class Quad2D():
    def __init__(self):
        self.g = 9.80665  # [meters/sec^2]
        self.m = 0.030  # [kilograms]
        self.l = 0.046  # [meters]
        self.Ixx = 1.43e-5  # [kilogram*meters^2]
        self.Kp = np.array([1,50,1200])
        self.Kd = np.array([1.5,12,self.Kp[2]/8])
        self.yd = np.array([5,15,0,0,0,0,0,0,0])
        self.A = np.array([[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1],[0,0,-self.g,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])   #linearized system matrix
        self.B = np.array([[0,0],[0,0],[0,0],[0,0],[1/self.m,0],[0,1/self.Ixx]])    #linearized input matrix
        self.initialpose = np.asarray([5.0,5.0,np.pi/8,0.0,0.0,0.0])
        self.currentpose = self.initialpose
        self.desiredpose = np.array([15,15,0,0,0,0,0,0,0])
        self.start_time = None
        self.end_time = None
        self.dt = 0.1
        self.pose_trajectory = None
        self.time_trajectory = None

    def xdot_2d(self,y,t,yd,u0,m,g,Ixx,Kp,Kd):
        # CONTROLLER
        e = yd[0:6] - y
        # position controller
        u1 = m * (yd[7] + Kd[1] * e[4] + Kp[1] * e[1])
        theta_d = -1 / g * (yd[6] + Kd[0] * e[3] + Kp[0] * e[0])
        # attitude controller
        u2 = Ixx * (yd[8] + Kd[2] * e[5] + Kp[2] * (theta_d - y[2]))  # add theta_d
        u = np.array([[u1], [u2]]) + u0
        # CLOSED-LOOP DYNAMICS
        #F = np.array([[y[3]], [y[4]], [y[5]], [0], [-self.g], [0]])
        #G = np.array([[0,0], [0,0], [0,0], [(-1/m)*np.sin(y[2]),0], [(1/m)*np.cos(y[2]),0], [0,1/self.Ixx]])
        return np.squeeze(np.matmul(self.A,y.reshape(6,1)) + np.matmul(self.B,u)).tolist()

    def simulate(self):
        x0 = self.currentpose
        u0 = np.array([[self.m * self.g], [0]])
        yd = self.desiredpose
        m = self.m

        # simulation parameters
        ts = self.start_time
        tf = self.end_time
        tstep = self.dt
        t = np.arange(start=ts, stop=tf, step=tstep)
        x = odeint(self.xdot_2d, x0, t, args=(yd,u0,self.m,self.g,self.Ixx,self.Kp,self.Kd))
        self.pose_trajectory= x
        self.time_trajectory = t

    def run_once(self,currentpose,desiredpose,start_time,end_time):
        self.currentpose = currentpose
        self.desiredpose = desiredpose
        self.start_time = start_time
        self.end_time = end_time
        self.simulate()
        return


def launch_quad2d(ip,tkh,hl,ht):
    # ip -initial pose, tkh -takeoff height, hl -hover location, ht -hover time
    Robot = Quad2D()
    dt = 0.005
    cp1 = np.asarray([ip[0], ip[1], ip[2], 0.0, 0.0, 0.0])
    dp1 = np.array([0, tkh, 0, 0, 0, 0, 0, 0, 0])
    t0 = 0
    t1 = 5
    Robot.run_once(cp1, dp1, t0, t0 + t1)
    trajectory_1 = Robot.pose_trajectory
    time_1 = Robot.time_trajectory

    # fly from takeoff 2 hover pose
    cp2 = trajectory_1[-1, 0:6]
    dp2 = np.array([hl[0], hl[1], 0, 0, 0, 0, 0, 0, 0])
    t2 = 5
    Robot.run_once(cp2, dp2, t1 + dt, t1 + t2)
    trajectory_2 = Robot.pose_trajectory
    time_2 = Robot.time_trajectory

    # Hover for some time
    cp3 = trajectory_2[-1, 0:6]
    dp3 = np.array([hl[0], hl[0], 0, 0, 0, 0, 0, 0, 0])
    t3 = ht
    Robot.run_once(cp3, dp3, t2 + dt, t2 + t3)

    trajectory_3 = Robot.pose_trajectory
    time_3 = Robot.time_trajectory

    # Land from Hover pose
    cp4 = trajectory_3[-1, 0:6]
    dp4 = np.array([hl[0], 0, 0, 0, 0, 0, 0, 0, 0])
    t4 = 5
    Robot.run_once(cp4, dp4, t3 + dt, t3 + t4)

    trajectory_4 = Robot.pose_trajectory
    time_4 = Robot.time_trajectory

    x = np.concatenate((trajectory_1, trajectory_2, trajectory_3, trajectory_4), axis=0)
    t = np.concatenate((time_1, time_2, time_3, time_4), axis=0)

    # extract for plotting
    Y = np.array(x)[:, 0]
    Z = np.array(x)[:, 1]
    Theta = np.array(x)[:, 2]

    # plot results
    plt.subplot(2, 2, 1)
    plt.plot(Y, Z, 'b')
    plt.xlabel(r'$y(t)$')
    plt.ylabel(r'$z(t)$')
    plt.xlim(-10, 10)
    plt.ylim(-1, 20)
    plt.grid(True)

    plt.subplot(2, 2, 2)
    plt.plot(t, Y, 'b')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$y(t)$')
    plt.xlim(-1, 15)
    plt.ylim(-5, 15)
    plt.grid(True)

    plt.subplot(2, 2, 3)
    plt.plot(t, Z, 'b')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$z(t)$')
    plt.xlim(-1, 15)
    plt.ylim(-5, 15)
    plt.grid(True)

    plt.subplot(2, 2, 4)
    plt.plot(t, Theta, 'b')
    plt.xlabel(r'$t$')
    plt.ylabel(r'$\phi$')
    plt.xlim(-1, 15)
    plt.ylim(-4, 4)
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    rospy.init_node('Main')
    root = Tk()
    Window1 = Gui_Main(root)
    Window1.master.resizable(width=False, height=False)
    nodeQuad2D = None
    nodeQuad3D = None
    root.mainloop()

