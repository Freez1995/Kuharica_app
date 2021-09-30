import sqlite3
from tkinter import *
from tkinter import font
from tkinter import messagebox
import yagmail
from tkinter import ttk
from tkinter import colorchooser
import os
import os.path
from reportlab.pdfgen import canvas
import pygetwindow
import pyautogui
from PIL import Image
import time
from reportlab.lib.units import inch


db = sqlite3.connect("recipes.db")
cursor = db.cursor()

list_of_recipes = list()
list_of_ingredients = list()
list_of_picked_ingredients = list()
fonts = ['System', 'Terminal', 'Fixedsys', 'Modern', 'Roman', 'Script', 'Courier', 'MS Serif', 'MS Sans Serif',
         'Small Fonts', 'Marlett', 'Arial', 'Arabic Transparent', 'Arial Baltic', 'Arial CE', 'Arial CYR',
         'Arial Greek', 'Arial TUR', 'Arial Black', 'Bahnschrift Light', 'Bahnschrift SemiLight', 'Bahnschrift',
         'Bahnschrift SemiBold', 'Bahnschrift Light SemiCondensed', 'Bahnschrift SemiLight SemiConde',
         'Bahnschrift SemiCondensed', 'Bahnschrift SemiBold SemiConden', 'Bahnschrift Light Condensed',
         'Bahnschrift SemiLight Condensed', 'Bahnschrift Condensed', 'Bahnschrift SemiBold Condensed', 'Calibri',
         'Calibri Light', 'Cambria', 'Cambria Math', 'Candara', 'Candara Light', 'Comic Sans MS', 'Consolas',
         'Constantia', 'Corbel', 'Corbel Light', 'Courier New', 'Courier New Baltic', 'Courier New CE',
         'Courier New CYR', 'Courier New Greek', 'Courier New TUR', 'Ebrima', 'Franklin Gothic Medium', 'Gabriola',
         'Gadugi', 'Georgia', 'Impact', 'Ink Free', 'Javanese Text', 'Leelawadee UI', 'Leelawadee UI Semilight',
         'Lucida Console', 'Lucida Sans Unicode', 'Malgun Gothic', '@Malgun Gothic', 'Malgun Gothic Semilight',
         '@Malgun Gothic Semilight', 'Microsoft Himalaya', 'Microsoft JhengHei', '@Microsoft JhengHei',
         'MS Gothic', '@MS Gothic', 'MS UI Gothic', '@MS UI Gothic', 'MS PGothic', '@MS PGothic', 'MV Boli',
         'Myanmar Text', 'Nirmala UI', 'Nirmala UI Semilight', 'Palatino Linotype', 'Segoe MDL2 Assets', 'Segoe Print',
         'Segoe Script', 'Segoe UI', 'Segoe UI Black', 'Segoe UI Emoji', 'Segoe UI Historic', 'Segoe UI Light',
         'Segoe UI Semibold', 'Segoe UI Semilight', 'Segoe UI Symbol', 'SimSun', '@SimSun', 'NSimSun', '@NSimSun',
         'SimSun-ExtB', '@SimSun-ExtB', 'Sitka Small', 'Sitka Text', 'Sitka Subheading', 'Sitka Heading',
         'Sitka Display', 'Sitka Banner', 'Sylfaen', 'Symbol', 'Tahoma', 'Times New Roman', 'Times New Roman Baltic',
         'Times New Roman CE', 'Times New Roman CYR', 'Times New Roman Greek', 'Times New Roman TUR', 'Trebuchet MS',
         'Verdana', 'Webdings', 'Wingdings', 'HoloLens MDL2 Assets', 'Digital-7 Mono',
         'Dungeon', 'hooge 05_53', 'hooge 05_54', 'hooge 05_55', 'LCDMono2', 'Lato', 'Lato Light', 'Lato Semibold']
font_height = [10, 11, 12, 13, 14, 18]
color_count = 0
indentation_count = 1
info_count = 0
info_count_rezanje = 0

# execute the query.

