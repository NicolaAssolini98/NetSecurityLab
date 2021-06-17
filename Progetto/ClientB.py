import socket
import time

from Messaggi import *
from FunzioniCritto import *

A_ID = "A"
B_HOST = '127.0.0.1'
B_PORT = 65432
B_ID = "B"



while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((B_HOST, B_PORT))
    print("\n\nConnesione aperta")
    s.listen()
    conn, addr = s.accept()
    print('\nConnected by', addr)
    data = conn.recv(1024)
    d_list = read_message(data)

    """ controllo che il messaggio sia rivolto a me e che non sia troppo vecchio """
    if d_list[2] != B_ID or int(d_list[3]) < int(time.time()) - 60:
        conn.sendall("close".encode())
        conn.close()
        print("Richiesta non valida")
        continue
    g_a = int(d_list[4])
    chose = input("Iniziare chat segreta con " + d_list[1] + "\n(y/n): ")

    if chose == "y":
        g_b, b, p = get_public_key()
        key = pow(g_a, b, p)
        key_finger = get_fingerprint(key)
        conn.sendall(chat_accept(B_ID, A_ID, int(time.time()), g_b, key_finger))
        print("Chat segreta aperta, digita <close> per uscire")
        while True:
            enc_data = conn.recv(1024)
            data = decode_msg(enc_data[48:], enc_data[16:48], key)

            if bytes.decode(data) == "close":
                s.close()
                print("Chat chiusa da A")
                break

            print('A: ', data.decode("UTF-8"))
            payload = input("-> ")

            if payload == "<close>":
                msg_key = get_msg_key("close", key).encode()
                mess = key_finger.encode() + msg_key + encode_msg("close", msg_key, key)
                conn.sendall(mess)
                conn.close()
                print("Chat chiusa")
                break

            msg_key = get_msg_key(payload, key).encode()
            mess = key_finger.encode() + msg_key + encode_msg(payload, msg_key, key)
            conn.sendall(mess)

    else:
        conn.sendall("close".encode("UTF-8"))

