import PySimpleGUI as sg
import subprocess
import os

def execute_gpupdate_command(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        return output, error, process.returncode
    except Exception as e:
        return b'', b'', -1

def main():
    sg.theme("default1")

    # Layout definitions
    layout_1 = [
        [
            sg.Text("Choose Option"),
            sg.Combo(["gpupdate", "gpupdate /force", "gpupdate /wait", "gpupdate /target", 
                      "gpupdate /logoff", "gpupdate /boot", "gpupdate /sync"],
                     key='COMBO')
        ]
    ]

    layout_2 = [[sg.Text('GP updated successfully')]]
    layout_3 = [[sg.Text('Reapplied all policy settings')]]
    layout_4 = [[sg.Text('Enter time (s)'), sg.InputText(key='TIME')]]
    layout_5 = [[sg.Radio("User", 'group1', key='USER'), sg.Radio("Computer", 'group1', key='COMPUTER')]]
    layout_6 = [[sg.Text('GP updated successfully & Logging off')]]
    layout_7 = [[sg.Text('GP updated successfully & Restarting computer')]]
    layout_8 = [[sg.Radio("Restart", 'group2', key='RESTART'), sg.Radio("Log Off", 'group2', key='LOGOFF')]]

    layout = [
        [
            sg.Column(layout_1, key='-COL1-'), sg.Column(layout_2, visible=False, key='-COL2-'),
            sg.Column(layout_3, visible=False, key='-COL3-'), sg.Column(layout_4, visible=False, key='-COL4-'),
            sg.Column(layout_5, visible=False, key='-COL5-'), sg.Column(layout_6, visible=False, key='-COL6-'),
            sg.Column(layout_7, visible=False, key='-COL7-'), sg.Column(layout_8, visible=False, key='-COL8-')
        ],
        [sg.Button('Ok'), sg.Button('Exit')]
    ]

    window = sg.Window("Group Policy Update", layout, size=(330, 100), resizable=True, element_justification='c')

    current_layout = 1

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Exit"):
            break

        if event == "Ok":
            selected_option = values['COMBO']
            if selected_option == 'gpupdate /wait':
                time_input = values["TIME"]
                command = f'gpupdate /wait:{time_input}' if time_input else None
            elif selected_option == 'gpupdate /target':
                if values['USER']:
                    command = 'gpupdate /target:user'
                elif values['COMPUTER']:
                    command = 'gpupdate /target:computer'
                else:
                    command = None
            elif selected_option == 'gpupdate /logoff':
                command = 'gpupdate'
            elif selected_option == 'gpupdate /boot':
                command = 'gpupdate'
            elif selected_option == 'gpupdate /sync':
                command = 'gpupdate'
            else:
                command = selected_option

            output, error, returncode = execute_gpupdate_command(command)
            decoded_output = output.decode('utf-8').replace('\r', '').replace('\n', '')

            window[f'-COL{current_layout}-'].update(visible=False)

            success_message = 'Updating policy...Computer Policy update has completed successfully.User Policy update has completed successfully.'
            if selected_option == 'gpupdate' and decoded_output == success_message:
                current_layout = 2
            elif selected_option == 'gpupdate /force' and decoded_output == success_message:
                current_layout = 3
            elif selected_option == 'gpupdate /wait':
                current_layout = 4
                if values["TIME"] != '' and decoded_output == success_message:
                    current_layout = 2
            elif selected_option == 'gpupdate /target':
                current_layout = 5
                if (values['USER'] or values['COMPUTER']):
                    current_layout = 2
            elif selected_option == 'gpupdate /logoff' and decoded_output == success_message:
                current_layout = 6
                os.system("shutdown -l")
            elif selected_option == 'gpupdate /boot' and decoded_output == success_message:
                current_layout = 7
                os.system("shutdown -r")
            elif selected_option == 'gpupdate /sync':
                current_layout = 8
                if values['RESTART'] and decoded_output == success_message:
                    os.system("shutdown -r")
                elif values['LOGOFF'] and decoded_output == success_message:
                    os.system("shutdown -l")

            window[f'-COL{current_layout}-'].update(visible=True)

    window.close()

if __name__ == "__main__":
    main()
