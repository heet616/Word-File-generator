# importing modules
import textract
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import csv
import pandas as pd
from docxtpl import DocxTemplate
import os
import docx
# creating login window
login_root = Tk()
login_root.title('LOGIN')
login_root.configure(bg='#BFD1DF')

logo_path = 'logo//instotech logo.png'
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

# empty list for all the files
file_name_index = []

file_saving_count = 0

# all the column headings
head = ('SR.NO', 'ID  NO. ', 'LOCATION ', 'SECTION', 'MAKE', 'RANGE', 'LEAST COUNT', 'ACCURACY ', 'ACCEPTANCE CRITERIA',
        'Calibration Date', 'Due Date')
# list specifying which headings to add
index_ticked = ['SR.NO', 'ID  NO. ', 'LOCATION ']
# list specifying all the data to added according to the headings
value_to_fill = ['row_count', 'id_no', 'location', 'cal_date', 'due_date']
# variable for the total columns
end_column_head = len(index_ticked)

# total files completed
file_stats = 0
# variable for counting the fail attempts while logging
error_count = 1
# variable to limit the uses of selection button to 1
head_select_count = 1

section_bool = False
least_bool = False
accuracy_bool = False
accept_bool = False
range_bool = False
make_bool = False
id_bool = False
location_bool = False
file_valid_bool = True
cal_bool = False
due_bool = False

status_bar = None
to_be_saved_in = ''
least_count = None
range_no = None
wb_new = None
acceptance_criteria = None
make_no = None
location = None
id_no = None
section = None
accuracy_value = None
csv_heading = None
instrument_val = ''
file_name_1 = []
word_import_count = 0

rd_file_select_count = 0
no_of_csv_head = 0
csv_file_name = 'Csv file//csv.csv'
word_template_path = "word//Calibration  Format for report MJ biopharm.docx"

file_list_xlsx = []
file_list_word_rd = []

file_label = ''


def isnumber(s):
    for i in range(len(s)):
        if not s[i].isdigit():

            return False

    return True


