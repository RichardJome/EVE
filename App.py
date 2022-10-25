from tkinter import *
import Brain
from Ears import take_user_input
from EVE import get_response
from tkinter import messagebox
import time
from PIL import Image, ImageTk

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        photo = PhotoImage(file="icon.png")
        self.window.iconphoto(False, photo)

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("EVE")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        setting_image = Image.open("question.png")
        setting_image_ph = ImageTk.PhotoImage(setting_image)

        setting_button = Button(head_label, text="Settings", font="FONT_BOLD", width="10", bg=BG_GRAY,
                                command=lambda: self.on_settings_pressed(None)
                                , image=setting_image_ph)
        setting_button.image = setting_image_ph
        setting_button.place(relx=0.025, rely=0.1, relheight=0.7, relwidth=0.060)

        vision_image = Image.open("eye.png")
        vision_image_ph = ImageTk.PhotoImage(vision_image)

        vision_button = Button(head_label, font="FONT_BOLD", width="10", bg=BG_GRAY, command=lambda: self._on_vision_pressed(None),
                                image=vision_image_ph)
        vision_button.image = vision_image_ph
        vision_button.place(relx=0.125, rely=0.1, relheight=0.7, relwidth=0.060)

        record_image = Image.open("red_circle.png")
        record_image_ph = ImageTk.PhotoImage(record_image)

        record_button = Button(head_label, text="Settings", font="FONT_BOLD", width="10", bg=BG_GRAY,
                               command=lambda: self.on_rec_pressed(None)
                               , image=record_image_ph)
        record_button.image = record_image_ph
        record_button.place(relx=0.925, rely=0.1, relheight=0.8, relwidth=0.070)

        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview())

        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        button_image = Image.open("robot.png")
        button_image_ph = ImageTk.PhotoImage(button_image)

        send_button = Button(bottom_label, text="Send", font="FONT_BOLD", width="20", bg=BG_GRAY,
                             command=lambda: self._on_enter_pressed(None), image=button_image_ph)
        send_button.image = button_image_ph
        send_button.place(relx=0.77, rely=0.008, relheight=0.05, relwidth=0.21)

    def on_settings_pressed(self, event):
        messagebox.showinfo("showinfo", "Created by Richard at age of 18 for science!")

    def _on_vision_pressed(self, event):
        from PIL import Image, ImageTk
        import tkinter as tk
        import argparse
        import datetime
        import cv2
        import os
        import mediapipe as mp

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mpFaceMesh = mp.solutions.face_mesh
        faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
        # mpPose = mp.solutions.pose
        # Pose = mpPose.Pose()
        mpDraw = mp.solutions.drawing_utils
        drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=5, color=(127, 255, 0))


        class Application:
            def __init__(self, output_path="./"):
                """ Initialize application which uses OpenCV + Tkinter. It displays
                    a video stream in a Tkinter window and stores current snapshot on disk """
                self.vs = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # capture video frames, 0 is your default video camera
                self.output_path = output_path  # store output path
                self.current_image = None  # current image from the camera

                self.root = tk.Tk()  # initialize root window
                self.root.title("My Vision")  # set window title
                # self.destructor function gets fired when the window is closed
                photo = tk.PhotoImage(file="icon.png")
                self.root.iconphoto(False, photo)

                self.panel = tk.Label(self.root)  # initialize image panel
                self.panel.pack(padx=10, pady=10)

                # create a button, that when pressed, will take the current frame and save it to file
                btn = tk.Button(self.root, text="Snapshot!", command=self.take_snapshot)
                btn.pack(fill="both", expand=True, padx=10, pady=10)

                # start a self.video_loop that constantly pools the video sensor
                # for the most recently read frame
                self.video_loop()

            def video_loop(self):
                """ Get frame from the video stream and show it in Tkinter """
                ok, frame = self.vs.read()  # read frame from video stream
                if ok:  # frame captured without any errors
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert colors from BGR to RGBA

                    results = hands.process(cv2image)
                    if results.multi_hand_landmarks:
                        for handLms in results.multi_hand_landmarks:
                            mpDraw.draw_landmarks(cv2image, handLms, mp_hands.HAND_CONNECTIONS, drawSpec, drawSpec)

                    results = faceMesh.process(cv2image)
                    if results.multi_face_landmarks:
                        for faceLms in results.multi_face_landmarks:
                            mpDraw.draw_landmarks(cv2image, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec,
                                                  drawSpec)

                    # results = Pose.process(cv2image)
                    # if results.pose_landmarks:
                    # mpDraw.draw_landmarks(cv2image, results.pose_landmarks, mpPose.POSE_CONNECTIONS, drawSpec, drawSpec)

                    self.current_image = Image.fromarray(cv2image)  # convert image for PIL
                    imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
                    self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
                    self.panel.config(image=imgtk)  # show the image
                # construct the argument parse and parse the arguments

                self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds

            def take_snapshot(self):
                """ Take snapshot and save it to the file """
                ts = datetime.datetime.now()  # grab the current timestamp
                filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))  # construct filename
                p = os.path.join(self.output_path, filename)  # construct output path
                self.current_image.save(p, "JPEG")  # save image as jpeg file

            def destructor(self):
                """ Destroy the root object and release all resources """
                self.root.destroy()
                self.vs.release()  # release web camera
                # it is not mandatory in this application

        ap = argparse.ArgumentParser()
        ap.add_argument("-o", "--output", default="./",
                        help="path to output directory to store snapshots (default: current folder")
        args = vars(ap.parse_args())
        self.window.destroy()
        pba = Application(args["output"])
        pba.root.mainloop()

    def on_rec_pressed(self, event):
        msg = take_user_input()
        self._insert_message(msg, "YOU")

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "YOU")

    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"EVE: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)


