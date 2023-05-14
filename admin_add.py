import PySimpleGUI as sg
import mysql.connector

def register_administrator():
    mydb = connect_to_db()

    sg.theme('Material2')
    sg.set_options(font=("Helvetica", 18))

    layout = [[sg.Text('Adding Administrator to an Attraction:')],
              [sg.Text("Enter First Name"),
               sg.InputText(key="firstName")],
              [sg.Text("Enter Last Name"),
               sg.InputText(key="lastName")],
              [sg.Text("Enter Email", ),
               sg.InputText(key="adminEmail")],
              [sg.Text("Enter Contact Number", ),
               sg.InputText(key="contactNo")],
              [sg.Text("Enter Attraction City", ),
               sg.InputText(key="cityName")],
              [sg.Text("Enter Attraction Country", ),
               sg.InputText(key="country")],
              [sg.Text("Enter Attraction Name", ),
               sg.InputText(key="attractionName")],
              [sg.Submit()], [sg.Exit()], [sg.Button("Clear")]]

    window = sg.Window('Administrator Registration', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Clear":
            window['firstName'].update('')
            window['lastName'].update('')
            window['adminEmail'].update('')
            window['contactNo'].update('')
            window['cityName'].update('')
            window['country'].update('')
            window['attractionName'].update('')

        if event == "Submit":

            try:
                firstName = values.get("firstName")
                lastName = values.get("lastName")
                adminEmail = values.get("adminEmail")
                contactNo = values.get("contactNo")
                cityName = values.get("cityName")
                country = values.get("country")
                attractionName = values.get("attractionName")
                add_recipe(mydb, firstName, lastName, adminEmail, contactNo, cityName, country, attractionName)
            except:
                sg.Popup('The data is incorrect. Please, refill the form')
                window['firstName'].update('')
                window['lastName'].update('')
                window['adminEmail'].update('')
                window['contactNo'].update('')
                window['cityName'].update('')
                window['country'].update('')
                window['attractionName'].update('')
                continue

            sg.Popup(
                f" {firstName} {lastName} is successfully registered as {attractionName}({cityName}, {country}) administrator")

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


def add_recipe(mydb, firstName, lastName, adminEmail, contactNo, cityName, country, attractionName):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Administration (cityName, country, attractionName, firstName, las" \
                "tName, adminEmail, contactNo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (cityName, country, attractionName, firstName, lastName, adminEmail, contactNo)
    mycursor.execute(sql, val)
    mydb.commit()


register_administrator()