command_recipes = """SELECT RECEPTI.recept
             FROM RECEPTI JOIN KUHARICA JOIN NAMIRNICE
             ON KUHARICA.recept_id = RECEPTI.recept_id AND
             KUHARICA.namirnica_id = NAMIRNICE.namirnica_id
             WHERE NAMIRNICE.namirnica = ?; """

command_ingredients = """SELECT NAMIRNICE.namirnica
             FROM RECEPTI JOIN KUHARICA JOIN NAMIRNICE
             ON KUHARICA.recept_id = RECEPTI.recept_id AND
             KUHARICA.namirnica_id = NAMIRNICE.namirnica_id
             WHERE RECEPTI.recept = ?; """

command_ingredients_list = """SELECT NAMIRNICE.namirnica
                            FROM NAMIRNICE"""

command_recipe_desc = """SELECT RECEPTI_OPIS.opis_recepta
             FROM RECEPTI JOIN RECEPTI_OPIS 
             ON RECEPTI_OPIS.recept_id = RECEPTI.recept_id
             WHERE RECEPTI.recept = ?; """

cursor.execute(command_ingredients_list)
for row in cursor:
    list_of_ingredients.append(row[0])


root = Tk()

HEIGHT = 500
WIDTH = 300
forte_font = font.Font(family='Forte')
#                       Program settings:
# screen adjust:
screen = Canvas(root, height=HEIGHT, width=WIDTH)
screen.pack()

# app name, screen is not resizable:
root.title("Don't throw!")
root.resizable(False, False)


# program icon:
root.iconbitmap("icon_circle.ico")


#                        Main screen button functions


def close_cooking_window():
    top_cooking.destroy()
    root.deiconify()


def close_shopping_window():
    top_shopping.destroy()
    root.deiconify()


def close_and_save_make_button():
    top_make_buttons.destroy()
    for ingredient in list_of_picked_ingredients:
        cursor.execute(command_recipes, [ingredient])
        for x in cursor:
            recipe = x[0]
            if recipe in list_of_recipes:
                continue
            else:
                list_of_recipes.append(recipe)

    for recipe in list_of_recipes:
        cursor.execute(command_ingredients, [recipe])
        ingredient_list = list()
        for row_second in cursor:
            ingredient_list.append(row_second[0])
        target_ingredient = ""
        count = 0
        for item in ingredient_list:
            count += 1
            if count == len(ingredient_list):
                target_ingredient += item
            else:
                target_ingredient += item + ", "
        listbox_recipes.insert("end", recipe + " (" + "glavni sastojci:" + " " + target_ingredient + ")")
    list_of_picked_ingredients.clear()
    list_of_recipes.clear()


def close_and_clear_make_button():
    top_make_buttons.destroy()
    listbox_recipes.delete(0, "end")
    list_of_picked_ingredients.clear()


def recipe_select(event):
    raw_string = ""
    if listbox_recipes.curselection() != ():
        raw_string = listbox_recipes.get(listbox_recipes.curselection())
    recipe = raw_string.split(" (")[0]
    pick_recipe_entry.delete(0, "end")
    pick_recipe_entry.insert("end", recipe)


def send_email():
    message_list = list()
    recipe = pick_recipe_entry.get()
    cursor.execute(command_recipe_desc, [recipe])
    check = cursor.fetchone()
    if check is None:
        messagebox.showinfo("Obavijest", "Označite recept iz liste.")
    else:
        receiver = pick_email_entry.get()
        if receiver == "" or receiver == "pero.peric@gmail.com":
            messagebox.showerror("Greška", "Nažalost niste upisali valjanu e-mail adresu.")
        else:
            cursor.execute(command_recipe_desc, [recipe])
            for recipe_desc in cursor:
                message = recipe_desc[0]
                message_list.append(message)
            sender_email = "dont.throvv.app@gmail.com"
            sender_password = "don'tthrow"
            receiver_email = receiver
            subject = "Uživajte u receptu i dobar tek!"
            yag = yagmail.SMTP(user=sender_email, password=sender_password)
            yag.send(receiver_email, subject, message_list)
            info_message = "E-mail uspješno poslan na "
            info_message += receiver_email
            messagebox.showinfo("Obavijest", info_message)

