


request_count = 0

def run():

    global request_count

    for i in range(100):
        request_count = request_count + 1
        print('===>')




if __name__ == '__main__':

    run()

    print(request_count)


