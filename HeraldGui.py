from Tkinter import *
from PIL import ImageTk, Image
import GCODEcreator2
import matplotlib, sys
matplotlib.use('TkAgg') 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from stream import stream 


# Our Main Gui page. 
class MainPage():
    def __init__ (self, myparent):
        self.myParent = myparent
        self.myParent.wm_title("Herald Caligraphy")
        self.myContainer1 = Frame(self.myParent, bg = "white")
        self.myContainer1.pack()
        
        # All of our constants that we use throughout the frames

        self.main_font = ('Helvetica', 16, 'normal')
        self.button_font = ('Helvetica', 14, 'normal')
        self.descrip_font = ('Helvetica', 14, 'normal')
        self.options_font = ('Helvetica', 14, 'normal')

        button_width = 10
        button_height = 3

        button_padx="2m"
        button_pady = "1m"

        title_frame_padx =  "10m"   
        title_frame_pady =  "10m"   
        title_frame_ipadx = "10m"   
        title_frame_ipady = "10m"

        num_options_pady = ".5m"

        frame_padx = "3m"
        frame_pady = "3m"
        frame_ipadx = "3m"
        frame_ipady = "3m" 

        self.page_size_choice = StringVar()
        self.page_size_choice.set("8.5in X 11in")

        self.font_choice = StringVar()
        self.font_choice.set("Edwardian.txt")     
        Fonts = ['Font1', 'Font2', 'Font3']
        
        self.title_size_choice = IntVar()
        self.title_size_choice.set(24)
        
        self.body_size_choice = IntVar()
        self.body_size_choice.set(16)


        Size_Choices = [16, 20, 24]

        self.title_alignment_choice = IntVar()
        self.title_alignment_choice.set(1)

        self.alignment_choice = IntVar()
        self.alignment_choice.set(0)

        self.vert_alignment_choice = IntVar()
        self.vert_alignment_choice.set(0)


        self.left_margin_choice = DoubleVar()
        self.top_margin_choice = DoubleVar()

        self.left_margin_choice.set(2.5)
        self.top_margin_choice.set(2.0)
        # Main Frames
        

        ###############
        # Title Frame #
        ###############
        
        self.title_frame = Frame(self.myContainer1, bg = "white")

        self.title_frame.pack(side = TOP) 

        im = Image.open('Herald.png')
        self.tkimage = ImageTk.PhotoImage(im)

        self.TitlePicture = Label(self.title_frame, image=self.tkimage, bg = "white")

        self.TitlePicture.pack()



        ###############
        # Action Frame #
        ###############

        self.action_frame = Frame(self.myContainer1, bg = "white")
        self.action_frame.pack(side = TOP)

        ###############
        # Closure Frame #
        ###############

        self.closure_frame = Frame(self.myContainer1, bg = "white")
        self.closure_frame.pack(side = TOP)


        ###############
        # Options Frame in Action Frame #
        ###############
        self.options_frame = Frame(self.action_frame, bg = "white")
        self.options_frame.pack(side = LEFT, fill = BOTH, ipadx = title_frame_ipadx,
               padx = title_frame_padx,
                pady = "8m")

        ###
        #Font Options
        ###

        self.font_options_frame = Frame(self.options_frame, bg = "white")
        self.font_options_frame.pack(side = TOP)

        #Font Frame
        
        self.font_frame = Frame(self.font_options_frame, bg = "white")
        self.font_frame.pack(side = LEFT)
        

        self.font_label = Label(self.font_frame, text = "Select a Font", font = self.main_font, bg = "white")
        self.font_label.pack(side= TOP)


        font_preview1 =  Image.open('Font1.png')
        self.fontimage1 = ImageTk.PhotoImage(font_preview1)
        self.preview_label1 = Radiobutton(self.font_frame, image=self.fontimage1, value= "Edwardian.txt", variable=self.font_choice, bg = "white" ) 
        self.preview_label1.pack()

        font_preview2 =  Image.open('Font2.png')
        self.fontimage2 = ImageTk.PhotoImage(font_preview2)
        self.preview_label2 = Radiobutton(self.font_frame, image=self.fontimage2, value="CamBam5.txt", variable=self.font_choice , bg = "white")# indicatoron=False) 
        self.preview_label2.pack()

        font_preview3 =  Image.open('Font3.png')
        self.fontimage3 = ImageTk.PhotoImage(font_preview3)
        self.preview_label3 = Radiobutton(self.font_frame, image=self.fontimage3, value="Font3.txt", variable=self.font_choice, bg = "white")# indicatoron=False) 
        self.preview_label3.pack()


        #Size Frame
        
        self.size_frame = Frame(self.font_options_frame, bg = "white")
        self.size_frame.pack(side = TOP, padx = title_frame_padx)
        

        #Page Size Choice
        self.page_size_frame = Frame(self.size_frame, bg = "white")
        self.page_size_frame.pack(side = TOP) 

        self.page_size_box = Spinbox(self.size_frame, values =["8.5in X 11in", "3in X 4in", "4.25in X 5.5in", "8.5in X 5.5in"]  , textvariable=self.page_size_choice, wrap = True, font = self.descrip_font)
        self.page_size_box["width"] = button_width*3/2
        self.page_size_box.pack(side=TOP, pady = num_options_pady)


        self.page_size_label = Label(self.page_size_frame, text = "Select a Page Size", font = self.main_font, bg = "white")
        self.page_size_label.pack(side= TOP, pady = num_options_pady)


        # Title font size choice
        self.title_size_label = Label(self.size_frame, text = "Select a Title Font Size", font = self.main_font, bg = "white")
        self.title_size_label.pack(side= TOP, pady = num_options_pady)
        #Font Buttons
 

        self.title_size_box = Spinbox(self.size_frame, from_ = 12, to = 70, increment = 2, textvariable=self.title_size_choice, wrap = True, font = self.descrip_font)
        self.title_size_box["width"] = button_width/2
        self.title_size_box.pack(side=TOP, pady = num_options_pady)


        # Body font size choice
        self.size_label = Label(self.size_frame, text = "Select a Body Font Size", font = self.main_font, bg = "white")
        self.size_label.pack(side= TOP, pady = num_options_pady)
        
        self.body_size_box = Spinbox(self.size_frame, from_ = 12, to = 70, increment = 2, textvariable=self.body_size_choice, wrap = True, font = self.descrip_font)
        self.body_size_box["width"] = button_width/2
        self.body_size_box.pack(side=TOP, pady = num_options_pady)


        # Margins Choice

        self.margins_options_frame = Frame (self.size_frame, bg = "white") 
        self.margins_options_frame.pack(side = TOP, pady = num_options_pady)

        self.margins_label = Label(self.margins_options_frame, text = "Select the Margins", font = self.main_font,   bg = "white")
        self.margins_label.pack(side = TOP, pady = num_options_pady)

        self.left_margin_frame = Frame(self.size_frame, bg= "white")
        self.left_margin_frame.pack(side = TOP)

        self.left_margin_label = Label(self.left_margin_frame, text = "Horizontal", font = self.descrip_font, width = button_width, bg = "white")
        self.left_margin_label.pack(side = LEFT, pady = num_options_pady)
        self.left_margin_entry = Spinbox(self.left_margin_frame, values = (1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, .25, .5, .75, 1.0, 1.25), textvariable=self.left_margin_choice, wrap = True, font = self.descrip_font)
        self.left_margin_entry["width"] = button_width/2
        self.left_margin_entry.pack(side=LEFT, pady = num_options_pady)

        self.right_margin_frame = Frame(self.size_frame, bg= "white")
        self.right_margin_frame.pack(side = TOP)

        self.top_margin_label = Label(self.right_margin_frame, text = "Vertical", font = self.descrip_font, width = button_width, bg = "white")
        self.top_margin_label.pack(side = LEFT, pady = num_options_pady)
        self.top_margin_entry = Spinbox(self.right_margin_frame, values = (1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, .25, .5, .75, 1.0, 1.25), textvariable=self.top_margin_choice, wrap = True, font = self.descrip_font)
        self.top_margin_entry["width"] = button_width/2
        self.top_margin_entry.pack(side=LEFT, pady = num_options_pady)



        # Frame for all the alignments. 
        self.spacing_options_frame = Frame(self.options_frame, bg = "white")
        self.spacing_options_frame.pack(side = TOP, padx = frame_ipadx,
                pady = frame_ipady)


        self.title_justify_frame = Frame(self.spacing_options_frame, bg = "white")
        self.title_justify_frame.pack(side = TOP,     pady = frame_ipady)

        self.title_justify_label = Label(self.title_justify_frame, text = "Select the Title Alignment", font = self.main_font, bg = "white")
        self.title_justify_label.pack(side = TOP)

        #Title
        self.title_justify_left_button = Radiobutton(self.title_justify_frame, text = "Left Aligned", font = self.button_font, 
            indicatoron = False, value = 0, variable = self.title_alignment_choice, width = (3*button_width)/2)
        self.title_justify_left_button.pack (side = LEFT)

        self.title_justify_center_button = Radiobutton(self.title_justify_frame, text = "Center Aligned", font = self.button_font, 
            indicatoron = False, value = 1, width = (3*button_width)/2,  variable = self.title_alignment_choice)
        self.title_justify_center_button.pack (side = LEFT)

        self.justify_frame = Frame(self.spacing_options_frame, bg = "white")
        self.justify_frame.pack(side = TOP,     pady = frame_ipady)

        #Body Horizontal

        self.justify_label = Label(self.justify_frame, text = "Select the Body Alignment", bg = "white", font = self.main_font)
        self.justify_label.pack(side = TOP)

        self.justify_left_button = Radiobutton(self.justify_frame, text = "Left Aligned", font = self.button_font, 
            indicatoron = False, value = 0, variable = self.alignment_choice, width = (3*button_width)/2)
        self.justify_left_button.pack (side = LEFT)

        self.justify_center_button = Radiobutton(self.justify_frame, text = "Center Aligned", font = self.button_font, 
            indicatoron = False, value = 1, width = (3*button_width)/2,  variable = self.alignment_choice)
        self.justify_center_button.pack (side = LEFT)

        self.vert_justify_frame = Frame(self.spacing_options_frame, bg = "white")
        self.vert_justify_frame.pack(side = TOP,     pady = frame_ipady)

        self.vert_justify_label = Label(self.vert_justify_frame, text = "Select the Vertical Alignment", bg = "white", font = self.main_font)
        self.vert_justify_label.pack(side = TOP)

        #Body Vertical
        self.vert_justify_left_button = Radiobutton(self.vert_justify_frame, text = "Top Aligned", font = self.button_font, 
            indicatoron = False, value = 0, variable = self.vert_alignment_choice, width = (3*button_width)/2, command = self.Vert_Align)
        self.vert_justify_left_button.pack (side = LEFT)

        self.vert_justify_center_button = Radiobutton(self.vert_justify_frame, text = "Middle Aligned", font = self.button_font, 
            indicatoron = False, value = 1, width = (3*button_width)/2,  variable = self.vert_alignment_choice, command = self.Middle_Align)
        self.vert_justify_center_button.pack (side = LEFT)

 
        
        ###############
        # Text Frame in Action Frame #
        ###############



        self.text_frame = Frame(self.action_frame, bg = "white")
        self.text_frame.pack( fill = BOTH, side = LEFT, ipadx = title_frame_ipadx,
                padx = title_frame_ipadx)

        #Where user enters title

        self.title_frame= Frame(self.text_frame, bg = "white")
        self.title_frame.pack(side=TOP,  ipady = title_frame_ipady)


        self.title_text_label = Label(self.title_frame, text = "Insert Title Text Here: ", font = self.main_font, bg = "white")
        self.title_text_label.pack( side= LEFT)

        self.title_text_input = Entry(self.title_frame, font = self.descrip_font)
        self.title_text_input.pack( side = LEFT) 

        #Where user enters body text

        self.text_label = Label(self.text_frame, text = "Insert Body Text Here:", font = self.main_font, bg = "white")
        self.text_label.pack( side= TOP)

        self.text_input = Text(self.text_frame, cursor = "pirate" , yscrollcommand = ".set",  height = "17", wrap = "word", font = self.descrip_font)
        self.text_input.pack( side = TOP, fill = X) 
        self.text_input.tag_add("all", 0.0, 100.0)
        self.text_input.tag_config("all",justify = CENTER)

        #User submitted gcode section
        #here is where the user can input a name and submit their own Gcode for Herald to run.

        self.user_gcode_frame = Frame(self.text_frame, bg = "white")
        self.user_gcode_frame.pack()

        self.user_gcode_label = Label( self.user_gcode_frame, bg = "white", font = self.descrip_font, text = "If you'd like to upload your own Gcode, put it in this GUI's folder and \n enter the filename below. Please ensure the file fits Herald's Gcode specifcations")
        self.user_gcode_label.pack(side = TOP)

        self.file_input_frame = Frame (self.user_gcode_frame, bg = "white")
        self.file_input_frame.pack()

        self.file_input_label = Label(self.file_input_frame, font = self.descrip_font, text = "Filename:", bg = "white" )
        self.file_input_label.pack( side = LEFT)

        self.file_input = Entry(self.file_input_frame, font = self.descrip_font)
        self.file_input.pack(side = LEFT)

        self.file_input_button = Button(self.file_input_frame, text = "Submit my own file", width = button_width*3/2, font = self.button_font, bg = "tan")
        self.file_input_button.pack(side = LEFT)
        
        self.file_input_button.bind("<Return>", self.Event_File_Preview)
        self.file_input_button.bind("<Button-1>", self.Event_File_Preview)
 


        ###############1
        # Closure Buttons in Closure Frame #
        ###############
        
        self.Cancel_button = Button(self.closure_frame, bg = "tan")
        self.Cancel_button.configure(
            text = "Cancel",
            width=button_width,  
            padx=button_padx,    
            pady=button_pady,    
            font = self.button_font
            )


        self.Cancel_button.pack(side=RIGHT)
        self.Cancel_button.bind("<Return>", self.Event_Cancel)
        self.Cancel_button.bind("<Button-1>", self.Event_Cancel)
 
       
        self.Preview_button = Button(self.closure_frame, bg = "tan") 
        self.Preview_button.configure(
            text = "Continue",
            width=button_width,  
            padx=button_padx,    
            pady=button_pady,    
            font = self.button_font
            )

        self.Preview_button.pack(side=RIGHT)
        self.Preview_button.focus_force()
        self.Preview_button.bind("<Return>", self.Event_Preview)
        self.Preview_button.bind("<Button-1>", self.Event_Preview)

    
    #If the user chooses to middle align, we no longer support titles. We lock the title entry box.
    #If there is someting in the title box, we warn the user with a popup that their text won't be displayed 
    
    def Middle_Align (self, event = None):
        self.title_text_input["state"] = "readonly" 

        if len(self.title_text_input.get()) > 0:
            w = warning("If the text is middle aligned, \nthere can't be seperate title text.", self.main_font)
      
    # If the user is going back to top aligned, we unlock the title entry box so the user can enter titles 
    def Vert_Align (self, event = None):
        self.title_text_input["state"] = NORMAL

    #Kills the GUI 
    def Event_Cancel (self, event = None):
        self.myParent.destroy()

    # Grabs all the relevent information calls GCODECreator and then opens the preview GUI
    def Event_Preview (self, event = None):
        #Grab all the info
        font = self.font_choice.get() 
        font_size = self.body_size_choice.get()
        hMarg = 25.4*self.top_margin_choice.get()
        vMarg = 25.4*self.left_margin_choice.get()
        Hcentered = self.alignment_choice.get()  
        Vcentered = self.vert_alignment_choice.get()
        pageW = 25.4*float(self.page_size_choice.get().split()[0][:-2])
        pageH = 25.4*float(self.page_size_choice.get().split()[2][:-2])
        raw_text = self.text_input.get(0.0, END)
        text = ""

        #Easter egg. If the user chooses our third font, we send them a funny message
        if font == "Font3.txt":
            w = warning("Go home Herald! You're Drunk!", self.main_font)
            conflict = True        
        for line in raw_text.split("\n"):
            text += line+"*"
        debug(font_size, text, hMarg, vMarg, Hcentered, Vcentered, False, pageW, pageH   )
            
        # Check if there is a title and is we're top aligned. If both are true, we grab the title information and create a title then create the body
        # If either or both is/are false, just write out the body text.     
        conflict = False 
        if len(self.title_text_input.get()) > 0 and Vcentered == 0:
            #Grab title info info
            title = self.title_text_input.get()
            title_size = self.title_size_choice.get()
            title_Hcentered = self.title_alignment_choice.get()
            #Write out the text, get back either the vertical space the title took up or the error the text caused  
            headerpace = GCODEcreator2.writer(font, title_size, title, hMarg, vMarg, title_Hcentered, Vcentered, True, pageW, pageH, "pen",0 , 0)
            #If it returned a string, that means there was an error and we throw a pop up with the error and set conflict to true. 
            if isinstance(headerpace, str):
                w = warning(headerpace, self.main_font)
                conflict = True
            #Else we're good to go
            else:
                #pass the Gcode creator the headerspace so the text is not written over old text.
                message = GCODEcreator2.writer(font, font_size, text, hMarg, vMarg, Hcentered, Vcentered, False, pageW, pageH,"pen",  headerpace[0] + font_size, headerpace[1]   )
                #Check for error messages again. Throw pop up if we get them.
                if isinstance(message, str):
                    w = warning(message, self.main_font)
                    conflict = True
        else:
            #If there is no title, simply send the text and check for an error. 
            message = GCODEcreator2.writer(font, font_size, text, hMarg, vMarg, Hcentered, Vcentered, True, pageW, pageH, "pen")
            if isinstance(message, str):
                w = warning(message, self.main_font)
                conflict = True
        #If we have not hit a conflict go to the Preview GUI
        if not conflict:     
            p = Preview_Gui( "grbl.gcode", self, pageW, pageH, hMarg, vMarg)
            self.myParent.destroy()
            
    #If the user wants to submit their own file, this function takes the filename input and passes it to the preview. 
    #The preview opens the user's document instead of the default document. 
    def Event_File_Preview (self, event = None):    
        user_file = self.file_input.get()

        Preview_Gui(user_file, self)
        self.myParent.destroy()             



