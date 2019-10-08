import argparse
import rdt_3_0 as RDT
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quotation client talking to a Pig Latin server.')
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    msg_L = [
        'The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense. -- Edsgar Dijkstra',
        'C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it blows away your whole leg. -- Bjarne Stroustrup',
        'A mathematician is a device for turning coffee into theorems. -- Paul Erdos',
        'Grove giveth and Gates taketh away. -- Bob Metcalfe (inventor of Ethernet) on the trend of hardware speedups not being able to keep up with software demands',
        'Wise men make proverbs, but fools repeat them. -- Samuel Palmer (1805-80)']

    timeout = 2  # send the next message if no response
    time_of_last_data = time.time()

    rdt = RDT.RDT('client', args.server, args.port)
    for msg_S in msg_L:
        print()
        print('NEED TO SEND: ' + msg_S)
        print()
        proceed = 0
        needSend = 1
        clone = msg_S
        while proceed == 0:
            if needSend == 1:
                rdt.rdt_3_0_send(msg_S)
                needSend = 0
                print("----attempting send")
                print()

            # try to receive message before timeout
            msg_S = None
            while msg_S == None:
                msg_S = rdt.rdt_3_0_receive()
                if msg_S is None:
                    if time_of_last_data + timeout < time.time():
                        needSend = 1
                        msg_S = clone
                        print("----timeout reached - resending")
                        print()
                        break
                    else:
                        continue
            time_of_last_data = time.time()
            if msg_S[:3] == "NAK":
                needSend = 1
                msg_S = clone
                print("----received NAK")
                print()

            if msg_S[:3] == "ACK":
                proceed = 1
                print("----received ACK")
                print()
        print("----proceeding")
        print()

        # print the result
        if msg_S:
            print('FINAL MESSAGE: ' + msg_S[4:] + '\n')
            1 + 1

    rdt.disconnect()