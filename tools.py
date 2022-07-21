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
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")


if __name__ == '__main__':
    log_setup.main("info","debug")
    # create()
    test()
