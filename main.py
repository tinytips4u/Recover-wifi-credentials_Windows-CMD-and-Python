import subprocess

curr_chcp = subprocess.getoutput('chcp').split(':')[1][1:]
print("The current code page is: ", curr_chcp)
cp_changed = False

try:
    try:
        profile = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])\
            .decode('utf-8').split('\r\n')
    except UnicodeDecodeError:
        new_chcp = subprocess.getoutput(["chcp","65001"]).split(':')[1][1:]
        print("The new code page is set to: ",new_chcp)
        cp_changed = True
        profile = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']) \
            .decode('utf-8').split('\r\n')

    if len(profile)==0:
        print("No SSID Name Found!")
    else:
        SSID_set = {line.split(':')[1][1:] for line in profile if 'All User Profile' in line}
        for ssid in SSID_set:
            ssid_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', ssid, 'key=clear'])\
                .decode('utf-8').split('\r\n')
            password = [line.split(':')[1][1:] for line in ssid_data if 'Key Content' in line]
            try:
                print(f"SSID: {ssid}, Password: {password[0]}")
            except IndexError:
                print(f"SSID: {ssid}, Password: Password was not saved")

except subprocess.CalledProcessError as e:
    print("Error:", e.output.decode('utf-8'))
finally:
    if cp_changed:
        chcp_set = subprocess.getoutput(["chcp", curr_chcp]).split(':')[1][1:]
        print("The code page is set back to: ",chcp_set)
        cp_changed = False
    input("Press any key to continue")