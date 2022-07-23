# 用于创建一个脚本
import log_setup
import logging
def create():
    import index
    strList=index.getIndex()
    with open("batch.sh", 'w', encoding='utf-8') as fp:
        for item in strList:
            # write each item on a new line
            fp.write("python dian.py %s\n" % item)
def test():
    # logger = logging.getLogger(__name__)
    # logger = logging 
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")


# logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d:%H:%M:%S',
#                     level=logging.DEBUG)

# logger = logging.getLogger(__name__)
# logger.debug("This is a debug log")
# logger.info("This is an info log")
# logger.critical("This is critical")
# logger.error("An error occurred")

def getit():
    string="20121212 12:12:12"
    print(string[:8])

if __name__ == '__main__':
    # log_setup.main("info","debug")
    # import html
    # html.getCurDate()
    # # create()
    # test()
    getit()
