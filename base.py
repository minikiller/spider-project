import logging
import log_setup

class BaseSpider:
    def __init__(self) -> None:
        pass

    def exportHtml(self, source, fileName):

        import os
        try:
            os.makedirs(self.fullpath, exist_ok=True)
        except OSError as error:
            logging.error(f'create dir error: {error}')
        with open(f'./{self.fullpath}/{fileName}.html', "w") as f:
            f.write(source)
            logging.info(f"{fileName} 保存成功")
