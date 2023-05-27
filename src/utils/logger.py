class Log:
    
    @staticmethod
    def info(name, msg):
        print("[INFO] {0} - {1}".format(name,msg))

    @staticmethod
    def error(name, msg, trace=None):
        print("[ERROR] {0} - {1}".format(name,msg), trace)


    