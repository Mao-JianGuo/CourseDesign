''' 爬虫数据IO处理类'''
import os
class DataStorage(object):
    # filepath
    # type#:cover\update
    def __init__(self, key, usip_word, writeType):
        self.filepath = '.'+os.sep+'data'+os.sep+'key:' + key + 'word:' + usip_word + '.txt'
        print(self.filepath)
        self.type = writeType

    def writeData(self, data):
        try:
            if isinstance(data, list):
                if self.type == 'cover':
                    print('开始全量覆盖更新，更新条目：' + str(len(data)))
                    self.__coverWrite(data)
                    return 0
                elif self.type == 'update':
                    self.__updateWrite(data)
                    return 0
        except IOError as e:
            print('文件打开失败，清检查路径或权限')
            print(e)

    # 全量覆盖
    def __coverWrite(self, data: 'list'):
        try:
            file = open(self.filepath, 'w')
            for x in range(len(data)):
                file.write(str(data[x]) + '\n')
        except IOError as e:
            print(e)
        finally:
            file.close()

    ##增量更新
    def __updateWrite(self, data):
        # 读取数据
        if os.path.exists(self.filepath):
            try:
                file = open(self.filepath, 'r')
                oldData = file.read().splitlines()
            except IOError as e:
                print(e)
                return 0
            finally:
                file.close()
            # 历史数据 {list:str}
            count = 0
            for x in range(len(data)):
                if isinstance(data[x], str):
                    tmp_str = data[x]
                else:
                    tmp_str = str(data[x])
                # 增量添加新数据
                if tmp_str not in oldData:
                    count += 1
                    oldData.append(tmp_str)
            # 写入文件
            print("【增量更新】新增数据：" + str(count) + "条")
            self.__coverWrite(oldData)
        else:
            self.__coverWrite(data)


if __name__ == '__main__':
    test = DataStorage('同仁堂', '为自己健康代言', 'update')
    data = ['123', '132']
    test.writeData(data)