def recipe_open_desc():
    recipe = pick_recipe_entry.get()
    cursor.execute(command_recipe_desc, [recipe])
    check = cursor.fetchone()
    if check is None:
        messagebox.showerror("Greška", "Nema rezultata za Vašu pretragu ili\n"
                                       "      niste označili recept iz liste.")
    else:
        recipe = pick_recipe_entry.get()
        top_recipe_desc = Toplevel()
        top_recipe_desc.iconbitmap("icon_circle.ico")
        top_recipe_desc.geometry('480x550')
        top_recipe_desc.config(bg="#D1D199")
        top_recipe_desc.resizable(False, False)
        frame_recipe_desc = Frame(top_recipe_desc, bg="#D1D199", bd=2)
        recipe_scroll_vertical = Scrollbar(frame_recipe_desc, orient="vertical")
        frame_recipe_desc.pack(expand=True, fill='both')
        text_for_recipe = Text(frame_recipe_desc, bg="#D1D199", yscrollcommand=recipe_scroll_vertical.set)
        cursor.execute(command_recipe_desc, [recipe])
        description = ""
        for recipe_desc in cursor:
            description = recipe_desc[0]
        text_for_recipe.insert(INSERT, description)
        text_for_recipe.configure(font=("Verdana", 10))
        recipe_scroll_vertical.config(command=text_for_recipe.yview)
        recipe_scroll_vertical.pack(side="right", fill="y")
        text_for_recipe.pack(expand=True, fill='both')
        text_for_recipe.config(state=DISABLED)