#This is the Preview GUI. It is called from the Main GUI and plots the Gcode in the way the machine would write it. 

class Preview_Gui():
    def __init__(self, file_name, owner, page_width =  215.9 , page_height = 279.4, h_margin = 0, v_margin = 0):
        #Create the GUI        
        self.main = owner
        self.master = Toplevel()
        self.master.title("Herald Preview")
        self.file_name = file_name        
        #Make the Gui a size that matches the size of the paper
        #defaults to 8.5 by 11 with user inputted files.
        w = int(round(page_width/25.4)*100)
        h = int(round(page_height/25.4)*100 + 50)
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        horzpos = (ws/2) - (w/2)
        vertpos = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, horzpos, vertpos))
    
        #each x and y is one time putting the pen down
        #Xs and Ys store all these times the pen go down so they can plot them. Z is simply the last height of the pen.     
        # Start the variable that is going to be graphed by writing in the lines of the page border and margins so the user has an idea of how much space they have.

        x=[]
        y=[]
        Xs = [[0, 0, page_width, page_width, 0], [h_margin, h_margin, page_width - h_margin, page_width - h_margin, h_margin]]
        Ys = [[0, page_height, page_height, 0, 0], [v_margin, page_height - v_margin, page_height - v_margin, v_margin, v_margin]]
        Zs = [0,0]

        Z = 0.0
        lastx= []
        lasty = [] 
 
        #Gcode
        gcode = open(self.file_name, 'r')
        write = False
        #for each word in each line...
        for lin in gcode:
            words = lin.split()
            for word in words:
                #If the word starts with X/Y, it represents the next X/Y spot, save add it to the current X/Y and and save it as the last X/Y in case we pick up the pen will be used later. 
                if word[0] == "X":
                    x.append(float(word[1:]))
                
                if word[0] == "Y":
                    y.append(float(word[1:]))
                # If it is Z check what we're doing with the pen height wise
                if word[0] == "Z":
                    # If there happens to be a ), get rid of it
                    if word[-1] == ")":
                        word = word [0:len(word)-1]


                    #If the height is off the paper, save the last X, Y and Z for plotting and set x and y to empty lists. 
                    #We save Z but don't currently use it. If we decided we want to plot with variable line thickness, we would use the Z component to do that. 
                    if float(word[1:]) > 0.001:
                        write = False
                        
                        Xs.append( x)
                        Ys.append( y)

                        Zs.append(Z)           
                        x = []
                        y = []
                        Z = float(word[1:])
                    else: 
                        Z = float(word[1:])
                        write = True

        gcode.close()                   
  
        #Save the last moves if the pen was down when they were done.       
        if write == True:
            Xs.append(x)
            Ys.append(y)
            Zs.append(Z)

        #Create the figure
        f = plt.figure(figsize=(int(page_width/(25.4*1.4)), int(page_height/(25.4*1.4))), dpi=100, facecolor = "w")
        a = f.add_subplot(111)
        #Turn off the axis so it looks like a white square and not like a graph.
        a.set_axis_off()

        #Take each list of positions when the pen was put down and plot them. We don't want to plot every point, because then we would draw lines between letters
        for i in range(len(Xs)):
            a.plot(Xs[i],Ys[i], "k")


        plt.xlim(0, page_width)
        plt.ylim(0, page_height)

        #Pack the Figure
        self.dataPlot = FigureCanvasTkAgg(f, master=self.master)
        self.dataPlot.show()
        self.dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        #Set the Option buttons for the user.
        self.button_frame = Frame( master=self.master)
        self.button_frame.pack(side=TOP)

        self.return_button = Button(self.button_frame, text = "Return")
        self.return_button.pack(side=RIGHT)
        self.return_button.bind("<Return>", self.Event_Return)
        self.return_button.bind("<Button-1>", self.Event_Return)

        self.continue_button = Button(self.button_frame, text = "Continue")
        self.continue_button.pack(side=RIGHT)
        self.continue_button.bind("<Return>", self.Event_Continue)
        self.continue_button.bind("<Button-1>", self.Event_Continue)

        self.zero_button = Button(self.button_frame, text = "Zero")
        self.zero_button.pack(side=RIGHT)
        self.zero_button.bind("<Return>", self.Event_Zero)
        self.zero_button.bind("<Button-1>", self.Event_Zero)


        save_input = BooleanVar()
        save_input.set(False)

        self.save_button = Button(self.button_frame, text = "Save" ,  command = self.Event_Save )
        self.save_button.pack(side = RIGHT)

        toolbar = NavigationToolbar2TkAgg( self.dataPlot, self.button_frame )
        toolbar.pack(side=RIGHT, fill=BOTH, expand=1)
        toolbar.update()

        self.master.mainloop()


    def Event_Return( self, event = None):
        self.master.destroy()

        #If the user is happy, this will start the machine and run GRBL
    def Event_Continue( self, event = None):
        stream(self.file_name)
        self.main.myParent.destroy()
        self.master.destroy()

    # This zeroes the arduino
    def Event_Zero(self, event = None):
        stream("zero.gcode")

    #This opens a save GUI allowing the user to save this gcode under another filename. 
    def Event_Save(self, event = None):
        sv = Save()
    #This is our simple Popup GUI. Any Popup uses this and simply displays its given text and has an ok button
