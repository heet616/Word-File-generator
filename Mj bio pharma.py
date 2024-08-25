import tkinter.filedialog
import textract
from tkinter import *
from tkinter import ttk
import csv
import pandas as pd
from docxtpl import DocxTemplate
import os
import docx

file_name_index = []

file_saving_count = 0

company = "MJ biopharma"

# all the column headings
head = ('SR.NO', 'ID  NO. ', 'LOCATION ', 'SECTION', 'MAKE', 'RANGE', 'LEAST COUNT', 'ACCURACY ', 'ACCEPTANCE CRITERIA',
        'Calibration Date', 'Due Date')
# list specifying which headings to add
index_ticked = ['SR.NO', 'ID NO. ', 'LOCATION ']
# variable for the total columns
end_column_head = len(index_ticked)

value_dict = {"Sr no": '', "ID NO.": '', "LOCATION": '', }

# error, current_directory, checkbox_count // total_files_rd, rd_dir, csv
misc = [1, '', 0, [], 'Csv file//csv.csv']

file_name_1 = []

no_of_csv_head = 0

file_list = []

logo_path = 'logo//instotech logo.png'


def login():
    login_root = Tk()
    login_root.title('LOGIN')
    login_root.configure(bg='#BFD1DF')

    # adding logo
    logo = PhotoImage(file=logo_path)
    login_root.iconphoto(False, logo)

    # crating a frame in login window
    login_frame = Frame(login_root, padx=10, pady=10)
    login_frame.pack()

    # label to display the specification about entry (username)
    name_label = Label(login_frame, text='ENTER YOUR USERNAME', padx=10, pady=10)
    name_label.grid(row=0, column=0)

    # entry space for username
    name = Entry(login_frame)
    name.grid(row=0, column=2)

    # label to display the specification about entry (password)
    password_lab = Label(login_frame, text='PLEASE ENTER YOUR PASSWORD', padx=10, pady=10, )
    password_lab.grid(row=2, column=0)

    # entry space for password
    password = Entry(login_frame, show='*')
    password.grid(row=2, column=2)

    check_button = Button(login_frame, text='ENTER',
                          command=lambda: check(login_root, login_frame, name, password, file_list))
    check_button.grid(row=4, column=1)

    cancel_button = Button(login_frame, text='CANCEL', command=login_frame.quit)
    cancel_button.grid(row=4, column=2)
    login_root.mainloop()


def inv_login(name, password, login_frame):
    name.delete(0, END)
    password.delete(0, END)
    # loop to prevent many no of labels saying invalid username or id
    if misc[0] != 1:
        label_error = Label(login_frame, text='Invalid username or Password', padx=10, pady=10, fg='red')
        label_error.grid(row=3, column=0)
        misc[0] += 1


def show_index_files(status_text, value_dict, index_ticked, section, make, var_range, least_count, accuracy, accept,
                     misc):
    if len(index_ticked) > 3:
        value_dict.clear()
        index_ticked.clear()
        index_ticked.append("SR.NO")
        index_ticked.append("ID NO. ")
        index_ticked.append("LOCATION ")
        value_dict["Sr no"] = ""
        value_dict["ID NO."] = ""
        value_dict["LOCATION"] = ""

    selections = [section.get(), make.get(), var_range.get(), least_count.get(), accuracy.get(), accept.get()]

    # checks with box is ticked
    if selections[0] == 'yes':
        index_ticked.append(head[3])
        value_dict['SECTION'] = ''
    if selections[1] == 'yes':
        index_ticked.append(head[4])
        value_dict['MAKE'] = ''
    if selections[2] == 'yes':
        index_ticked.append(head[5])
        value_dict['RANGE'] = ''
    if selections[3] == 'yes':
        index_ticked.append(head[6])
        value_dict['LEAST COUNT'] = ''
    if selections[4] == 'yes':
        index_ticked.append(head[7])
        value_dict['ACCURACY'] = ''
    if selections[5] == 'yes':
        index_ticked.append(head[8])
        value_dict['ACCEPTANCE CRITERIA'] = ''
    index_ticked.append('Calibration Date')
    index_ticked.append('Due Date')
    value_dict['Cal. Date'] = ''
    value_dict['Due Date'] = ''
    value_dict['INSTRUMENT'] = ''
    misc[2] = 1
    status_text.set("Options selected")