def cooking_window():
    global top_cooking
    global listbox_recipes
    top_cooking = Toplevel()
    top_cooking.resizable(False, False)
    top_cooking.protocol("WM_DELETE_WINDOW", close_cooking_window)
    root.withdraw()
    height_cooking = 550
    width_cooking = 700
    screen_cooking = Canvas(top_cooking, height=height_cooking, width=width_cooking)
    screen_cooking.pack()
    top_cooking.title("Kuhaj sa Don't throw!")
    top_cooking.iconbitmap("icon_circle.ico")
    frame_cooking = Frame(top_cooking, bg="#548A2C", bd=2)
    frame_cooking.place(relx=0, rely=0, relwidth=1, relheight=1)
    cooking_image = PhotoImage(file="cooking_part_image.png")
    cooking_image_pack = Label(top_cooking, image=cooking_image, borderwidth=0, highlightthickness=0, compound="center",
                               bg="#548A2C")
    cooking_image_pack.place(relx=0.015, rely=0.015)
    cooking_image_pack.photo = cooking_image

    pick_ingredient_text = Label(frame_cooking,
                                 text="Odaberite namirnicu koju\nželite iskoristiti:",
                                 font=("Franklin Gothic Medium Cond", 12, "bold"), bg="#548A2C", justify="left")
    pick_ingredient_text.place(relx=0.01, rely=0.2)
    pick_ingredient_text_1 = Label(frame_cooking, text="Iz liste recepata upišite\nili odaberite željeni recept:",
                                   font=("Franklin Gothic Medium Cond", 12, "bold"), bg="#548A2C", justify="left")
    pick_ingredient_text_1.place(relx=0.01, rely=0.4)
    pick_ingredient_text_2 = Label(frame_cooking, text="Proslijedite recept e-mailom",
                                   font=("Franklin Gothic Medium Cond", 12, "bold"), bg="#548A2C", justify="left")
    pick_ingredient_text_2.place(relx=0.01, rely=0.7)
    recipes_list_text = Label(top_cooking,
                              text="Recepti koji sadrže unesene namirnice:",
                              font=("Franklin Gothic Medium Cond", 12, "bold"), bg="#548A2C")
    recipes_list_text.place(relx=0.35, rely=0.07)
    pick_ingredient_button = Button(frame_cooking, text="Namirnice", bg="#e0a307",
                                    font=("Franklin Gothic Medium Cond", 10, "bold"),
                                    highlightthickness=4,
                                    highlightcolor="#21ad4b",
                                    highlightbackground="#479600",
                                    borderwidth=4, command=make_buttons)
    pick_ingredient_button.place(relx=0.06, rely=0.32)

    pick_recipe_button = Button(frame_cooking, text="Otvori recept", bg="#e0a307",
                                font=("Franklin Gothic Medium Cond", 10, "bold"),
                                highlightthickness=2, highlightcolor="#21ad4b",
                                highlightbackground="#479600",
                                borderwidth=3,
                                command=recipe_open_desc)
    pick_recipe_button.place(relx=0.05, rely=0.62)
    global pick_recipe_entry
    pick_recipe_entry = Entry(frame_cooking, bd=2, bg="#D1D199")
    pick_recipe_entry.place(relx=0.01, rely=0.535, relwidth=0.3, relheight=0.06)
    pick_recipe_entry.insert(0, 'označeni recept iz tablice recepata')
    pick_recipe_entry.bind('<FocusIn>', on_pick_recipe_entry_click)
    pick_recipe_entry.bind('<FocusOut>', on_pick_recipe_entry_focusout)
    global pick_email_entry
    pick_email_button = Button(frame_cooking, text="Proslijedi", bg="#e0a307",
                               font=("Franklin Gothic Medium Cond", 10, "bold"),
                               highlightthickness=2, highlightcolor="#21ad4b",
                               highlightbackground="#479600",
                               borderwidth=3,
                               command=send_email)
    pick_email_button.place(relx=0.065, rely=0.87)
    pick_email_entry = Entry(frame_cooking, bd=2, bg="#D1D199")
    pick_email_entry.place(relx=0.01, rely=0.79, relwidth=0.3, relheight=0.06)
    pick_email_entry.insert(0, 'pero.peric@gmail.com')
    pick_email_entry.bind('<FocusIn>', on_pick_email_entry_click)
    pick_email_entry.bind('<FocusOut>', on_pick_email_entry_focusout)
    frame_for_listbox = Frame(frame_cooking, height=26,
                              width=74)
    frame_for_listbox.place(relx=0.35, rely=0.125, relwidth=0.637, relheight=0.865)
    listbox_scroll_vertical = Scrollbar(frame_for_listbox, orient="vertical")
    listbox_scroll_horizontal = Scrollbar(frame_for_listbox, orient="horizontal")
    listbox_recipes = Listbox(frame_for_listbox,
                              bg="#D1D199",
                              activestyle='dotbox',
                              yscrollcommand=listbox_scroll_vertical.set,
                              xscrollcommand=listbox_scroll_horizontal.set,
                              font=("Times", 9))
    listbox_recipes.bind('<<ListboxSelect>>', recipe_select)
    listbox_scroll_vertical.config(command=listbox_recipes.yview)
    listbox_scroll_horizontal.config(command=listbox_recipes.xview)
    listbox_scroll_vertical.pack(side="right", fill="y")
    listbox_scroll_horizontal.pack(side="bottom", fill="x")
    listbox_recipes.pack(fill="both", expand=1)


