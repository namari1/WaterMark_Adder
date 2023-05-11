from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

global img, filename

font_options = ["Arial", "Bahnschrift", "Calibri", "Cambria", "Candara", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Courier New",
                "Ebrima", "Franklin Gothic Medium", "Gabriola", "Gadugi", "Georgia", "Impact", "Ink Free", "Javanese Text", "Leelawadee UI",
                "Lucida Console", "Malgun Gothic", "Mongolian Baiti", "MV Boli", "Myanmar Text", "Nirmala UI", "Palatino Linotype",
                "Segoe UI", "Sitka Text", "Sylfaen", "Symbol", "Tahoma", "Times New Roman", "Trebuchet MS",
                "Verdana", "Webdings"]

font_dict = {"Arial": "arial.ttf", "Bahnschrift": "bahnschrift.ttf", "Calibri": "calibri.ttf", "Cambria": "cambriab.ttf", "Candara": "candara.ttf", "Comic Sans MS": "comic.ttf", "Consolas": "consola.ttf", "Constantia": "constan.ttf", "Corbel": "corbel.ttf", "Courier New": "cour.ttf",
                "Ebrima": "ebrima.ttf", "Franklin Gothic Medium": "framd.ttf", "Gabriola": "Gabriola.ttf", "Gadugi": "gadugi.ttf", "Georgia": "georgia.ttf", "Impact": "impact.ttf", "Ink Free": "Inkfree.ttf", "Javanese Text": "javatext.ttf", "Leelawadee UI": "leelawui.ttf",
                "Lucida Console": "lucon.TTF", "Malgun Gothic": "malgun.ttf", "Mongolian Baiti": "monbaiti.ttf", "MV Boli": "mvboli.ttf", "Myanmar Text": "mmrtext.ttf", "Nirmala UI": "Nirmala.ttf", "Palatino Linotype": "pala.ttf",
                "Segoe UI": "segoeui.ttf", "Sitka Text": "SitkaVF.ttf", "Sylfaen": "sylfaen.ttf", "Symbol": "symbol.ttf", "Tahoma": "tahoma.ttf", "Times New Roman": "times.ttf", "Trebuchet MS": "trebuc.ttf",
                "Verdana": "verdana.ttf", "Webdings": "webdings.ttf"}


def change_size(image):
    width = image.width
    height = image.height
    if width and height > 3000:
        width = int(width / 15)
        height = int(height / 15)
    elif width and height > 1200:
        width = int(width / 4)
        height = int(height / 4)
    elif width and height > 400:
        width = int(width / 2)
        height = int(height / 2)
    return width, height


def open_img():
    global img, filename
    filename = filedialog.askopenfilename()
    img = Image.open(filename)
    width, height = change_size(img)
    img = img.resize((width, height), Image.BICUBIC)
    image_size = Label(text=f"Image Width: {width}\nImage Height: {height}")
    image_size.grid(row=10, column=0)
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)


def add_watermark():
    global img, filename
    img = Image.open(filename)
    img.putalpha(255)
    width, height = change_size(img)
    img = img.resize((width, height), Image.BICUBIC)
    txt_img = Image.new("RGBA", img.size, (255,255,255,0))
    drawing = ImageDraw.Draw(txt_img)
    pos = (float(x_pos.get()), float(y_pos.get()))
    red = int(red_scale.get())
    green = int(green_scale.get())
    blue = int(blue_scale.get())
    transparency = int(opacity_scale.get())
    font_color = (red, green, blue, transparency)
    text = text_entry.get()
    text_size = int(size_scale.get())
    font_chosen = font_dict[font_var.get()]
    font = ImageFont.truetype(font_chosen, text_size, encoding="unic")
    drawing.text(pos, text, fill=font_color, font=font)
    rotation = angle_var.get()
    txt_img = txt_img.rotate(rotation)
    composite = Image.alpha_composite(img, txt_img)
    if "PNG" or "png" in filename:
        composite.save(f"{filename}.png")
    else:
        composite.save(f"{filename}.jpg")
    img = ImageTk.PhotoImage(composite)
    panel.config(image=img)


window = Tk()
window.title("Watermark Adder")
window.config(padx=20, pady=20)
window.resizable(width=True, height=True)

image_label = Label(text="Image", font=("Arial", 14, "bold"))
image_label.grid(row=0, column=0, columnspan=2, sticky="EW")

properties = Label(text="Properties", font=("Arial", 14, "bold"))
properties.grid(row=0, column=2, columnspan=2, sticky="EW")

add_image = Button(text="Upload Image", command=open_img)
add_image.grid(row=1, column=0, columnspan=2, sticky="EW")

panel = Label()
panel.grid(row=2, column=0, rowspan=8, columnspan=2, sticky="EW")

text_label = Label(text="Text:")
text_label.grid(row=1, column=2, sticky="EW")

text_entry = Entry()
text_entry.grid(row=1, column=3, sticky="EW")

size_label = Label(text="Text Size:")
size_label.grid(row=2, column=2, sticky="EW")
size_var = IntVar()
size_scale = Scale(window, variable=size_var, from_=10, to=80, orient=HORIZONTAL)
size_scale.grid(row=2, column=3, sticky="EW")

font_label = Label(text="Font:")
font_label.grid(row=3, column=2, sticky="EW")
font_var = StringVar()
font_drop = OptionMenu(window, font_var, *font_options)
font_drop.grid(row=3, column=3, sticky="EW")

x_pos_label = Label(text="X Position:")
y_pos_label = Label(text="Y Position:")
x_pos_label.grid(row=4, column=2, sticky="EW")
y_pos_label.grid(row=5, column=2, sticky="EW")

x_pos = Entry()
x_pos.grid(row=4, column=3, sticky="EW")
y_pos = Entry()
y_pos.grid(row=5, column=3, sticky="EW")

opacity_label = Label(text="Opacity:")
opacity_label.grid(row=6, column=2, sticky="EW")
opacity_var = IntVar()
opacity_scale = Scale(window, variable=opacity_var, from_=0, to=255, orient=HORIZONTAL)
opacity_scale.grid(row=6, column=3, sticky="EW")

red_label = Label(text="Red:")
red_label.grid(row=7, column=2, sticky="EW")
red_var = IntVar()
red_scale = Scale(window, variable=red_var, from_=0, to=255, orient=HORIZONTAL)
red_scale.grid(row=7, column=3, sticky="EW")

blue_label = Label(text="Blue:")
blue_label.grid(row=8, column=2, sticky="EW")
blue_var = IntVar()
blue_scale = Scale(window, variable=blue_var, from_=0, to=255, orient=HORIZONTAL)
blue_scale.grid(row=8, column=3, sticky="EW")

green_label = Label(text="Green:")
green_label.grid(row=9, column=2, sticky="EW")
green_var = IntVar()
green_scale = Scale(window, variable=green_var, from_=0, to=255, orient=HORIZONTAL)
green_scale.grid(row=9, column=3, sticky="EW")

angle_label = Label(text="Angle:")
angle_label.grid(row=10, column=2, sticky="EW")
angle_var = IntVar()
angle_scale = Scale(window, variable=angle_var, from_=0, to=360, orient=HORIZONTAL)
angle_scale.grid(row=10, column=3, sticky="EW")

add = Button(text="Add Watermark", command=add_watermark)
add.grid(row=11, column=2, columnspan=2, sticky="EW", padx=5)

window.mainloop()