# main program
def check():
    # checking for input
    if name.get() == 'admin' and password.get() == 'heet':
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
        logo2 = PhotoImage(file=logo_path)
        root.iconphoto(False, logo2)

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

        head_frame = LabelFrame(index_frame, bg='#BFD1DF',  pady=10, padx=10)

        body_frame = LabelFrame(index_frame, bg='#BFD1DF',  pady=10, padx=10)

        # label as an heading in index
        lab_head = Label(head_frame, text='INSTOTECH', padx=10, pady=10, font=('algerian', 30), bg='#BFD1DF', fg='#161B53')
        company_name = Label(index_frame, text='MJ Biopharm', width=27, bd=2, padx=10, pady=10, bg='#FDC12A', font=13)

        frame_select = LabelFrame(body_frame, text='select the criteria', pady=10, padx=10, bg='#BFD1DF')

        # label showing the current status in index tab
        status_bar = Label(body_frame, text='WAITING FOR SELECTION', bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')

        # variables to store checkbox data
        var_accuracy = StringVar()
        var_least_count = StringVar()
        var_range = StringVar()
        var_accept = StringVar()
        var_section = StringVar()
        var_make = StringVar()

        # all the checkboxes in index tab
        section_but = Checkbutton(frame_select, text='SECTION', variable=var_section, width='10', onvalue='yes', offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
        section_but.deselect()

        make_but = Checkbutton(frame_select, text='MAKE', variable=var_make, width='10', onvalue='yes', offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
        make_but.deselect()

        range_but = Checkbutton(frame_select, text='RANGE', variable=var_range, width='10', onvalue='yes', offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
        range_but.deselect()

        least_count_but = Checkbutton(frame_select, text='LEAST COUNT', variable=var_least_count, width='19', onvalue='yes', offvalue="no", bg='#FDC12A', padx=5, pady=5, anchor=W)
        least_count_but.deselect()

        accuracy_but = Checkbutton(frame_select, text='ACCURACY', variable=var_accuracy, width='19', onvalue='yes', offvalue="no", bg='#FDC12A', padx=5, pady=5, anchor=W)
        accuracy_but.deselect()

        accept_but = Checkbutton(frame_select, text='ACCEPTANCE CRITERIA', width='19', variable=var_accept, onvalue='yes', offvalue="no", padx=5, pady=5, anchor=W, bg='#FDC12A')
        accept_but.deselect()

        # function to save the tick and add to the list
        def show_function_of_index():
            global end_column_head, value_to_fill
            global index_ticked
            global head_select_count
            global status_bar

            # loop to avoid repetition of headings due to more clicks
            if head_select_count == 1:
                index_lab = Label(root, text=(var_section.get(), var_make.get(), var_range.get(), var_least_count.get(), var_accuracy.get(), var_accept.get()), padx=10, pady=10)
                index_lab_value = str(index_lab.cget('text'))
                index_1 = index_lab_value.split(' ')
                index_ticked = ['SR.NO', 'ID  NO. ', 'LOCATION ']
                value_to_fill = ['row_count', 'id_no', 'location', 'cal_date', 'due_date']

                # checks with box is ticked
                if index_1[0] == 'yes':
                    index_ticked.append(head[3])
                    value_to_fill.append('section')
                if index_1[1] == 'yes':
                    index_ticked.append(head[4])
                    value_to_fill.append('make')
                if index_1[2] == 'yes':
                    index_ticked.append(head[5])
                    value_to_fill.append('range_no')
                if index_1[3] == 'yes':
                    index_ticked.append(head[6])
                    value_to_fill.append('least_count')
                if index_1[4] == 'yes':
                    index_ticked.append(head[7])
                    value_to_fill.append('accuracy_value')
                if index_1[5] == 'yes':
                    index_ticked.append(head[8])
                    value_to_fill.append('acceptance_criteria')
                    head_select_count += 1
                index_ticked.append('Calibration Date')
                index_ticked.append('Due Date')
                end_column_head = len(index_ticked)
                status_bar = Label(body_frame, text='Options selected', bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)
                root.update_idletasks()

        # function to import all the files to extract the data from
        def import_files_function_of_index():
            global file_name_index, to_be_saved_in, row_count, status_bar
            global file_xlsx, word_import_count

            root.filename = filedialog.askopenfilenames(initialdir="", title="Select the Files", filetypes=(("word files", "*.doc"), ("all files", "*.*")))
            label = Label(index_frame, text=root.filename)

            # removing excess things from the file paths
            fil = str(label.cget('text'))

            if len(fil) > 0:
                final_filename = fil.replace('{', '')
                final__file_name = final_filename.replace('} ', 'separate_here')
                final__file_name1 = final__file_name.replace('}', 'separate_here')
                final_file_name = final__file_name1.replace('/', '//')
                x = final_file_name.split('separate_here')

                file_name_index.clear()
                file_list_xlsx.clear()

                # appending all the file in previous list
                for file in x:
                    file_name_index.append(file)
                    word_import_count += 1

                file_name_index.sort()

                file_name_index.remove('')

                for file_xls in file_name_index:
                    file_list_xlsx.append(file_xls)

                    status_bar = Label(body_frame, text=str(word_import_count) + ' OUT OF ' + str(len(file_list_xlsx)) + 'SELECTED', bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                    status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)
                    root.update_idletasks()

                # again removing extras
                # variables for getting the directory of the files
                file_root = str(file_name_index[0])
                head_tail = os.path.split(file_root)
                # the file in which it is to saved in
                to_be_saved_in = str(head_tail[0]) + '//index.docx'

                status_bar = Label(body_frame, text="FILES SELECTED", bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)
                root.update_idletasks()
                file_name_index.clear()
            else:
                status_bar = Label(body_frame, text="NO FILES ARE SELECTED", bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)

            # function that actually does the main task
        def generate_index_function_of_index():
            global file_stats, least_count, range_no, accuracy_value, section, acceptance_criteria, make_no, cal_bool, cal_date, due_bool, due_date
            global end_column_head, instrument_val, row_count
            file_stats = 0

            # adding cal date and due date they are absent
            if len(index_ticked) == 3:
                index_ticked.append('Calibration Date')
                index_ticked.append('Due Date')
                end_column_head = len(index_ticked)
            comp_file_count = 0

            # loop that goes through all files and starts filling the excel sheet
            if len(file_list_xlsx) > 0:
                wb_new = docx.Document()
                table = wb_new.add_table(rows=1, cols=len(index_ticked))
                if '' in file_list_xlsx:
                    file_list_xlsx.pop(file_list_xlsx.index(''))
                row_count = 1
                instrument_in_file = ['']

                for file_count in file_list_xlsx:
                    global status_bar, least_bool, section_bool
                    global range_bool, accept_bool, accuracy_bool, make_bool, id_bool
                    global location_bool, id_no, location, file_saving_count, to_be_saved_in, file_valid_bool

                    file_stats += 1
                    file_valid_bool = True

                    main_list = []
                    word_encoded_value = textract.process(file_count, input_encoding='ISO-8859-1')
                    word_decoded_value = word_encoded_value.decode('UTF-8')
                    word_content_for_index = str(word_decoded_value)
                    list_word_for_index = word_content_for_index.split('|')
                    for data_for_index in list_word_for_index:
                        if not data_for_index == '|':
                            new_data_for_index = data_for_index.strip(' ')
                            if not new_data_for_index == '':
                                data_1_for_index = new_data_for_index.strip('\r\n')
                                if not data_1_for_index == '':
                                    main_list.append(data_1_for_index)

                    names = []

                    for val in main_list:

                        if val is not None:
                            names.append(val)

                    # appending the instrument to the list
                    # finding the indexes of the column headings
                    if 'INSTRUMENT ' in names:
                        instrument_1 = names.index('INSTRUMENT ')
                        instrument_ind = instrument_1 + 1
                        instrument_val = names[instrument_ind]
                    elif 'INSTRUMENT' in names:
                        instrument_1 = names.index('INSTRUMENT')
                        instrument_ind = instrument_1 + 1
                        instrument_val = names[instrument_ind]
                    if 'Cal.  Date ' in names:
                        cal = names.index('Cal.  Date ')
                        cal_1 = cal + 1
                        cal_date = names[cal_1]
                        cal_bool = True
                    elif 'Cal.  Date' in names:
                        cal = names.index('Cal.  Date')
                        cal_1 = cal + 1
                        cal_date = names[cal_1]
                        cal_bool = True
                    elif 'Cal. Date ' in names:
                        cal = names.index('Cal. Date ')
                        cal_1 = cal + 1
                        cal_date = names[cal_1]
                        cal_bool = True
                    elif 'Cal. Date' in names:
                        cal = names.index('Cal. Date')
                        cal_1 = cal + 1
                        cal_date = names[cal_1]
                        cal_bool = True
                    if 'Due  Date' in names:
                        due = names.index('Due  Date')
                        due_1 = due + 1
                        due_date = names[due_1]
                        due_bool = True
                    elif 'Due  Date ' in names:
                        due = names.index('Due  Date ')
                        due_1 = due + 1
                        due_date = names[due_1]
                        due_bool = True
                    elif 'Due Date ' in names:
                        due = names.index('Due Date ')
                        due_1 = due + 1
                        due_date = names[due_1]
                        due_bool = True
                    elif 'Due Date' in names:
                        due = names.index('Due Date')
                        due_1 = due + 1
                        due_date = names[due_1]
                        due_bool = True
                    if 'ID  NO. ' in names:
                        id_ = names.index('ID  NO. ')
                        id_1 = id_ + 1
                        id_no = names[id_1]
                        id_bool = True
                    elif 'ID  NO.' in names:
                        id_ = names.index('ID  NO.')
                        id_1 = id_ + 1
                        id_no = names[id_1]
                        id_bool = True
                    elif 'ID NO.' in names:
                        id_ = names.index('ID NO.')
                        id_1 = id_ + 1
                        id_no = names[id_1]
                        id_bool = True
                    elif 'ID NO. ' in names:
                        id_ = names.index('ID NO. ')
                        id_1 = id_ + 1
                        id_no = names[id_1]
                        id_bool = True
                    if 'LOCATION ' in names:
                        loc = names.index('LOCATION ')
                        loc_1 = loc + 1
                        location = names[loc_1]
                        location_bool = True
                    elif 'LOCATION' in names:
                        loc = names.index('LOCATION')
                        loc_1 = loc + 1
                        location = names[loc_1]
                        location_bool = True
                    if 'SECTION' in names:
                        sect = names.index('SECTION')
                        sect_1 = sect + 1
                        section = names[sect_1]
                        section_bool = True
                    if 'MAKE' in names:
                        make_index = names.index('MAKE')
                        make_index_1 = make_index + 1
                        make_no = names[make_index_1]
                        make_bool = True
                    elif 'MAKE ' in names:
                        make_index = names.index('MAKE ')
                        make_index_1 = make_index + 1
                        make_no = names[make_index_1]
                        make_bool = True
                    if 'RANGE' in names:
                        range_index = names.index('RANGE')
                        range_index_1 = range_index + 1
                        range_no = names[range_index_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        range_bool = True
                    elif 'RANGE ' in names:
                        range_index = names.index('RANGE ')
                        range_index_1 = range_index + 1
                        range_no = names[range_index_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        range_bool = True
                    if 'LEAST COUNT' in names:
                        least_count_index = names.index('LEAST COUNT')
                        least_count_index_1 = least_count_index + 1
                        least_count = names[least_count_index_1]
                        least_bool = True
                    elif 'LEAST COUNT ' in names:
                        least_count_index = names.index('LEAST COUNT ')
                        least_count_index_1 = least_count_index + 1
                        least_count = names[least_count_index_1]
                        least_bool = True
                    if 'ACCURACY ' in names:
                        accuracy_index = names.index('ACCURACY ')
                        accuracy_index_1 = accuracy_index + 1
                        accuracy_value = names[accuracy_index_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        accuracy_bool = True
                    elif 'ACCURACY' in names:
                        accuracy_index = names.index('ACCURACY')
                        accuracy_index_1 = accuracy_index + 1
                        accuracy_value = names[accuracy_index_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        accuracy_bool = True
                    if 'ACCEPTANCE CRITERIA' in names:
                        accept_criteria = names.index('ACCEPTANCE CRITERIA')
                        accept_criteria_1 = accept_criteria + 1
                        acceptance_criteria = names[accept_criteria_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        accept_bool = True
                    elif 'ACCEPTANCE CRITERIA  ' in names:
                        accept_criteria = names.index('ACCEPTANCE CRITERIA  ')
                        accept_criteria_1 = accept_criteria + 1
                        acceptance_criteria = names[accept_criteria_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        accept_bool = True
                    elif 'ACCEPTANCE CRITERIA ' in names:
                        accept_criteria = names.index('ACCEPTANCE CRITERIA  ')
                        accept_criteria_1 = accept_criteria + 1
                        acceptance_criteria = names[accept_criteria_1].replace('0C', '°C').replace('(F.S.', '%F.S.').replace('(', '±')
                        accept_bool = True

                    # list to be appended
                    headers = [row_count]

                    # checking which data is to be added
                    # and if it exists then its fine else it will be a "-"
                    if 'id_no' in value_to_fill:
                        if id_bool:
                            headers.append(id_no)
                        else:
                            id_no = '---'
                            headers.append(id_no)
                    if 'location' in value_to_fill:
                        if location_bool:
                            headers.append(location)
                        else:
                            location = '---'
                            headers.append(location)
                    if 'section' in value_to_fill:
                        if accuracy_bool:
                            headers.append(section)
                        else:
                            section = '---'
                            headers.append(section)
                    if 'make' in value_to_fill:
                        if make_bool:
                            headers.append(make_no)
                        else:
                            make_no = '---'
                            headers.append(make_no)
                    if 'range_no' in value_to_fill:
                        if range_bool:
                            headers.append(range_no)
                        else:
                            range_no = '---'
                            headers.append(range_no)
                    if 'least_count' in value_to_fill:
                        if least_bool:
                            headers.append(least_count)
                        else:
                            least_count = '---'
                            headers.append(least_count)
                    if 'accuracy_value' in value_to_fill:
                        if accuracy_bool:
                            headers.append(accuracy_value)
                        else:
                            accuracy_value = '---'
                            headers.append(accuracy_value)
                    if 'acceptance_criteria' in value_to_fill:
                        if accept_bool:
                            headers.append(acceptance_criteria)
                        else:
                            acceptance_criteria = '---'
                            headers.append(acceptance_criteria)
                    if 'cal_date' in value_to_fill:
                        if cal_bool:
                            headers.append(cal_date)
                        else:
                            cal_date = '---'
                            headers.append(cal_date)
                    if 'due_date' in value_to_fill:
                        if due_bool:
                            headers.append(due_date)
                        else:
                            due_date = '---'
                            headers.append(due_date)

                    if not instrument_in_file[-1] == instrument_val:
                        instrument_in_file.append(instrument_val)
                        instrument_row = table.add_row().cells
                        instrument_row[0].text = instrument_val
                        instrument_row[0].merge(instrument_row[-1])
                        col_heads_row = table.add_row().cells
                        row_count = 1
                        headers[0] = row_count
                        for col_heads in enumerate(index_ticked):
                            col_heads_row[col_heads[0]].text = col_heads[1]
                    else:
                        row_count += 1
                        headers[0] = row_count
                    data_row = table.add_row().cells
                    for cell_content in enumerate(headers):
                        cell_contents = (cell_content[0], str(cell_content[1]))
                        data_row[cell_contents[0]].text = cell_contents[1]
                    wb_new.save(to_be_saved_in)
                    # row_count += 1
                    comp_file_count += 1
                    status_bar = Label(body_frame, text=str(comp_file_count) + ' OUT OF ' + str(len(file_list_xlsx)) + ' SELECTED', bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                    status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)
                    root.update_idletasks()
                status_bar = Label(body_frame, text='INDEX SUCCESSFULLY GENERATED', bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)
                root.update_idletasks()
            else:
                status_bar = Label(body_frame, text="NO FILES SELECTED", bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                status_bar.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=10, pady=10)

        # button to search for files
        excel_files_button = Button(body_frame, text='SEARCH FOR FILES', command=import_files_function_of_index, padx=10, pady=10, bg='#FDC12A')
        # button to start generating index
        convert_button = Button(body_frame, text='START INDEX', command=generate_index_function_of_index, padx=10, pady=10, bg='#FDC12A')
        # button ot save the ticks made in checkboxes
        show_but = Button(frame_select, text='SAVE SELECTION', command=lambda: show_function_of_index(), padx=10, pady=10, bg='#FDC12A')
        # placing the status bar

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

        lab_head_rd = Label(head_rd_frame, text='INSTOTECH', padx=10, pady=10, font=('algerian', 30), bg='#BFD1DF',
                            fg='#161B53')
        company_name_rd = Label(raw_data_frame, text='MJ Biopharm', width=27, bd=2, padx=10,
                                pady=10, bg='#FDC12A', font=13)

        body_rd_frame = LabelFrame(raw_data_frame, padx=10, pady=10, bg='#BFD1DF')

        status_bar_rd = Label(body_rd_frame, text='WAITING TO IMPORT FILES', width=25, bd=2, relief=SUNKEN, padx=10,
                              pady=10, bg='#FDC12A')

        def raw_data_import_files():
            global rd_file_select_count, no_of_csv_head, csv_heading, csv_file_name, status_bar_rd, base_dir, file_label
            csv_import_count = 0

            # global csv_heading
            root.filename_raw_data = filedialog.askopenfilenames(initialdir="", title="Select the Files", filetypes=(("word files", "*.doc"), ("all files", "*.*")))
            label = Label(raw_data_frame, text=root.filename_raw_data)

            file_label = str(label.cget('text'))
            if len(file_label) > 0:
                f = open(csv_file_name, "w+")
                f.close()
                final_filename_1 = file_label.replace('{', '')
                final__file_name_1 = final_filename_1.replace('} ', 'separate_here')
                final__file_name1_1 = final__file_name_1.replace('}', 'separate_here')
                final_file_name_1 = final__file_name1_1.replace('/', '//')
                y = final_file_name_1.split('separate_here')

                file_name_1.clear()
                file_list_word_rd.clear()

                # appending all the file in previous list
                for file_1 in y:
                    file_name_1.append(file_1)

                file_name_1.sort()

                # again removing extras
                if '' in file_name_1:
                    file_name_1.remove('')

                base_file = str(file_name_1[0])
                base_dir_1 = os.path.split(base_file)
                base_dir = base_dir_1[0]

                csv_heading = ['idno', 'location', 'acceptancecriteria', 'sectionname', 'accuracy', 'leastcount',
                               'rangevalue', 'makename', 'instrumentname', 'serialno', 'sr1', 'sr2', 'sr3', 'sr4', 'sr5',
                               'sr6', 'sr7', 'calicerticode', 'temp', 'relhum', 'workno']
                csv_data = [[]]

                sr1 = ' '
                sr2 = ' '
                sr3 = ' '
                sr4 = ' '
                sr5 = ' '
                sr6 = ' '
                sr7 = ' '
                cal_year = ' '
                temp_val = ' '
                rel_hum = ' '
                work_no = ' '

                for file_1 in file_name_1:
                    main_list_1 = []
                    text_output = textract.process(file_1, input_encoding='ISO-8859-1')
                    word_content = text_output.decode('UTF-8')
                    word_content = str(word_content)
                    list_word = word_content.split('|')
                    for data in list_word:
                        if not data == '|':
                            new_data = data.strip(' ')
                            if not new_data == '':
                                data_1 = new_data.strip('\r\n')
                                if not data_1 == '':
                                    main_list_1.append(data_1)

                    names_1 = []

                    for val_1 in main_list_1:

                        if val_1 is not None:
                            names_1.append(val_1)

                    if 'ID  NO. ' in names_1:
                        id_1 = names_1.index('ID  NO. ')
                        id_ind = id_1 + 1
                        id_no_1_val = names_1[id_ind]
                    elif 'ID  NO.' in names_1:
                        id_1 = names_1.index('ID  NO.')
                        id_ind = id_1 + 1
                        id_no_1_val = names_1[id_ind]
                    else:
                        id_no_1_val = '---'
                    if 'LOCATION ' in names_1:
                        loc_1 = names_1.index('LOCATION ')
                        loc_ind = loc_1 + 1
                        location_1_val = names_1[loc_ind]
                    elif 'LOCATION' in names_1:
                        loc_1 = names_1.index('LOCATION')
                        loc_ind = loc_1 + 1
                        location_1_val = names_1[loc_ind]
                    else:
                        location_1_val = '---'
                    if 'INSTRUMENT ' in names_1:
                        instrument_1 = names_1.index('INSTRUMENT ')
                        instrument_ind = instrument_1 + 1
                        instrument_val_1 = names_1[instrument_ind]
                    elif 'INSTRUMENT' in names_1:
                        instrument_1 = names_1.index('INSTRUMENT')
                        instrument_ind = instrument_1 + 1
                        instrument_val_1 = names_1[instrument_ind]
                    else:
                        instrument_val_1 = '---'
                    if 'MAKE ' in names_1:
                        make_1 = names_1.index('MAKE ')
                        make_ind = make_1 + 1
                        make_val = names_1[make_ind]
                    elif 'MAKE' in names_1:
                        make_1 = names_1.index('MAKE')
                        make_ind = make_1 + 1
                        make_val = names_1[make_ind]
                    else:
                        make_val = '---'
                    if 'RANGE ' in names_1:
                        range_1 = names_1.index('RANGE ')
                        range_ind = range_1 + 1
                        range_val_1 = names_1[range_ind]
                        range_val_2 = range_val_1.replace('0C', '°C')
                        range_val_3 = range_val_2.replace('(F.S.', '%F.S.')
                        range_val = range_val_3.replace('(', '±')
                    elif 'RANGE' in names_1:
                        range_1 = names_1.index('RANGE')
                        range_ind = range_1 + 1
                        range_val_1 = names_1[range_ind]
                        range_val_2 = range_val_1.replace('0C', '°C')
                        range_val_3 = range_val_2.replace('(F.S.', '%F.S.')
                        range_val = range_val_3.replace('(', '±')
                    else:
                        range_val = '---'
                    if 'LEAST COUNT ' in names_1:
                        least_count_1 = names_1.index('LEAST COUNT ')
                        least_count_ind = least_count_1 + 1
                        least_count_val_1 = names_1[least_count_ind]
                        least_count_val_2 = least_count_val_1.replace('0C', '°C')
                        least_count_val_3 = least_count_val_2.replace('(F.S.', '%F.S.')
                        least_count_val = least_count_val_3.replace('(', '±')
                    elif 'LEAST COUNT' in names_1:
                        least_count_1 = names_1.index('LEAST COUNT')
                        least_count_ind = least_count_1 + 1
                        least_count_val_1 = names_1[least_count_ind]
                        least_count_val_2 = least_count_val_1.replace('0C', '°C')
                        least_count_val_3 = least_count_val_2.replace('(F.S.', '%F.')
                        least_count_val = least_count_val_3.replace('(', '±')
                    else:
                        least_count_val = '---'
                    if 'ACCURACY ' in names_1:
                        accuracy_1 = names_1.index('ACCURACY ')
                        accuracy_ind = accuracy_1 + 1
                        accuracy_val_1 = names_1[accuracy_ind]
                        accuracy_val_2 = accuracy_val_1.replace('0C', '°C')
                        accuracy_val_3 = accuracy_val_2.replace('(F.S', '%F.S')
                        accuracy_val = accuracy_val_3.replace('(', '±')

                    elif 'ACCURACY' in names_1:
                        accuracy_1 = names_1.index('ACCURACY')
                        accuracy_ind = accuracy_1 + 1
                        accuracy_val_1 = names_1[accuracy_ind]
                        accuracy_val_2 = accuracy_val_1.replace('0C', '°C')
                        accuracy_val_3 = accuracy_val_2.replace('(F.S', '%F.S')
                        accuracy_val = accuracy_val_3.replace('(', '±')
                    else:
                        accuracy_val = '---'
                    if 'SECTION ' in names_1:
                        section_1 = names_1.index('SECTION ')
                        section_ind = section_1 + 1
                        section_val = names_1[section_ind]
                    elif 'SECTION' in names_1:
                        section_1 = names_1.index('SECTION')
                        section_ind = section_1 + 1
                        section_val = names_1[section_ind]
                    else:
                        section_val = '---'
                    if 'ACCEPTANCE CRITERIA  ' in names_1:
                        accept_1 = names_1.index('ACCEPTANCE CRITERIA  ')
                        accept_ind = accept_1 + 1
                        accept_1_val_1 = names_1[accept_ind]
                        accept_1_val_2 = accept_1_val_1.replace('0C', '°C')
                        accept_1_val_3 = accept_1_val_2.replace('(F.S', '%F.S')
                        accept_1_val = accept_1_val_3.replace('(', '±')
                    elif 'ACCEPTANCE CRITERIA ' in names_1:
                        accept_1 = names_1.index('ACCEPTANCE CRITERIA ')
                        accept_ind = accept_1 + 1
                        accept_1_val_1 = names_1[accept_ind]
                        accept_1_val_2 = accept_1_val_1.replace('0C', '°C')
                        accept_1_val_3 = accept_1_val_2.replace('(F.S', '%F.S')
                        accept_1_val = accept_1_val_3.replace('(', '±')
                    elif 'ACCEPTANCE CRITERIA' in names_1:
                        accept_1 = names_1.index('ACCEPTANCE CRITERIA')
                        accept_ind = accept_1 + 1
                        accept_1_val_1 = names_1[accept_ind]
                        accept_1_val_2 = accept_1_val_1.replace('0C', '°C')
                        accept_1_val_3 = accept_1_val_2.replace('(F.S', '%F.S')
                        accept_1_val = accept_1_val_3.replace('(', '±')
                    else:
                        accept_1_val = '---'
                    if 'SERIAL  No.  ' in names_1:
                        serial_1 = names_1.index('SERIAL  No. ')
                        serial_ind = serial_1 + 1
                        serial_no = names_1[serial_ind]
                    elif 'SERIAL  No.' in names_1:
                        serial_1 = names_1.index('SERIAL  No.')
                        serial_ind = serial_1 + 1
                        serial_no = names_1[serial_ind]
                    elif 'SERIAL No. ' in names_1:
                        serial_1 = names_1.index('SERIAL No. ')
                        serial_ind = serial_1 + 1
                        serial_no = names_1[serial_ind]
                    elif 'SERIAL No.' in names_1:
                        serial_1 = names_1.index('SERIAL No.')
                        serial_ind = serial_1 + 1
                        serial_no = names_1[serial_ind]
                    else:
                        serial_no = '---'
                    for codes in names_1:
                        if codes.__contains__('CALIBRATION  CERTIFICATE  NO.'):
                            og_codes = codes.split(':')
                            og_code = og_codes[1].split('/')
                            year, id_code = og_code[1], og_code[2]
                            year_part = year[0]
                            year_no = year.strip(year_part)
                            if year_part == 'F':
                                year_part = 'S'
                                cal_year = year_part + str(year_no) + '/' + str(id_code)
                            else:
                                year_part = 'F'
                                year_no = int(year_no) + 1
                                cal_year = year_part + str(year_no) + '/' + str(id_code)
                        if codes.__contains__('Temperature :'):
                            new_code_temp = codes.split(':')
                            temp_val_1 = new_code_temp[1]
                            temp_val = temp_val_1.replace('0C', '°C').replace('(', '±')
                        if codes.__contains__('Relative Humidity :'):
                            new_code_hum = codes.split(':')
                            rel_hum = new_code_hum[1].replace('0C', '°C').replace('(', '%')
                    if 'Work Instruction No.' in names_1:
                        work = names_1.index('Work Instruction No.')
                        work_1 = work + 1
                        work_no = names_1[work_1]
                    elif 'Work Instruction No' in names_1:
                        work = names_1.index('Work Instruction No')
                        work_1 = work + 1
                        work_no = names_1[work_1]

                    if '1.' in names_1:
                        sr1 = "1 ."
                        if '2.' in names_1:
                            sr2 = "2 ."
                            if '3.' in names_1:
                                sr3 = "3 ."
                                if '4.' in names_1:
                                    sr4 = "4 ."
                                    if '5.' in names_1:
                                        sr5 = "5 ."
                                        if '6.' in names_1:
                                            sr6 = "6 ."
                                            if '7.' in names_1:
                                                sr7 = "7 ."

                    csv_content = [id_no_1_val, location_1_val, accept_1_val, section_val, accuracy_val,
                                   least_count_val, range_val, make_val, instrument_val_1, serial_no, sr1,
                                   sr2, sr3, sr4, sr5, sr6, sr7, cal_year, temp_val, rel_hum, work_no]

                    csv_import_count += 1
                    csv_data.append(csv_content)
                    status_bar_rd = Label(body_rd_frame,
                                          text=str(csv_import_count) + ' OUT OF ' + str(len(file_name_1)) + ' imported',
                                          width=25, bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                    status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                    root.update_idletasks()
                csv_data_final = (list(filter(lambda x: x, csv_data)))
                with open(csv_file_name, 'w') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(csv_heading)
                    csv_writer.writerows(csv_data_final)

                rd_file_select_count += 1
                status_bar_rd = Label(body_rd_frame, text='FILES SELECTED', width=25, bd=2, relief=SUNKEN, padx=10,
                                      pady=10, bg='#FDC12A')
                status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                root.update_idletasks()
            else:
                status_bar_rd = Label(body_rd_frame, text='NO FILES SELECTED', width=25, bd=2, relief=SUNKEN, padx=10,
                                      pady=10, bg='#FDC12A')
                status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                root.update_idletasks()

        def create_raw_data():
            global file_label, rd_file_select_count, status_bar_rd, no_of_csv_head
            if len(file_name_1) > 0:
                rd_files_convert_count = 0

                save_dir = (base_dir + "//Raw Data")

                if not os.path.exists(save_dir):
                    os.makedirs(save_dir, exist_ok=True)

                def make_word(n, file_name_rd):
                    tpl = DocxTemplate(word_template_path)  # In same directory
                    df1 = pd.read_csv(csv_file_name, encoding='ISO-8859-1')
                    df_to_doct = df1.to_dict()  # dataframe -> dict for the template render
                    x = df1.to_dict(orient='records')
                    context = x
                    tpl.render(context[n])
                    tpl.save("%s.docx" % (save_dir + '//' + file_name_rd + ' RD'))
                    status_bar_rd = Label(body_rd_frame, text=str(rd_files_convert_count) + ' OF ' + str(len(file_name_1)) + ' RAW DATA CREATED', width=25, bd=2, relief=SUNKEN, padx=10, pady=10, bg='#FDC12A')
                    status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                    root.update_idletasks()

                df2 = len(pd.read_csv(csv_file_name, encoding='ISO-8859-1'))

                for i in range(0, df2):
                    df = pd.read_csv(csv_file_name, encoding='ISO-8859-1')
                    columns_data = df.loc[:, 'idno']
                    file_save_name = columns_data[i]
                    file_save_name_1 = file_save_name.replace('/', '-')
                    make_word(i, file_save_name_1)
                    rd_files_convert_count += 1

                f = open(csv_file_name, "w+")
                f.close()
                file_name_1.clear()
                rd_file_select_count = 0
                no_of_csv_head = 0
                file_label = ''

                status_bar_rd = Label(body_rd_frame, text='RAW DATA GENERATED', width=25, bd=2, relief=SUNKEN, padx=10,
                                      pady=10, bg='#FDC12A')
                status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                root.update_idletasks()

            else:
                status_bar_rd = Label(body_rd_frame, text='NO FILES ARE SELECTED', width=25, bd=2, relief=SUNKEN,
                                      padx=10, pady=10, bg='#FDC12A')
                status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
                root.update_idletasks()

        def clear_csv():
            global file_label, rd_file_select_count, no_of_csv_head
            f = open(csv_file_name, "w+")
            f.close()
            file_name_1.clear()
            file_label = ''
            status_bar_rd = Label(body_rd_frame, text='SELECTION CLEARED', width=25, bd=2, relief=SUNKEN, padx=10,
                                  pady=10, bg='#FDC12A')
            status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
            root.update_idletasks()
            rd_file_select_count = 0
            no_of_csv_head = 0

        raw_data_import_button = Button(body_rd_frame, text='SELECT FILES FOR RAW DATA', padx=10, pady=10, bg='#FDC12A',
                                        command=raw_data_import_files)

        create_raw_data_button = Button(body_rd_frame, text='CREATE RAW DATA FILES', command=create_raw_data, padx=10,
                                        pady=10, bg='#FDC12A')

        clear_button = Button(body_rd_frame, text='CLEAR SELECTED FILES', padx=10, pady=10, bg='#FDC12A',
                              command=clear_csv)

        head_rd_frame.pack()
        lab_head_rd.grid(row=0, column=0, padx=10, pady=10)
        company_name_rd.pack()
        body_rd_frame.pack()
        status_bar_rd.grid(row=0, column=2, padx=10, pady=10)
        raw_data_import_button.grid(row=0, column=0, padx=10, pady=10)
        create_raw_data_button.grid(row=0, column=1, padx=10, pady=10)
        clear_button.grid(row=1, column=1, padx=10, pady=10)

        root.mainloop()

    # if password or username is wrong
    else:
        global error_count
        name.delete(0, END)
        password.delete(0, END)
        # loop to prevent many no of labels saying invalid username or id
        if error_count == 1:
            label_error = Label(login_frame, text='Invalid username or Password', padx=10, pady=10, fg='red')
            label_error.grid(row=3, column=0)
            error_count += 1


# button to start check command
check_button = Button(login_frame, text='ENTER', command=check)
check_button.grid(row=4, column=1)

cancel_button = Button(login_frame, text='CANCEL', command=login_frame.quit)
cancel_button.grid(row=4, column=2)
login_root.mainloop()