def shopping_cart_window():
    global text_for_shopping
    global top_shopping
    global font_option_combo
    global pick_email_entry
    top_shopping = Toplevel()
    root.withdraw()
    top_shopping.resizable(False, False)
    top_shopping.geometry('400x600')
    top_shopping.config(bg="#548A2C")
    top_shopping.title("Moja shopping košarica")
    top_shopping.iconbitmap("icon_circle.ico")
    frame_shopping = Frame(top_shopping, bg="#80a840", bd=4)
    frame_shopping.place(relx=0.02, rely=0.135, relwidth=0.96, relheight=0.72)
    top_shopping.protocol("WM_DELETE_WINDOW", close_shopping_window)
    text_for_shopping = Text(frame_shopping, bg="#D1D199")
    text_for_shopping.pack(expand=True, fill='both')

    def create_pdf():
        username = os.getlogin()
        x2, y2 = pyautogui.size()
        x2, y2 = int(str(x2)), int(str(y2))
        # print(x2, y2)
        z3 = "Moja shopping košarica"
        my = pygetwindow.getWindowsWithTitle(z3)[0]
        # quarter of screen screensize
        x3 = x2 // 2
        y3 = y2 // 2
        my.resizeTo(x3, y3)
        # top-left
        my.moveTo(0, 0)
        time.sleep(3)
        my.activate()
        time.sleep(1)

        # save screenshot
        p = pyautogui.screenshot()
        p.save(f"C:\\Users\\{username}\\Desktop\\Lista_za_trgovinu.png")
        im = Image.open(f"C:\\Users\\{username}\\Desktop\\Lista_za_trgovinu.png")
        im_crop = im.crop((17, 118, 392, 542))
        im_crop.save(f"C:\\Users\\{username}\\Desktop\\Lista_za_trgovinu.png", quality=100)
        # create pdf
        image = Image.open(f"C:\\Users\\{username}\\Desktop\\Lista_za_trgovinu.png", 'r')  # Fetch picture
        img = Image.new('RGB', (210, 297), "#80a840")
        img.save(f"C:\\Users\\{username}\\Desktop\\green_colored.png")
        time.sleep(2)
        image_1 = Image.open(f"C:\\Users\\{username}\\Desktop\\green_colored.png", 'r')
        image_2 = Image.open("cooking_part_image_pdf.png")
        file_name = "Moja_shopping_lista.pdf"
        save_name = os.path.join(os.path.expanduser("~"), "Desktop/", file_name)
        document_title = ""
        title = "Lista za trgovinu"
        pdf = canvas.Canvas(save_name)
        pdf.setTitle(document_title)
        pdf.drawInlineImage(image_1, 0, 0, width=10*inch, height=13*inch)
        pdf.drawInlineImage(image_2, 220, 730)
        pdf.setFont("Courier-Bold", 25)
        pdf.drawString(190, 650, title)
        pdf.line(170, 640, 460, 640)
        pdf.drawInlineImage(image, 130, 170)
        os.remove(f'C:\\Users\\{username}\\Desktop\\Lista_za_trgovinu.png')
        os.remove(f'C:\\Users\\{username}\\Desktop\\green_colored.png')
        pdf.save()
        messagebox.showinfo("Obavijest", "PDF je uspješno generiran, "
                                         "te je pohranjen na radnoj površini.")

    def send_shopping_email():
        shopping_list = text_for_shopping.get("0.0", "end")
        if shopping_list == "\n":
            messagebox.showwarning("Upozorenje", "Poslati prazan e-mail?")
        else:
            reciever = pick_email_entry.get()
            if reciever == "" or reciever == "pero.peric@gmail.com":
                messagebox.showerror("Greška", "Nažalost niste upisali valjanu e-mail adresu.")
            else:
                shopping_list_final = text_for_shopping.get("0.0", "end")
                sender_email = "dont.throvv.app@gmail.com"
                sender_password = "don'tthrow"
                receiver_email = reciever
                subject = "Moja shopping lista"
                yag = yagmail.SMTP(user=sender_email, password=sender_password)
                yag.send(receiver_email, subject, shopping_list_final)
                info_message = "E-mail uspješno poslan na "
                info_message += receiver_email
                messagebox.showinfo("Obavijest", info_message)

    def text_changes(*event):
        global current_font
        # On every KeyRelease with the Text widget in focus,
        # it get the current tag, start index and current index.
        new_font_type = font_option_combo.get()
        new_font_height = int(font_height_combo.get())
        current_font = font.Font(family="".join(new_font_type), size=new_font_height)
        text_for_shopping.configure(font=current_font)
        text_for_shopping.tag_add(current_tag.get(), start_index.get(), current_index())
        text_for_shopping.tag_config(current_tag.get(), font=current_font)

    def current_index():
        # Return current cursor position in the text widget
        return text_for_shopping.index(INSERT)

    def font_size_func(*new_var):
        # Create a new tag with a new start index / position
        start_index.set(current_index())
        current_tag.set(current_index())

    def make_bold():
        try:
            current_tags = text_for_shopping.tag_names("sel.first")
            if "bt" in current_tags:
                text_for_shopping.tag_remove("bt", "sel.first", "sel.last")
            else:
                text_for_shopping.tag_add("bt", "sel.first", "sel.last")
            current_font = font.Font(text_for_shopping, text_for_shopping.cget("font"))
            current_font.configure(weight="bold")
            text_for_shopping.tag_configure("bt", font=current_font)
        except TclError:
            messagebox.showinfo('Greška:', "Označite (zaplavite) tekst koji želite zadebljati.")

    def make_italic():
        try:
            current_tags = text_for_shopping.tag_names("sel.first")
            if "it" in current_tags:
                text_for_shopping.tag_remove("it", "sel.first", "sel.last")
            else:
                text_for_shopping.tag_add("it", "sel.first", "sel.last")
            current_font = font.Font(text_for_shopping, text_for_shopping.cget("font"))
            current_font.configure(slant="italic")
            text_for_shopping.tag_configure("it", font=current_font)
        except TclError:
            messagebox.showinfo('Greška:', "Označite (zaplavite) tekst koji želite ukositi.")

    def make_underline():
        try:
            current_tags = text_for_shopping.tag_names("sel.first")
            if "ul" in current_tags:
                text_for_shopping.tag_remove("ul", "sel.first", "sel.last")
            else:
                text_for_shopping.tag_add("ul", "sel.first", "sel.last")
            current_font = font.Font(text_for_shopping, text_for_shopping.cget("font"))
            current_font.configure(underline=True)
            text_for_shopping.tag_configure("ul", font=current_font)
        except TclError:
            messagebox.showinfo('Greška:', "Označite (zaplavite) tekst koji želite podcrtati.")

    def change_font_color():
        try:
            check_sel = text_for_shopping.tag_names("sel.first")
            if check_sel != "":
                global color_count
                color_count += 1
                my_color = colorchooser.askcolor()[1]
                current_tags = text_for_shopping.tag_names("sel.first")

                if my_color:
                    color_font = font.Font(text_for_shopping, text_for_shopping.cget("font"))

                    text_for_shopping.tag_configure("colored" + str(color_count), font=color_font,
                                                    foreground=my_color)
                    if "colored" + str(color_count) in current_tags:
                        text_for_shopping.tag_remove("colored" + str(color_count), "sel.first", "sel.last")
                    else:
                        text_for_shopping.tag_add("colored" + str(color_count), "sel.first", "sel.last")
        except TclError:
            messagebox.showinfo("Informacija", "Prvo upišite i označite (zaplavite) tekst.\n"
                                               "Nakon toga odaberite boju.")

    def edit_text(event):
        global indentation_count
        global info_count
        if variable.get() == "None":
            indentation_count = 1
            pass
        else:
            if info_count == 0:
                message = messagebox.askyesno("Obavijest", "Odaberite 'None' ukoliko ne želite koristiti listu."
                                                           "\n                     Isključi ovu obavijest?")
                if message is True:
                    info_count += 1
                else:
                    info_count = 0
            try:
                int(variable.get())
                string = "\n" + "    " + str(indentation_count) + "." + "  "
                text_for_shopping.tag_add(current_tag.get(), start_index.get(), current_index())
                text_for_shopping.insert("end", string)
                indentation_count += 1
                return 'break'
            except:
                string = "\n" + "    " + variable.get() + "  "
                text_for_shopping.tag_add(current_tag.get(), start_index.get(), current_index())
                text_for_shopping.insert("end", string)
                return 'break'

    button_font_bold = font.Font(family='Helvetica', weight='bold')
    bold_text = Button(top_shopping, text="B", font=button_font_bold, width=1, height=1, bg="#548A2C", borderwidth=0,
                       command=make_bold)
    bold_text.place(relx=0.273, rely=0.055)
    button_font_italic = font.Font(family='Helvetica', weight='bold', slant="italic")
    italic_text = Button(top_shopping, text="I", font=button_font_italic, width=1, height=1, bg="#548A2C",
                         borderwidth=0,
                         command=make_italic)
    italic_text.place(relx=0.398, rely=0.055)
    button_font_underline = font.Font(family='Arial', weight='bold', underline=True)
    underline_text = Button(top_shopping, text="U", font=button_font_underline, width=1, height=1, bg="#548A2C",
                            borderwidth=0,
                            command=make_underline)
    underline_text.place(relx=0.335, rely=0.055)
    variable = StringVar(top_shopping)
    variable.set("None")  # default value
    editing_text = OptionMenu(top_shopping, variable, "◆", "•", "▪", "1", "None", command=font_size_func)
    editing_text.config(borderwidth=0)
    editing_text.place(relx=0.7, rely=0.045)
    if variable != "None":
        text_for_shopping.bind("<Return>", edit_text)
    editing_text_label = Label(top_shopping, text="Oblikujte listu:", font=("Times new roman", 12), bg="#548A2C")
    editing_text_label.place(relx=0.65, rely=0)
    color_text = Button(top_shopping, text="Boja \nteksta", width=5, height=2, command=change_font_color)
    color_text.place(relx=0.50, rely=0.021)
    font_option_combo = ttk.Combobox(top_shopping, width=18, value=fonts)
    font_height_combo = ttk.Combobox(top_shopping, width=6, value=font_height)
    font_option_combo.current(0)
    font_height_combo.current(0)
    font_option_combo.bind("<<ComboboxSelected>>", font_size_func)
    font_height_combo.bind("<<ComboboxSelected>>", font_size_func)
    font_option_combo.place(relx=0.02, rely=0.01)
    font_height_combo.place(relx=0.02, rely=0.06)
    send_email_button = Button(top_shopping, text="Proslijedi e-mailom", bg="#e0a307",
                               font=("Franklin Gothic Medium Cond", 10, "bold"),
                               highlightthickness=2, highlightcolor="#21ad4b",
                               highlightbackground="#479600",
                               borderwidth=3,
                               command=send_shopping_email)
    send_email_button.place(relx=0.1, rely=0.93)
    pick_email_entry = Entry(top_shopping, bd=2)
    pick_email_entry.place(relx=0.072, rely=0.885, relwidth=0.4, relheight=0.04)
    pick_email_entry.insert(0, 'pero.peric@gmail.com')
    pick_email_entry.bind('<FocusIn>', on_pick_email_entry_click)
    pick_email_entry.bind('<FocusOut>', on_pick_email_entry_focusout)
    export_pdf = Button(top_shopping, text="Izvoz u PDF formatu", bg="#e0a307",
                        font=("Franklin Gothic Medium Cond", 10, "bold"),
                        highlightthickness=2, highlightcolor="#21ad4b",
                        highlightbackground="#479600",
                        borderwidth=3,
                        command=create_pdf)
    export_pdf.place(relx=0.55, rely=0.93)

    # Initialize start_index and current_tag
    start_index = StringVar()
    current_tag = StringVar()
    start_index.set(current_index())
    current_tag.set(current_index())
    # When the text entry has focus, every key release will run the
    # text_changes function
    text_for_shopping.bind('<KeyRelease>', text_changes)


