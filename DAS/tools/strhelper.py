
def GetMiddleStr(content,startStr,endStr):
  '''
  获取开始跟结束中间的字符串
  :param content: 全部字符串
  :param startStr: 开始字符
  :param endStr: 结束字符
  :return: 夹在中间的字符串
  '''
  startIndex = content.index(startStr)
  if startIndex>=0:
    startIndex += len(startStr)
  endIndex = content.index(endStr)
  return content[startIndex:endIndex].strip()


def GetSqlDateStr(datestr):
  '''
  将20180901转换成2018-09-01
  :param datestr: 20180901类型的日期
  :return: 2018-09-01类型的日期
  '''
  sdatestr = datestr.strip()
  result_date = sdatestr[:4] + '-' + sdatestr[4:6] + '-' + sdatestr[6:8]
  return result_date