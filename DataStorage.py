''' 爬虫数据IO处理类'''
import os
# 数据存储类， 实现全量更新和增量更新
#全量更新：新建或完全覆盖历史的爬取数据，适用于第一次搜索特定的关键词和公众号时使用
#增量更新：对特定关键词或公众号进行数据爬取后，在历史爬取的数据基础上追加新增的数据，适合实时监控公众号文章时使用
#增量更新这个功能，主要是为了针对任务书所提到的对公众号实时监控并更新爬取数据而开发的
class DataStorage(object):
    # filepath
    # type#:cover\update
    def __init__(self, key, usip_word, writeType):
        self.filepath = '.'+os.sep+'data'+os.sep+'key:' + key + 'word:' + usip_word + '.txt'
        self.key = key
        self.usip_word = usip_word
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
                file.write('{'+'\'key\': '+self.key+'  \'usip\': ' + self.usip_word + '  content: ' + str(data[x]) + '\n')
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

