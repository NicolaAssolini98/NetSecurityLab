def chat_requested(user_id, part_id, date, g_a):
    """
    flags	#	Flags, see TL conditional fields
    folder_id	flags.0?int	Peer folder ID, for more info click here
    id              Chat ID                         TODO
    access_hash	    Check sum depending on user ID  TODO
    date	    	Chat creation date
    admin_id		Chat creator ID
    participant_id	ID of second chat participant
    g_a	bytes	    A = g ^ a mod p
    """
    mess = "start\n" + \
           str(user_id) + "\n" \
           + str(part_id) + "\n" \
           + str(date) + "\n" + \
           str(g_a)

    return mess.encode("UTF-8")


def read_message(message):
    return message.decode("UTF-8").split("\n")


def chat_accept(user_id, part_id, date, g_b, k_finger):
    """
    id	                Chat ID  TODO
    access_hash	        Check sum dependant on the user ID
    date		        Date chat was created
    admin_id		    Chat creator ID
    participant_id	    ID of the second chat participant
    g_a_or_b		    B = g ^ b mod p
    key_fingerprint	    64-bit fingerprint of received key
    """
    mess = "accept\n" + \
           str(user_id) + "\n" \
           + str(part_id) + "\n" \
           + str(date) + "\n" \
           + str(g_b) + "\n" \
           + str(k_finger)

    return mess.encode("UTF-8")



