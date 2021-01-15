import numpy as np
import tkinter as tk
import matplotlib.pylab as plt
from matplotlib.widgets import Slider
import matplotlib.widgets as widgets
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from matplotlib import animation


class Oscillator:
    """
    Initialises variables and
    functions to be used later on."""

    def __init__(self):
        self.pause = False  # Initialization for later use
        self.frequency = 1
        self.initfrequency = 1
        self.phase = 0
        self.initphase = 0
        self.n = 1001  # Stepsize for x-axis spread.
        self.damp = 0  # Damping Coefficient initially
        self.amplitude = 1
        self.omega = 2 * np.pi  # Omega as a constant
        self.t = np.linspace(0, 2, self.n)  # Time (x-axis)
        """ List of functions for the different plots."""
        self.func_list = [lambda t: self.amplitude * np.cos(self.omega * t * self.frequency + self.phase), lambda t: self.amplitude * np.sin(self.omega * t * self.frequency + self.phase), lambda t: -self.amplitude
                          * np.cos(self.omega * t * self.frequency + self.phase)]

        self.sinusoids = [lambda t: np.cos(
            self.omega * t), lambda t: np.sin(self.omega * t)]
        self.KE = 0.5 * (1 - (self.sinusoids[0](self.t))**2)
        self.PE = 0.5 * (self.sinusoids[0](self.t))**2

    def PlotAxesMotion(self):
        """
        Plot functions for the widet
        """
        self.ylimit = self.amplitude * 2
        self.data, = self.ax.plot(
            self.t, self.amplitude * np.exp(-self.damp * self.t) * self.func_list[0](self.t + self.phase))
        self.data1, = self.ax1.plot(
            self.t, self.amplitude * np.exp(-self.damp * self.t) * self.func_list[1](self.t + self.phase))
        self.data2, = self.ax2.plot(
            self.t, self.amplitude * np.exp(-self.damp * self.t) * self.func_list[2](self.t + self.phase))
        self.ax.set_title(r'Simple Harmonic Motion')
        self.ax.set_ylabel(r'Position ($m$)')
        self.ax.set_xlabel(r'Time ($s$)')
        self.ax1.set_ylabel(r'Velocity ($\frac{m}{s}$)')
        self.ax1.set_xlabel(r'Time ($s$)')
        self.ax2.set_ylabel(r'Acceleration ($\frac{m}{s^2}$)')
        self.ax2.set_xlabel(r'Time ($s$)')
        self.ax.grid(True, lw=2, ls='--', c='.75')
        self.ax1.grid(True, lw=2, ls='--', c='.75')
        self.ax2.grid(True, lw=2, ls='--', c='.75')
        self.ax.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax1.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax2.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)

    def PlotAxesEnergy(self):
        self.data3, = self.ax3.plot(
            self.t, self.KE - 0.25, '--', label="Kinetic Energy")
        self.data4, = self.ax3.plot(
            self.t, self.PE, '-', label="Potential Energy")
        self.data5, = self.ax3.plot(
            self.t, 0.25 * np.ones_like(self.t), label="Total Energy")
        self.ax3.set_title('SHM Energy Oscilator')
        self.ax3.set_xlabel(r'Displacement ($m$)')
        self.ax3.set_ylabel(r'Energy ($J$)')
        self.ax3.axes.get_xaxis().set_ticks([])
        self.ax3.axes.get_yaxis().set_ticks([])
        self.ax3.grid(True, lw=2, ls='--', c='.75')
        self.ax3.legend(loc=1)
        self.ax3.set_xlim(0.125, 0.375)
        self.ax3.set_ylim(0, 0.30)

    def ClearAxesMotion(self):
        """Clearning axes"""
        self.ax.clear()
        self.ax1.clear()
        self.ax2.clear()
        self.ax.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax1.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax2.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)

    def ClearAxesEnergy(self):
        self.ax3.clear()

    """ Initialization functions for the animate-functions."""

    def initMotion(self):
        self.PlotAxesMotion()
        return self.ax, self.ax1, self.ax2,

    def initEnergy(self):
        self.PlotAxesEnergy()
        return self.ax3,

    """Animating the plots"""

    def animateMotion(self, animate_time):
        if self.pause != True:
            self.ClearAxesMotion()
            self.ax.plot(self.t, self.amplitude * np.exp(-self.damp * self.t) *
                         self.func_list[0]((self.t - 0.05 * animate_time) + self.phase))
            self.ax1.plot(self.t, self.amplitude * np.exp(-self.damp * self.t) *
                          self.func_list[1]((self.t - 0.05 * animate_time) + self.phase))
            self.ax2.plot(self.t, self.amplitude * np.exp(-self.damp * self.t) *
                          self.func_list[2]((self.t - 0.05 * animate_time) + self.phase))
            self.ax.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
            self.ax1.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
            self.ax2.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        return self.ax, self.ax1, self.ax2,

    def animateEnergy(self, animate_time):
        if self.pause != True:
            self.ClearAxesEnergy()
            self.ax3.plot(
                self.t, (self.KE - 0.5 * np.cos(animate_time)**2), '--', label="Kinetic Energy")
            self.ax3.plot(self.t, (self.PE - 0.5 * np.sin(animate_time)
                                   ** 2), '-.', label="Potential Energy")
            self.ax3.plot(self.t, 0.5 * np.ones_like(self.t),
                          label="Total Energy")
            self.ax3.set_xlim(0.125, 0.375)
        return self.ax3,

    """Activating the different plots (for later use with tkinter)"""

    def clickCallbackMotion(self, event):
        anim = animation.FuncAnimation(self.fig, self.animateMotion, init_func=self.initMotion,
                                       frames=100, interval=5, blit=True)
        self.fig.canvas.draw_idle()

    def clickCallbackEnergy(self, event):
        anim = animation.FuncAnimation(self.fig1, self.animateEnergy, init_func=self.initEnergy,
                                       frames=100, interval=5, blit=True)

        self.fig1.canvas.draw_idle()

    """ Resetting the time Dependence (animation) of the plots"""

    def resetMotion(self, event):
        self.ClearAxesMotion()
        self.sliderHandlephase.reset()
        self.sliderHandleDamp.reset()
        self.sliderHandlefreq.reset()
        self.sliderHandleAmplitude.reset()
        self.pause ^= True
        self.PlotAxesMotion()

    def resetEnergy(self, event):
        self.ClearAxesEnergy()
        self.pause ^= True
        self.PlotAxesEnergy()

    """ Slider Callback values for the Motion plot characteristics """

    def SliderCallbackfreq(self, val):
        self.frequency = self.sliderHandlefreq.val
        self.ClearAxesMotion()
        self.PlotAxesMotion()
        self.fig.canvas.draw_idle()

    def SliderCallbackphase(self, val):
        self.phase = self.sliderHandlephase.val
        self.ClearAxesMotion()
        self.PlotAxesMotion()
        self.fig.canvas.draw_idle()

    def SliderCallbackAmplitude(self, val):
        self.amplitude = self.sliderHandleAmplitude.val
        self.ClearAxesMotion()
        self.PlotAxesMotion()
        self.fig.canvas.draw_idle()

    def SliderCallbackDamp(self, val):
        self.damp = self.sliderHandleDamp.val
        self.ClearAxesMotion()
        self.PlotAxesMotion()
        self.fig.canvas.draw_idle()

    """ Activating the Oscillator for Motion"""

    def activateOscillatorMotion(self):

        self.fig = plt.figure('Simple Harmonic Oscilator')
        self.ax = self.fig.add_subplot(311)
        self.ax1 = self.fig.add_subplot(312)
        self.ax2 = self.fig.add_subplot(313)

        self.PlotAxesMotion()
        self.fig.subplots_adjust(left=0.25, bottom=0.4, hspace=0.2)

        Signalax = self.fig.add_axes([0.05, 0.005, 0.20, 0.07])
        self.buttonHandle = widgets.Button(Signalax, 'Time Dependence')
        self.buttonHandle.on_clicked(self.clickCallbackMotion)

        resetax = self.fig.add_axes([0.8, 0.025, 0.1, 0.04])
        self.button = widgets.Button(resetax, 'Reset')
        self.button.on_clicked(self.resetMotion)

        Freqax = self.fig.add_axes([0.25, 0.25, 0.65, 0.03])
        self.sliderHandlefreq = widgets.Slider(
            Freqax, 'Freq', 1, 15, valinit=self.initfrequency)
        self.sliderHandlefreq.on_changed(self.SliderCallbackfreq)

        Phaseax = self.fig.add_axes([0.25, 0.1, 0.65, 0.03])
        self.sliderHandlephase = widgets.Slider(
            Phaseax, 'Phase', 1, 15, valinit=self.initphase)
        self.sliderHandlephase.on_changed(self.SliderCallbackphase)

        Dampax = self.fig.add_axes([0.25, 0.15, 0.65, 0.03])
        self.sliderHandleDamp = widgets.Slider(
            Dampax, 'Damping', 0, 2, valinit=self.damp)
        self.sliderHandleDamp.on_changed(self.SliderCallbackDamp)

        Amplitudeax = self.fig.add_axes([0.25, 0.2, 0.65, 0.03])
        self.sliderHandleAmplitude = widgets.Slider(
            Amplitudeax, 'Amplitude', 1, 5, valinit=self.amplitude)
        self.sliderHandleAmplitude.on_changed(self.SliderCallbackAmplitude)
        self.ax.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax1.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        self.ax2.set_ylim(-1.5*self.amplitude, 1.5*self.amplitude)
        # self.fig.tight_layout()
        self.fig.show()
        plt.show()

    """ Activating the Oscillator for Energy"""

    def activateOscillatorEnergy(self):
        self.fig1 = plt.figure('Energy')
        self.ax3 = self.fig1.add_subplot()

        self.PlotAxesEnergy()

        Signalax1 = self.fig1.add_axes([0.05, 0.005, 0.20, 0.07])
        self.buttonHandle = widgets.Button(Signalax1, 'Time Dependence')
        self.buttonHandle.on_clicked(self.clickCallbackEnergy)

        resetax1 = self.fig1.add_axes([0.8, 0.025, 0.1, 0.04])
        self.button = widgets.Button(resetax1, 'Reset')
        self.button.on_clicked(self.resetEnergy)

        # self.fig1.tight_layout()
        self.fig1.show()
        plt.show()