def import_files_index(root, status_text, misc):
    files = list(tkinter.filedialog.askopenfilenames())

    if len(files) == 0:
        status_text.set('NO FILES SELECTED')
        return None

    # misc[3] = dirs
    # removing excess things from the file paths
    word_import_count = 0

    for file in files:
        if not file.__contains__("RD") and file != '' and not file.__contains__("index"):
            word_import_count += 1
            status_text.set(str(word_import_count) + ' OUT OF ' + str(len(files)) + 'SELECTED')
            root.update_idletasks()

    misc[2] = len(files)
    misc[3] = files
    # variables for getting the directory of the files
    file_root = os.path.dirname(files[0])
    misc[1] = file_root + '//index.docx'

    status_text.set("FILES SELECTED")
    root.update_idletasks()


def generate_index(root, status_text, misc):
    # adding cal date and due date they are absent
    if len(index_ticked) == 3:
        index_ticked.append('Calibration Date')
        index_ticked.append('Due Date')
        value_dict['Cal. Date'] = ''
        value_dict['Due Date'] = ''
        value_dict['INSTRUMENT'] = ''
    comp_file_count = 0
    files = misc[3]
    # loop that goes through all files and starts filling the Excel sheet
    if len(files) == 0:
        status_text.set("NO FILES SELECTED")
        return None

    wb_new = docx.Document()
    table = wb_new.add_table(rows=1, cols=len(index_ticked))

    row_count = 1
    instrument_in_file = ['']
    for file in files:
        if file.__contains__('index.docx'):
            files.pop(files.index(file))
            continue
        names = []
        word_encoded_value = textract.process(file, input_encoding='ISO-8859-1', output_encoding="UTF-8")
        word_decoded_value = word_encoded_value.decode('UTF-8')

        if file[-1] == 'c':
            word_content = str(word_decoded_value)
            list_word = word_content.split('|')
            for data in list_word:
                data = data.strip()
                if data:
                    names.append(' '.join(data.split()))
        else:
            word_decoded_value = word_decoded_value.split('\n')
            for data in word_decoded_value:
                data = data.strip()
                if data:
                    names.append(' '.join(data.split()))

        for i in value_dict.keys():
            value_dict[i] = ""

        for i in range(len(names)):
            if names[i] in value_dict:
                if value_dict[names[i]] != "":
                    continue
                val = names[i + 1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                value_dict[names[i]] = val

        if not instrument_in_file[-1] == value_dict["INSTRUMENT"]:
            instrument_in_file.append(value_dict["INSTRUMENT"])
            instrument_row = table.add_row().cells
            instrument_row[0].text = value_dict["INSTRUMENT"]
            instrument_row[0].merge(instrument_row[-1])
            col_heads_row = table.add_row().cells
            row_count = 1
            for col_heads in enumerate(index_ticked):
                col_heads_row[col_heads[0]].text = col_heads[1]
        else:
            row_count += 1
        value_dict["Sr no"] = str(row_count)
        data_row = table.add_row().cells
        for cell_content in enumerate(list(value_dict.values())):
            if cell_content[0] == len(index_ticked):
                break
            data_row[cell_content[0]].text = cell_content[1] if cell_content[1] != '' else "---"
        comp_file_count += 1
        status_text.set(str(comp_file_count) + ' OUT OF ' + str(len(files)) + ' SELECTED')
        root.update_idletasks()
    wb_new.save(misc[1])
    misc[2] = 0
    misc[3].clear()
    status_text.set('INDEX SUCCESSFULLY GENERATED')


def import_rawdata_files(root, status_text):
    files = list(tkinter.filedialog.askopenfilenames())

    if len(files) == 0:
        status_text.set('NO FILES SELECTED')
        return None

    csv_heading = ['id', 'loc', 'accept', 'section', 'acc', 'lc', 'range', 'make', 'inst', 'serial',
                   's1', 's2', 's3', 's4', 's5', 's6', 's7', 'workno', 'oprange']
    csv_import_count = 0

    f = open(misc[4], "w+")
    f.close()

    files.sort()

    with (open(misc[4], 'w') as csv_file):
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(csv_heading)

        misc[2] = len(files)
        misc[3] = files
        for file in files:
            rd_dict = {'ID NO.': '', 'LOCATION': '', 'ACCEPTANCE CRITERIA': '', 'SECTION': '', 'ACCURACY': '',
                       'LEAST COUNT': '', 'RANGE': '', 'MAKE': '', 'INSTRUMENT': '', 'SERIAL No.': '', '1.': ' ',
                       '2.': ' ', '3.': ' ', '4.': ' ', '5.': ' ', '6.': ' ', '7.': ' ',
                       'Work Instruction No.': '', 'OPERATING RANGE': ''}
            if file.__contains__('index.docx') or file.__contains__(' RD.docx'):
                files.remove(file)
                continue
            names = []
            text_output = textract.process(file, input_encoding='ISO-8859-1')
            word_decoded_value = text_output.decode('UTF-8')
            if file[-1] == 'c':
                word_content = str(word_decoded_value)
                list_word = word_content.split('|')
                for data in list_word:
                    data = data.strip()
                    if data:
                        names.append(' '.join(data.split()))
            else:
                word_decoded_value = word_decoded_value.split('\n')
                for data in word_decoded_value:
                    data = data.strip()
                    if data:
                        names.append(' '.join(data.split()))

            for data in names:
                if data == "INSTRUMENT RANGE":
                    rd_dict["RANGE"] = names[names.index(data) + 1].replace('0C',
                                                                            '°C').replace('(F.S.',
                                                                                          '%F.S.').replace(
                        '(', '±')

                if data in rd_dict:
                    if data in ['1.', '2.', '3.', '4.', '5.', '6.', '7.']:
                        rd_dict[data] = data[0] + ' .'
                    else:
                        if rd_dict[data] == "":
                            rd_dict[data] = names[names.index(data) + 1].replace('0C',
                                                                                 '°C').replace('(F.S.',
                                                                                               '%F.S.')
                            if rd_dict[data].__contains__("(") and not rd_dict[data].__contains__(")"):
                                rd_dict[data] = (rd_dict[data]).replace('(', '±')

            for i in list(rd_dict.keys()):
                if rd_dict[i] == '' or rd_dict[i] == "SR. NO.":
                    rd_dict[i] = '---'
            csv_import_count += 1
            csv_data_final = (list(filter(lambda x: x, list(rd_dict.values()))))
            csv_writer.writerow(csv_data_final)
            status_text.set(str(csv_import_count) + ' OUT OF ' + str(len(files)) + ' imported')
            root.update_idletasks()
    status_text.set('FILES SELECTED')


def clear_csv(status_text):
    f = open(misc[4], "w+")
    f.close()
    misc[2] = 0
    misc[3].clear()
    status_text.set('SELECTION CLEARED')


def get_template_path(idno, instrumentname):
    templates = {
        'cod': 'word//cod.docx',
        'dhm': 'word//DHM.docx',
        'dmgd': 'word//DMGD.docx',
        'sld': 'word//SLD.docx',
        'tmf': 'word//TMF.docx',
        'pg': 'word//PG.docx'
    }

    idno = str(idno)
    instrumentname = str(instrumentname)

    if 'COD' in idno or 'ASD' in idno:
        return templates['cod']
    elif any(term in idno for term in ['DHM', 'DHD', 'RHTID']):
        return templates['dhm']
    elif 'DMGD' in idno:
        return templates['dmgd']
    elif 'SLD' in idno:
        return templates['sld']
    elif any(term in instrumentname for term in ['Timer', 'Watch', 'Clock', 'Hour', 'Time']):
        return templates['tmf']
    else:
        return templates['pg']


def make_word(n, file_name_rd, save_dir, context, idno, instrumentname):
    template_path = get_template_path(idno, instrumentname)
    tpl = DocxTemplate(template_path)
    tpl.render(context[n])
    tpl.save(f"{save_dir}/{file_name_rd} RD.docx")


def create_rawdata(root, status_text, files):
    if misc[2] == 0:
        status_text.set('NO FILES ARE SELECTED')
        return

    rd_count = 0
    df1 = pd.read_csv(misc[4], encoding='ISO-8859-1')
    context = df1.to_dict(orient='records')
    total_files = misc[2]
    save_dir = os.path.dirname(misc[3][0]) + "/Raw data"

    os.makedirs(save_dir, exist_ok=True)

    for i, row in df1.iterrows():
        file_save_name = row['id'].replace('/', '-')
        make_word(i, file_save_name, save_dir, context, row['id'], row['inst'])
        status_text.set(f'{rd_count} OF {total_files} RAW DATA CREATED')
        root.update_idletasks()
        rd_count += 1

    with open(misc[4], "w+"):
        pass
    files.clear()
    status_text.set('RAW DATA GENERATED')
    misc[2] = 0


def check(login_root, login_frame, name, password, file_list):
    # checking for input
    if not (name.get() == 'admin' and password.get() == 'heet'):
        misc[0] += 1
        inv_login(name, password, login_frame)
        return None

    login_root.destroy()
    # the main window with all the functioning
    root = Tk()
    root.title('Raw data Generator')
    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    # setting tkinter window size
    root.geometry("%dx%d" % (width, height))
    root.configure(bg='#35455D')
    # adding logo
    logo = PhotoImage(file=logo_path)
    root.iconphoto(False, logo)

    # creating tab
    the_tab = ttk.Notebook(root)
    the_tab.pack()

    # creating index frame
    index_frame = LabelFrame(the_tab, bg='#BFD1DF', relief=SUNKEN)
    index_frame.pack(fill='both', expand=1)

    # creating a raw data frame
    raw_data_frame = LabelFrame(the_tab, bg='#BFD1DF')
    raw_data_frame.pack(fill='both', expand=1)

    # adding the tabs
    the_tab.add(index_frame, text='Index')
    the_tab.add(raw_data_frame, text="Raw Data")

    head_frame = LabelFrame(index_frame, bg='#BFD1DF', pady=10, padx=10)

    body_frame = LabelFrame(index_frame, bg='#BFD1DF', pady=10, padx=10)

    # label as a heading in index
    lab_head = Label(head_frame, text='INSTOTECH Calibration LLP', padx=10, pady=10, font=('algerian', 30), bg='#BFD1DF', fg='#161B53')
    company_name = Label(index_frame, text=company, width=27, bd=2, padx=10, pady=10, bg='#FDC12A', font=13)

    frame_select = LabelFrame(body_frame, text='select the criteria', pady=10, padx=10, bg='#BFD1DF')

    # label showing the current status in index tab
    status_text = StringVar()
    status_text.set("WAITING FOR FILES")
    status_bar = Label(body_frame, textvariable=status_text, bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')

    # variables to store checkbox data
    var_accuracy = StringVar()
    var_least_count = StringVar()
    var_range = StringVar()
    var_accept = StringVar()
    var_section = StringVar()
    var_make = StringVar()

    # all the checkboxes in index tab
    section_but = Checkbutton(frame_select, text='SECTION', variable=var_section, width='10', onvalue='yes',
                              offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
    section_but.deselect()

    make_but = Checkbutton(frame_select, text='MAKE', variable=var_make, width='10', onvalue='yes', offvalue="no",
                           padx=5, pady=5, anchor=W, bg='#FDC12A')
    make_but.deselect()

    range_but = Checkbutton(frame_select, text='RANGE', variable=var_range, width='10', onvalue='yes', offvalue="no",
                            padx=5, pady=5, anchor=W, bg='#FDC12A')
    range_but.deselect()

    least_count_but = Checkbutton(frame_select, text='LEAST COUNT', variable=var_least_count, width='19', onvalue='yes',
                                  offvalue="no", bg='#FDC12A', padx=5, pady=5, anchor=W)
    least_count_but.deselect()

    accuracy_but = Checkbutton(frame_select, text='ACCURACY', variable=var_accuracy, width='19', onvalue='yes',
                               offvalue="no", bg='#FDC12A', padx=5, pady=5, anchor=W)
    accuracy_but.deselect()

    accept_but = Checkbutton(frame_select, text='ACCEPTANCE CRITERIA', width='19', variable=var_accept, onvalue='yes',
                             offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
    accept_but.deselect()

    excel_files_button = Button(body_frame, text='SEARCH FOR FILES',
                                command=lambda: import_files_index(root, status_text, misc),
                                padx=10, pady=10, bg='#FDC12A')
    # button to start generating index
    convert_button = Button(body_frame, text='START INDEX',
                            command=lambda: generate_index(root, status_text, misc), padx=10, pady=10,
                            bg='#FDC12A')
    # button ot save the ticks made in checkboxes
    show_but = Button(frame_select, text='SAVE SELECTION',
                      command=lambda: show_index_files(status_text, value_dict, index_ticked, var_section, var_make,
                                                       var_range, var_least_count, var_accuracy, var_accept, misc),
                      padx=10, pady=10, bg='#FDC12A')

    head_frame.pack()
    lab_head.grid(row=0, column=0, padx=10, pady=10)
    company_name.pack()

    body_frame.pack()
    excel_files_button.grid(row=3, column=0, padx=5, pady=5)

    frame_select.grid(row=3, column=1, padx=10, pady=10)
    section_but.grid(row=0, column=0, padx=5, pady=5)
    make_but.grid(row=1, column=0, padx=5, pady=5)
    range_but.grid(row=2, column=0, padx=5, pady=5)
    least_count_but.grid(row=0, column=2, padx=5, pady=5)
    accuracy_but.grid(row=1, column=2, padx=5, pady=5)
    accept_but.grid(row=2, column=2, padx=5, pady=5)
    show_but.grid(row=3, column=1, padx=5, pady=5)

    convert_button.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

    status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)

    head_rd_frame = LabelFrame(raw_data_frame, bg='#BFD1DF', pady=10, padx=10)

    lab_head_rd = Label(head_rd_frame, text='INSTOTECH Calibration LLP', padx=10, pady=10, font=('algerian', 30), bg='#BFD1DF',
                        fg='#161B53')
    company_name_rd = Label(raw_data_frame, text=company, width=27, bd=2, padx=10,
                            pady=10, bg='#FDC12A', font=13)

    body_rd_frame = LabelFrame(raw_data_frame, padx=10, pady=10, bg='#BFD1DF')

    status_text_ = StringVar()
    status_text_.set("WAITING FOR FILES")
    status_bar_rd = Label(body_rd_frame, textvariable=status_text_, width=25, bd=2, relief=SUNKEN, padx=10,
                          pady=10, bg='#FDC12A')
    raw_data_import_button = Button(body_rd_frame, text='SELECT FILES FOR RAW DATA', padx=10, pady=10, bg='#FDC12A',
                                    command=lambda: import_rawdata_files(root, status_text_))

    create_raw_data_button = Button(body_rd_frame, text='CREATE RAW DATA FILES',
                                    command=lambda: create_rawdata(root, status_text_, file_list), padx=10,
                                    pady=10, bg='#FDC12A')

    clear_button = Button(body_rd_frame, text='CLEAR SELECTED FILES', padx=10, pady=10, bg='#FDC12A',
                          command=lambda: clear_csv(status_text_))

    head_rd_frame.pack()
    lab_head_rd.grid(row=0, column=0, padx=10, pady=10)
    company_name_rd.pack()
    body_rd_frame.pack()
    status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
    raw_data_import_button.grid(row=0, column=0, padx=10, pady=10)
    create_raw_data_button.grid(row=0, column=1, padx=10, pady=10)
    clear_button.grid(row=1, column=1, padx=10, pady=10)

    root.mainloop()


login()
