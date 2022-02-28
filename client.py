import socket, os, json, datetime
from time import sleep


IP = '192.168.1.16' # server ip address
PORT = 4455
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

config_file = open('config.json')
config = json.load(config_file)
config_file.close()

todays_date = datetime.date.today()
yesterdays_date = str(todays_date - datetime.timedelta(days=1))
print(os.path.join(config["usb_drive_location"], yesterdays_date))

def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)

    # send dir name
    client.send(yesterdays_date.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    for filename in os.listdir(os.path.join(config["usb_drive_location"], yesterdays_date)):
        print(filename)
        """ Opening and reading the file data. """
        file = open(filename, "r")
        data = file.read()

        """ Sending the filename to the server. """
        client.send(filename.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")

        """ Sending the file data to the server. """
        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")

        """ Closing the file. """
        file.close()

    """ Closing the connection from the server. """
    client.close()


if __name__ == "__main__":
    main()