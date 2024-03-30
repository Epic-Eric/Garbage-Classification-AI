import tkinter
import cv2
import PIL.Image, PIL.ImageTk



class App:


    def __init__(self, window, video_source=1):
        self.window=window
        self.window.title=("Garbage Classification")
        self.video_source=video_source
        self.window.resizable(False, False)
        self.vid= MyVideoCapture(self.video_source)
        self.canvas=tkinter.Canvas(window, width=self.vid.width-15, height =  self.vid.height-15)
        self.canvas.pack()
        self.camera = 1


        self.switch_camera()


        btn_frame=tkinter.Frame(window, background=self.from_rgb((117, 123, 129)))
        btn_frame.place(x=0,y=0, anchor="nw", width=self.vid.width+4)


        self.btn_snapshot=tkinter.Button(btn_frame, text="Classify",width=20, command=self.snapshot, bg=self.from_rgb((52, 61, 70)), fg="white")
        self.btn_snapshot.pack(side="left", padx=10, pady=10)
	

        self.btn_proses=tkinter.Button(btn_frame, text="Change Camera", width=20, command=self.switch_camera, bg=self.from_rgb((52, 61, 70)), fg="white")
        self.btn_proses.pack(side="left", padx=10, pady=10)

        self.classifytext=tkinter.Label(btn_frame, text="The image resembles _______", width=100, bg=self.from_rgb((117, 123, 129)), fg="white")
        self.classifytext.pack(side="left", padx=10, pady=10)


        self.delay=15
        self.update()


        self.window.mainloop()

    def digit_flip(self):
        if self.video_source == 1:
            self.video_source = 0


        elif self.video_source == 0:
            self.video_source = 1
       
    def switch_camera(self):
        self.digit_flip()
        self.vid= MyVideoCapture(self.video_source)
        print(self.video_source)


    def snapshot(self):
        ret, frame=self.vid.get_frame()
        if ret:
            cv2.imwrite("image.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) )
            self.classifytext.config(text=predict_external_image('image.jpg'))

    def update(self):
        ret, frame=self.vid.get_frame()


        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image=self.photo, anchor=tkinter.NW)


            self.window.after(self.delay,self.update)
           


    def from_rgb(self,rgb):
        return "#%02x%02x%02x" % rgb




class  MyVideoCapture:
    """docstring for  MyVideoCapture"""
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("unable open video source", video_source)


        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret,None)      
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tkinter.Tk())