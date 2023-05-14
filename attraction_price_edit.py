import PySimpleGUI as sg
import mysql.connector

def edit_attraction_price():
    mydb = connect_to_db()

    sg.theme('Material2')
    sg.set_options(font=("Helvetica", 18))

    layout = [[sg.Text('Editing Attraction Entrance Fee:')],
              [sg.Text("Enter Attraction City", ),
               sg.InputText(key="cityName")],
              [sg.Text("Enter Attraction Country", ),
               sg.InputText(key="country")],
              [sg.Text("Enter Attraction Name", ),
               sg.InputText(key="attractionName")],
              [sg.Text("Enter new min price", ),
               sg.InputText(key="priceFrom")],
              [sg.Text("Enter new max price", ),
               sg.InputText(key="priceTo")],

              [sg.Submit()], [sg.Exit()], [sg.Button("Clear")]]

    window = sg.Window('Price Editor', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "Exit":
            break

        if event == "Clear":
            window['cityName'].update('')
            window['country'].update('')
            window['attractionName'].update('')
            window['priceFrom'].update('')
            window['priceTo'].update('')


        if event == "Submit":
            try:
                cityName = values.get("cityName")
                country = values.get("country")
                attractionName = values.get("attractionName")
                priceFrom = int(values.get('priceFrom'))
                priceTo = int(values.get('priceTo'))
                prevFrom, prevTo = get_prev_price(mydb, cityName, country, attractionName)
                edit_price(mydb, cityName, country, attractionName, priceFrom, priceTo)

                if priceTo<priceFrom:
                    raise Exception

            except:
                sg.Popup('The data is incorrect. Please, refill the form')
                window['cityName'].update('')
                window['country'].update('')
                window['attractionName'].update('')
                window['priceFrom'].update('')
                window['priceTo'].update('')
                continue

            sg.Popup(
                f" Entrance Fee is successfully changed from {prevFrom} & {prevTo} to {priceFrom} & {priceTo} for {attractionName}({cityName}, {country})")

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

def get_prev_price(mydb, city, count, attraction):
    mycursor = mydb.cursor()
    print("lolll")
    mycursor.execute(f"SELECT priceFrom, priceTo FROM Entrancefee WHERE attractionName = {attraction} cityName = {city} AND country = {count}")
    print("bang")
    result = mycursor.fetchall()
    prevFrom, prevTo = result[0][0], result[0][1]

    return prevFrom, prevTo

def edit_price(mydb, cityName, country, attractionName, priceFrom, priceTo):
    mycursor = mydb.cursor()
    sql = "UPDATE entrancefee SET priceFrom = %s, priceTo = %s "\
            "WHERE (cityName = %s AND country = %s AND attractionName = %s)"
    val = (priceFrom, priceTo, cityName, country, attractionName)
    mycursor.execute(sql, val)
    mydb.commit()


edit_attraction_price()