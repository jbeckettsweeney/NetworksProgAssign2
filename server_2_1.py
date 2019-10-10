import argparse
import rdt_2_1 as RDT
import time
import network_2_1 as net


def makePigLatin(word):
    m = len(word)
    vowels = "a", "e", "i", "o", "u", "y"
    if m < 3 or word == "the":
        return word
    else:
        for i in vowels:
            if word.find(i) < m and word.find(i) != -1:
                m = word.find(i)
        if m == 0:
            return word + "way"
        else:
            return word[m:] + word[:m] + "ay"


def piglatinize(message):
    essagemay = ""
    message = message.strip(".")
    for word in message.split(' '):
        essagemay += " " + makePigLatin(word)
    return essagemay.strip() + "."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pig Latin conversion server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    timeout = 5  # close connection if no new data within 5 seconds
    time_of_last_data = time.time()

    rdt = RDT.RDT('server', None, args.port)
    while (True):
        # try to receiver message before timeout
        msg_S = rdt.rdt_2_1_receive()
        if msg_S is None:
            if time_of_last_data + timeout < time.time():
                break
            else:
                continue
        time_of_last_data = time.time()
        print()
        print("received: ", msg_S)
        print()
        # convert and reply
        if msg_S[:3] == "NAK":
            rep_msg_S = "NAK"
            print()
            print("received corrupt packet")
            print()
            print("reply set to: ", rep_msg_S)
            print()
            rdt.rdt_2_1_send(rep_msg_S)
        else:
            rep_msg_S = piglatinize(msg_S)
            rep_msg_S = "ACK " + rep_msg_S
            print()
            print("no corrupt packet")
            print()
            print("reply set to: ", rep_msg_S)
            print()
            #print('Converted %s \nto \n%s\n' % (msg_S, rep_msg_S))
            rdt.rdt_2_1_send(rep_msg_S)

    rdt.disconnect()