def login_screen():
    w = Tk()
    photo = PhotoImage(file="icon.png")
    w.iconphoto(False, photo)
    w.geometry('350x500')
    w.title(' L O G I N ')
    w.resizable(0, 0)

    # Making gradient frame
    j = 0
    r = 10
    for i in range(100):
        c = str(222222 + r)
        Frame(w, width=10, height=500, bg="#" + c).place(x=j, y=0)
        j = j + 10
        r = r + 1

    Frame(w, width=250, height=400, bg='white').place(x=50, y=50)

    l1 = Label(w, text='Username', bg='white')
    l = ('Consolas', 13)
    l1.config(font=l)
    l1.place(x=80, y=200)

    # e1 entry for username entry
    e1 = Entry(w, width=20, border=0)
    l = ('Consolas', 13)
    e1.config(font=l)
    e1.place(x=80, y=230)

    # e2 entry for password entry
    e2 = Entry(w, width=20, border=0, show='*')
    e2.config(font=l)
    e2.place(x=80, y=310)

    l2 = Label(w, text='Password', bg='white')
    l = ('Consolas', 13)
    l2.config(font=l)
    l2.place(x=80, y=280)

    ###lineframe on entry

    Frame(w, width=180, height=2, bg='#141414').place(x=80, y=332)
    Frame(w, width=180, height=2, bg='#141414').place(x=80, y=252)

    from PIL import ImageTk, Image

    imagea = Image.open("log.png")
    imageb = ImageTk.PhotoImage(imagea)

    label1 = Label(image=imageb,
                   border=0,

                   justify=CENTER)

    label1.place(x=115, y=50)

    # Command
    def cmd():
        if e1.get() == 'Richard' and e2.get() == 'EVE':
            messagebox.showinfo("LOGIN SUCCESSFULLY", "         W E L C O M E        ")
            w.destroy()
            loadingscreen()

        else:
            messagebox.showwarning("LOGIN FAILED", "        PLEASE TRY AGAIN        ")


    # Button_with hover effect
    def bttn(x, y, text, ecolor, lcolor):
        def on_entera(e):
            myButton1['background'] = ecolor  # ffcc66
            myButton1['foreground'] = lcolor  # 000d33

        def on_leavea(e):
            myButton1['background'] = lcolor
            myButton1['foreground'] = ecolor

        myButton1 = Button(w, text=text,
                           width=20,
                           height=2,
                           fg=ecolor,
                           border=0,
                           bg=lcolor,
                           activeforeground=lcolor,
                           activebackground=ecolor,
                           command=cmd)

        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x, y=y)

    bttn(100, 375, 'L O G I N', 'white', '#994422')

    w.mainloop()


def loadingscreen():
    w = Tk()

    # Using piece of code from old splash screen
    width_of_window = 427
    height_of_window = 250
    screen_width = w.winfo_screenwidth()
    screen_height = w.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width_of_window / 2)
    y_coordinate = (screen_height / 2) - (height_of_window / 2)
    w.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
    # w.configure(bg='#ED1B76')
    w.overrideredirect(1)  # for hiding titlebar

    # new window to open
    def new_win():
        q = Tk()
        q.title('main window')
        q.mainloop()

    Frame(w, width=427, height=250, bg='#272727').place(x=0, y=0)
    label1 = Label(w, text='EVE', fg='white', bg='#272727')  # decorate it
    label1.configure(font=("Game Of Squids", 24, "bold"))  # You need to install this font in your PC or try another one
    label1.place(x=180, y=90)

    label2 = Label(w, text='Loading...', fg='white', bg='#272727')  # decorate it
    label2.configure(font=("Calibri", 11))
    label2.place(x=350, y=215)

    # making animation

    image_a = ImageTk.PhotoImage(Image.open('c2.png'))
    image_b = ImageTk.PhotoImage(Image.open('c1.png'))

    for i in range(5):  # 5loops
        l1 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
        l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
        l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
        l4 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.5)

        l1 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
        l2 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
        l3 = Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
        l4 = Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
        w.update_idletasks()
        time.sleep(0.5)

    w.destroy()
    w.mainloop()
    Brain.greet_user()
    app = ChatApplication()
    app.run()


if __name__ == '__main__':
    login_screen()