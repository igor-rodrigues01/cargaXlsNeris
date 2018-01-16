import sys

class Utils:

    def error_message_and_stop_script(self,custom_msg,exception_msg=False):
        if not exception_msg:
            print('\n{}\n'.format(custom_msg))
        else:
            print('\n{}\n{}\n'.format(exception_msg,custom_msg))

        sys.exit()


















