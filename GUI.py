from customtkinter import *
import os
from tkinter import filedialog,colorchooser,font
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import SEL_FIRST,SEL_LAST
from PIL import Image
import Reader
from CTkSpinbox import CTkSpinbox
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu


class App:
    
    def __init__(self):
        self.default_image_path = None
        self.htr = Reader.HTR(model_path='model')
        self.htr_page = Reader.HTR_page_reader()
        self.result_text_HTR_mltu = ''
        self.result_text_HTR_pipeline = ''

    def new_file(self):
        self.text_area.delete(1.0,END)
        self.handwritten_image_label.configure(image=self.no_image)

    def save_file(self,root):
        file = filedialog.asksaveasfilename(initialfile='untitled.txt',defaultextension='.txt',filetypes=[('All Files','*.*'),('Text files','*.txt')])
        if file is None:
            return
        else:
            try:
                root.title(os.path.basename(file))
                file = open(file,'w')
                file.write(self.text_area.get(1.0,END))

            except Exception:
                showerror('error','something went wrong')
            finally:
                file.close()

    def cut(self,root):
        self.copy(root)
        try: self.text_area.delete(SEL_FIRST, SEL_LAST)
        except: pass

    def copy(self,root):
        root.clipboard_clear()
        try: root.clipboard_append(self.text_area.get(SEL_FIRST, SEL_LAST))
        except: pass
        

    def paste(self,root):
        try: self.text_area.insert(self.text_area.index('insert'), root.clipboard_get())
        except: pass

    def about(self):
        showinfo('About this program','This program is written by Erfan Nateghi to convert handwritten images to text. Give your image to the program and click on the scan button and your text will be displayed')

    def quit(self,root):
        root.destroy()

    def change_color(self):
        color = colorchooser.askcolor(title = "pick a color")
        self.text_area.configure(text_color= color[1])
    
    def Change_font(self):
        self.text_area.configure(font=(self.font_name.get(),self.font_size.get()))
    
    def insert_image(self):
        
        try:
            temp = filedialog.askopenfilename(initialdir="/", title="Select an image",
                                            filetypes=( [("Image Files", "*.jpg; *.png")]))
            if temp != '':
                self.default_image_path = temp
                self.handwritten_image_label.configure(image=CTkImage(Image.open(self.default_image_path),size=(400,300)))
                self.image_path_label.configure(text=self.default_image_path)
        except Exception:
            print('error')

    def choose_AI(self):
        self.text_area.delete(1.0,END)
        if self.AI_choose.get() == 'HTR pipeline(page reader)':
            self.text_area.insert(1.0,self.result_text_HTR_pipeline)
        elif self.AI_choose.get() == 'HTR mltu(sentence reader)':
            self.text_area.insert(1.0,self.result_text_HTR_mltu)

    def scan(self):
        self.result_text_HTR_pipeline = self.htr_page.scan(self.default_image_path)
        self.result_text_HTR_mltu = self.htr.scan(self.default_image_path)

        if self.AI_choose.get() == 'HTR pipeline(page reader)':
            self.text_area.delete(1.0,END)
            self.text_area.insert(1.0,self.result_text_HTR_pipeline)
        elif self.AI_choose.get() == 'HTR mltu(sentence reader)':
            self.text_area.delete(1.0,END)
            self.text_area.insert(1.0,self.result_text_HTR_mltu)
        

    def center_window(self,root,window_width,window_height):
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    
    def main(self):
        root = CTk()
        window_width = 1200
        window_height = 600
        self.center_window(root,window_width,window_height)
        root.resizable(False,False)
        root.title("HTR")

        background_image = CTkImage(Image.open('background.jpg'),size=(1200,600))
        background_label = CTkLabel(root,image=background_image,text='')
        background_label.place(x=0,y=0)

        #split the window into two frame (one for image and other for text editor)
        main_frame = CTkFrame(root,corner_radius=50,background_corner_colors=("#2c3bdc","#2ac0cf","#2167da","#2c3bdc"))
        main_frame.pack(pady=20,padx=20,fill='both',expand=True)
        
        #image frame
        image_frame = CTkFrame(main_frame, width=500 ,height=600,fg_color='#1D1D1D')
        image_frame.pack( side='left',padx=50,pady=20,fill='both',expand=True)

        #text editor frame
        text_editor = CTkFrame(main_frame, width=500 ,height=500,fg_color='#1D1D1D')
        text_editor.pack( side='right',padx=50,pady=20,fill='both',expand=True)

        

        #------------------------------------------------------------------------------------------------------------------------
        # left half (image_frame)
        
        #image label
        self.no_image = CTkImage(Image.open('noImage.jpg'),size=(400,300))
        self.handwritten_image_label = CTkLabel(image_frame, text="",image=self.no_image)
        self.handwritten_image_label.pack(side='top',pady=(20,0))

        #insert image button and scan image button
        insert_scan_frame = CTkFrame(image_frame,fg_color='#1D1D1D')
        insert_scan_frame.pack(pady=(30,20))

        insert_image_button = CTkButton(insert_scan_frame, text='Insert Image', font=('', 25), width=180, height=50, corner_radius=20,command=lambda: self.insert_image())
        insert_image_button.pack(side='left',padx=(0,20))

        scan_button = CTkButton(insert_scan_frame, text='scan', font=('', 25), width=180, height=50, corner_radius=20,command=lambda: self.scan() if self.default_image_path!=None else None)
        scan_button.pack(side='right')

        self.image_path_label = CTkLabel(image_frame, text='', font=('', 10),fg_color='#2B2B2B' ,width=400, height=50, corner_radius=20)
        self.image_path_label.pack(pady=(0,20),padx=30,expand=True)

        #------------------------------------------------------------------------------------------------------------------------
        # right half (text_editor)
        self.font_name = StringVar(root)
        self.font_name.set("Arial")
        self.font_size = IntVar(root)
        self.font_size.set(25)
        self.AI_choose = StringVar(root)
        self.AI_choose.set('HTR pipeline(page reader)')

        # menu bar for file, edit
        menu_bar = CTkMenuBar(text_editor,bg_color='#1D1D1D')
        menu_bar.pack(fill='both',expand=True)

        file_bar = menu_bar.add_cascade("File")
        edit_bar = menu_bar.add_cascade("Edit")
        about_bar = menu_bar.add_cascade("About")
        self.HTR_AI_optionMenu = CTkOptionMenu(menu_bar,variable=self.AI_choose,values=['HTR pipeline(page reader)','HTR mltu(sentence reader)'],bg_color='#1D1D1D',fg_color='#1D1D1D',button_color='#1D1D1D',command=lambda x: self.choose_AI())
        
        # file menu
        file_drop_down = CustomDropdownMenu(widget=file_bar)
        file_drop_down.add_option('New', lambda: self.new_file())
        file_drop_down.add_option("Save", lambda: self.save_file(root))
        file_drop_down.add_separator()
        file_drop_down.add_option("Exit", lambda: self.quit(root))

        # edit menu
        edit_drop_down = CustomDropdownMenu(widget=edit_bar)
        edit_drop_down.add_option("Cut", lambda: self.cut(root))
        edit_drop_down.add_option("Copy", lambda: self.copy(root))
        edit_drop_down.add_option("Paste", lambda: self.paste(root))

        # about menu
        about_drop_down = CustomDropdownMenu(widget=about_bar)
        about_drop_down.add_option("About", lambda: self.about())

        # HTR AI option menu
        self.HTR_AI_optionMenu.grid(row=0,column=4)
        menu_bar.grid_columnconfigure(3, weight=1)

        self.text_area = CTkTextbox(text_editor,font=(self.font_name.get(),self.font_size.get()),width=450, height=450,undo=True)
        self.text_area.pack()

        editor_options_frame = CTkFrame(text_editor)
        editor_options_frame.pack(fill='both',expand=True)

        color_button = CTkButton(editor_options_frame, text='color', font=('', 15), corner_radius=20,command=lambda: self.change_color())
        color_button.pack(side='left',pady=10,padx=10)

        font_box = CTkOptionMenu(editor_options_frame,variable=self.font_name, values= font.families(), command=lambda x: self.Change_font())
        font_box.pack(side='left',padx=10)

        size_box = CTkSpinbox(editor_options_frame,font=('', 15),width=100,height=30,min_value=1, max_value=100,start_value=25 , variable=self.font_size, command=lambda x: self.Change_font())
        size_box.pack(side='right',padx=10)


        root.mainloop()