#                           Pre made entry

# email entry pretext
def on_pick_email_entry_click(event):
    # function that gets called whenever entry is clicked
    if pick_email_entry.get() == 'pero.peric@gmail.com':
        pick_email_entry.delete(0, "end")  # delete all the text in the entry
        pick_email_entry.insert(0, '')  # Insert blank for user input
        pick_email_entry.config(fg='black')


def on_pick_email_entry_focusout(event):
    if pick_email_entry.get() == '':
        pick_email_entry.config(fg='grey')
        pick_email_entry.insert(0, 'pero.peric@gmail.com')

# recipe entry pretext


def on_pick_recipe_entry_click(event):
    #  function that gets called whenever entry is clicked
    if pick_recipe_entry.get() == 'označeni recept iz tablice recepata':
        pick_recipe_entry.delete(0, "end")  # delete all the text in the entry
        pick_recipe_entry.insert(0, '')  # Insert blank for user input
        pick_recipe_entry.config(fg='black')


def on_pick_recipe_entry_focusout(event):
    if pick_recipe_entry.get() == '':
        pick_recipe_entry.insert(0, 'označeni recept iz tablice recepata')
        pick_recipe_entry.config(fg='grey')


#                              Picking_ingredients_in_Kuhaj!
def button_pull_update(ingredient):
    string = ""
    if ingredient in list_of_picked_ingredients:
        messagebox.showinfo("Obavijest", "Namirnica je već u listi dodanih namirnica.")

    else:
        list_of_picked_ingredients.append(ingredient)
    count = 0
    for x in list_of_picked_ingredients:
        if count == 0:
            string += x
        else:
            string += "," + x
        text_ingredient.delete(0, "end")
        text_ingredient.insert(0, string)
        count += 1