class warning():
    def __init__ (self, text, font):
        warning = Toplevel  ()
        self.parent = warning
        self.parent.wm_title("Herald Warning")

        w = 400
        h = 100
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.main_frame = Frame(self.parent, bg = "white")
        self.main_frame.pack(ipadx = "2m", ipady = "2m", fill = BOTH )
        
        #Displays the text
        self.message = Label(self.main_frame, bg = "white", font = font, text = text)
        self.message.pack(side = TOP,padx = "2m", pady = "1m")
        self.Cancel_button = Button(self.main_frame, bg = "tan")
        self.Cancel_button.configure(
            text = "Ok",
            width=10,  
            padx="2m",    
            pady="1m",    
            font = font
            )
        #Creates the one button.
        self.Cancel_button.pack(side=TOP)
        self.Cancel_button.bind("<Return>", self.quit)
        self.Cancel_button.bind("<Button-1>", self.quit)
     

        self.parent.mainloop()  

    def quit (self, event = None):
        self.main_frame.pack_forget()
        self.parent.destroy()


#This GUI for inputting a file name and saving your Gcode. 
class Save():
    def __init__ (self):
        Save_file = Toplevel  ()
        self.parent = Save_file
        self.parent.wm_title("Herald Save File")
        self.font = ('Helvetica', 16, 'normal')

        #Set the size
        w = 400
        h = 100
        ws = self.parent.winfo_screenwidth()
        hs = self.parent.winfo_screenheight()
        
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.main_frame = Frame(self.parent, bg = "white")
        self.main_frame.pack(ipadx = "2m", ipady = "2m", fill = BOTH )

        self.save_frame = Frame(self.main_frame, bg = "white")
        self.save_frame.pack(side = TOP)

        #User side of the GUI
        self.message = Label(self.save_frame, bg = "white", font = self.font, text = "Enter the File Name")
        self.message.pack(side = LEFT, padx = "2m", pady = "1m")

        self.save_entry = Entry(self.save_frame, bg = "white", font = self.font )
        self.save_entry.pack()

        self.save_text = Label(self.main_frame, bg = "white", font = self.font, text = "The file will be saved in this Gui's folder.")
        self.save_text.pack(side = TOP)

        self.button_frame = Frame(self.main_frame, bg = "white")
        self.button_frame.pack(side = TOP, padx = "3m")
        self.Save_button = Button(self.button_frame, bg = "tan")
        self.Save_button.configure(
            text = "Save",
            width=10,  
            padx="2m",    
            pady="1m",     
            font = self.font
            )

        self.Save_button.pack(side=LEFT)
        self.Save_button.bind("<Return>", self.save_file)
        self.Save_button.bind("<Button-1>", self.save_file)
     

        self.Cancel_button = Button(self.button_frame, bg = "tan")
        self.Cancel_button.configure(
            text = "Cancel",
            width=10,  
            padx="2m",   
            pady="1m",   
            font = self.font
            )

        self.Cancel_button.pack(side=LEFT)
        self.Cancel_button.bind("<Return>", self.quit)
        self.Cancel_button.bind("<Button-1>", self.quit)
     

        self.parent.mainloop()

    #If saving, the user calls this:  
    def save_file(self, event = None):
        # Grab what the user wants to call their saved file
        filename = self.save_entry.get()
        #Open the file being copied and the new file
        gcode = open('grbl.gcode', 'r')
        new_file = open(filename, 'w')
        #Write each line of the old code in the next code. 
        for lin in gcode:
            new_file.write(lin+"\n")
        gcode.close()
        new_file.close()
        self.quit()
        
    def quit (self, event = None):
        self.main_frame.pack_forget()
        self.parent.destroy()    


#This function was used when we wanted to make sure our input took the form we wanted. 
#It may not be called in the code, but we keep in case we introduce bugs.     
def debug (font_size, text, hMarg, vMarg, Hcentered, Vcentered, first, pageW, pageH, headerpace = 0 ):
    print "The text is: " + text
    print "The fontsize is: " + str(font_size)
    print "The Horizonatal and Vert Margins are:" + str(hMarg) + ", " + str(vMarg)
    if Hcentered == 1:
        print "It is horizontally centered:"
    else:
        print "It isn't horizontally centered" 
    if Vcentered == 1:
        print "It is Verticlaly Centered."
    else:
        print "it is not vertically centered"
    print "the page is " + str(pageW) + "mm by " + str(pageH) + "mm."


root = Tk()
openpage = MainPage(root)
root.mainloop()
    