On = Oscillator()

""" Differnt fonts for the tkinter widget-labels/buttons."""
Font = ("Verdana", 16)
Font2 = ("Verdana", 12)

""" Tk Widget was inspired by: https://pythonprogramming.net/tkinter-depth-tutorial-making-actual-program/"""


class OscillatorApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Figures in (HomePage, Page2):

            frame = Figures(container, self)

            self.frames[Figures] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Oscillator Widget",
                         font=Font).pack(pady=10, padx=10)

        self.image = Image.open("shm.ico")
        self.logo = ImageTk.PhotoImage(self.image)

        self.School_Logo_Label = tk.Label(
            self, image=self.logo).pack(side="top")
        self.School_Logo_Label_position = tk.Label(self,
                                                   justify=tk.LEFT,
                                                   padx=10,
                                                   text='').pack(side="top")
        button1 = tk.Button(self, text="Initiate Widget",
                            command=lambda: controller.show_frame(Page2)).pack()


class Page2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Oscillator Plots",
                         font=Font).pack(pady=10, padx=10)
        label1 = tk.Label(self, text="Position, Velocity, Acceleration",
                          font=Font2).pack(pady=10, padx=10)
        button2 = tk.Button(self, text="SHM characteristics",
                            command=lambda: On.activateOscillatorMotion()).pack()
        label2 = tk.Label(self, text="Energy of Simple Harmonic Oscillator",
                          font=Font2).pack(pady=10, padx=10)
        button3 = tk.Button(self, text="Energy characteristics",
                            command=lambda: On.activateOscillatorEnergy()).pack()
        button4 = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(HomePage)).pack(side='bottom')


app = OscillatorApp()
app.mainloop()