def close_and_del_ingredient():
    if messagebox.askokcancel("Izlaz", "Izlaskom brišete sve unesene namirnice"):
        list_of_picked_ingredients.clear()
        top_make_buttons.destroy()


def make_buttons():
    global top_make_buttons
    global text_ingredient
    top_make_buttons = Toplevel()
    top_make_buttons.protocol("WM_DELETE_WINDOW", close_and_del_ingredient)
    top_make_buttons.configure(bg="#548A2C")
    top_make_buttons.iconbitmap("icon_circle.ico")
    frame_for_text = Frame(top_make_buttons)
    ingredient_scroll_horizontal = Scrollbar(frame_for_text, orient="horizontal")
    frame_for_text.grid(row=0, column=0, sticky='EW', columnspan=6, ipady=6)
    text_ingredient = Entry(frame_for_text, bd=2, bg="#D1D199", xscrollcommand=ingredient_scroll_horizontal.set)
    ingredient_scroll_horizontal.config(command=text_ingredient.xview)
    ingredient_scroll_horizontal.pack(side="bottom", fill="x")
    text_ingredient.pack(fill="both", expand=1)
    ingredient_button_dict = {}
    col = 0
    ro = 1
    for ingredient in list_of_ingredients:
        # pass each button's text to a function
        action = lambda x=ingredient: button_pull_update(x)
        # create the buttons and assign to ingredient:button-object dict pair
        ingredient_button_dict[ingredient] = Button(top_make_buttons, text=ingredient, width=10, bg="#e0a307",
                                                    font=("Franklin Gothic Medium Cond", 10, "bold"),
                                                    highlightthickness=2, highlightcolor="#21ad4b",
                                                    highlightbackground="#479600", borderwidth=3, command=action)
        ingredient_button_dict[ingredient].grid(row=ro, column=col, pady=5, sticky='EW')
        col += 1
        if col == 6:
            ro += 1
            col = 0
    listbox_recipes.delete("0", "end")
    quit_and_save_button = Button(top_make_buttons, text="spremi i izađi", width=10, bg="#AEC644",
                                  font=("Franklin Gothic Medium Cond", 10, "bold"),
                                  highlightthickness=2, highlightcolor="#21ad4b",
                                  highlightbackground="#479600", borderwidth=3, command=close_and_save_make_button)
    quit_and_save_button.grid(row=ro+1, column=2, pady=5, padx=5, sticky='EW')
    quit_and_clear_button = Button(top_make_buttons, text="obriši i izađi", width=10, bg="#B74F14",
                                   font=("Franklin Gothic Medium Cond", 10, "bold"),
                                   highlightthickness=2, highlightcolor="#21ad4b",
                                   highlightbackground="#479600", borderwidth=3, command=close_and_clear_make_button)
    quit_and_clear_button.grid(row=ro+1, column=3, pady=5, sticky='EW')


#                               App enter screen

# first frame
frame = Frame(screen, bg="#38641A", bd=2)
frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# first page picture frame
frame_pic = Frame(frame, bg="#38641A", bd=2)
frame_pic.place(relx=0.2, rely=0.015, relwidth=0.6, relheight=0.5)

# program png inset
program_image = PhotoImage(file="program_image.png")
program_image_pack = Label(frame_pic, image=program_image, borderwidth=0, highlightthickness=0,
                           bg="#38641A")
program_image_pack.pack()

# start_app_button
start_app_button = Button(frame, text="Kuhaj!", bg="#DCA322", font="Arial 12 bold", command=cooking_window)
start_app_button.place(relx=0.5, rely=0.595, anchor="center")

# shopping_list_button
shopping_app_button = Button(frame, text="Moja košarica", bg="#DCA322", font="Arial 12 bold",
                             command=shopping_cart_window)
shopping_app_button.place(relx=0.5, rely=0.695, anchor="center")

# program info_button
info_button = Button(frame, text="Info", bg="#DCA322", font="Arial 12 bold")
info_button.place(relx=0.5, rely=0.795, anchor="center")


root.mainloop()
