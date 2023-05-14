import PySimpleGUI as sg
import mysql.connector

def add_agency():
    mydb = connect_to_db()

    sg.theme('Material2')
    sg.set_options(font=("Helvetica", 18))

    layout = [[sg.Text('Adding Administrator to an Attraction:')],
              [sg.Text("Enter Agency Name"),
               sg.InputText(key="agencyName")],
              [sg.Text("Enter Contact Number"),
               sg.InputText(key="contactNo")],
              [sg.Submit()], [sg.Exit()], [sg.Button("Clear")]]

    window = sg.Window('Travel Agency Registration', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Clear":
            window['agencyName'].update('')
            window['contactNo'].update('')

        if event == "Submit":
            try:
                agencyName = values.get("agencyName")
                contactNo = values.get("contactNo")

                regg_agency(mydb, agencyName, contactNo)
            except:
                sg.Popup('The data is incorrect. Please, refill the form')
                window['agencyName'].update('')
                window['contactNo'].update('')

                continue

            sg.Popup(
                f" {agencyName}({contactNo}) is successfully registered")

            break

    window.close()

    return values


def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="cityattractions"
    )
    return mydb


def regg_agency(mydb, agencyName, contactNo):
    mycursor = mydb.cursor()
    sql = "INSERT INTO travelagency (agencyName, contactNo) VALUES (%s, %s)"
    val = (agencyName, contactNo)
    mycursor.execute(sql, val)
    mydb.commit()


add_agency()
