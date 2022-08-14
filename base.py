import logging
import os


class BaseSpider:
    def __init__(self) -> None:
        pass

    def exportHtml(self, source, fileName):
        import re
        try:
            os.makedirs(self.fullpath, exist_ok=True)
            fileName = re.sub('[\/:*?"<>|]', '_', fileName)  # 去掉非法字符
            with open(f'./{self.fullpath}/{fileName}.html', "w", encoding="utf-8") as f:
                f.write(source)
            logging.info(f"{fileName} 保存成功")
        except OSError as error:
            logging.error(f'create dir error: {error}')
        except Exception as error:
            logging.error(f'exportHtml error: {error}')


if __name__ == '__main__':
    data = BaseSpider()
    # data.main()
