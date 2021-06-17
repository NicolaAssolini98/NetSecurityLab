import socket
import time

from Messaggi import *
from FunzioniCritto import *

A_ID = "A"
B_HOST = '127.0.0.1'  # Client B host
B_PORT = 65432
B_ID = "B"

int(time.time())
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    chose = input("\n1. Inizia chat con B\n0. esci\n-> ")
    if chose == "0":
        exit(0)

    """ inizio chat """
    g_a, a, p = get_public_key()
    s.connect((B_HOST, B_PORT))
    s.sendall(chat_requested(A_ID, B_ID, int(time.time()), g_a))
    print("Richiesta chat segreta inviata... ")
    data = s.recv(1024)
    d_list = read_message(data)
    g_b = int(d_list[4])
    key = pow(g_b, a, p)
    key_finger = get_fingerprint(key)

    if d_list[0] == "accept":
        """ controllo destinatario, data, correttezza chiave """
        if d_list[2] != A_ID or int(d_list[3]) < int(time.time()) - 60 or d_list[5] != key_finger:
            print(d_list[5] + " ==? " + key_finger)
            s.sendall("close".encode())
            s.close()
            print("Errore risposta")
            continue

        print("Chat segreta aperta, digita <close> per uscire")
        while True:
            payload = input("-> ")

            if payload == "<close>":
                msg_key = get_msg_key("close", key).encode()
                mess = key_finger.encode() + msg_key + encode_msg("close", msg_key, key)
                s.sendall(mess)
                s.close()
                break

            # TODO volendo si può fare il check sulla fingerprint
            msg_key = get_msg_key(payload, key).encode()
            mess = key_finger.encode() + msg_key + encode_msg(payload, msg_key, key)
            s.sendall(mess)
            enc_data = s.recv(1024)
            data = decode_msg(enc_data[48:], enc_data[16:48], key)

            if data.decode("UTF-8") == "close":
                s.close()
                print("Chat chiusa da B")
                break

            print('B: ', data.decode("UTF-8"))

    elif d_list[0] == "close":
        print("Chat rifiutata")

    else:
        print("Error")



