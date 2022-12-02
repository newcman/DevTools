#coding=utf-8
import json
import os
import re

startMode_cold = 0 # 冷起
startMode_hot = 1 # 热起

def getAttr(path,key) :
    result = 0
    if path.get(key) != None:
        result = path.get(key).get('time')
    return result
def filterLogs(dir, name,templateId,startMode):
    if not os.path.exists(dir):
        print("%s 目录不存在" % dir)
        return None
    files = []
    if os.path.isfile(dir):
        files.append(dir)
    else:
        data = os.listdir(dir)
        print(data)
        for item in data:
            f = os.path.join(dir, item)
            if os.path.isfile(f):
                files.append(f)

    lastSessionId = ''
    lastPath = ''
    lastTemplateId = ''
    result = []
    for f in files:
        with open(file=f, mode='r', encoding='utf-8') as file:
            print(f)
            try:
                for line in file:
                    reResult = re.match(
                        '^(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}:\d{2})\.\d+\s(\d+)\s(\d+)\s(\w+)\s\[(\w+)\](.*)', line)
                    if reResult is not None and len(reResult.groups()) == 7:
                        try:
                            time = reResult.groups()[0]
                            time1 = reResult.groups()[1]
                            pName = reResult.groups()[2]
                            tName = reResult.groups()[3]
                            leve = reResult.groups()[4]
                            tag = reResult.groups()[5]
                            content = reResult.groups()[6]
                            if tag == 'ChannelProcessor' and content.lstrip().startswith('chnp==tpl==updateTemplateId'):
                                lastTemplateId = content.lstrip().replace("chnp==tpl==updateTemplateId:", "") 
                                print("templateId %s " % lastTemplateId)
                            elif tag == 'CompletionRateV2' and content.lstrip().startswith('sendMsg json data') and lastTemplateId == templateId:
                                content = content.lstrip().replace("sendMsg json data : ", "") \
                                    .replace("\\", "") \
                                    .replace("\"{", "{") \
                                    .replace("}\"", "}")
                                # print("%s is %s" % ("time", time))
                                # print("%s is %s" % ("time1", time1))
                                # print("%s is %s" % ("pName", pName))
                                # print("%s is %s" % ("tName", tName))
                                # print("%s is %s" % ("tag", tag))
                                # print("%s is %s" % ("content", content))
                                content = json.loads(content)
                                sessionId = content.get('ext').get('session_id')
                                pathStr = content.get('ext').get('path')
                                if lastSessionId == '':
                                    lastPath = pathStr
                                    lastSessionId = sessionId
                                elif lastSessionId == sessionId and len(lastPath) < len(pathStr):
                                    lastPath = pathStr
                                    lastSessionId = sessionId
                                elif lastSessionId != sessionId:
                                    # print("lastTemplateId %s  lastSessionId %s lastPath %s" % (lastTemplateId, lastSessionId, lastPath))  
                                    result.append((lastSessionId, lastPath))
                                    lastPath = pathStr
                                    lastSessionId = sessionId

                        except Exception as e:
                            print("error1")
                            print(e)

            except Exception as e:
                print("error2")
                print(e)  
    result.append((lastSessionId, lastPath))
    # 写文件
    # 以写模式打开文件
    fileName = '%s.csv' % name
    if os.path.exists(fileName):
        os.remove(fileName)
    f = open(fileName, "w")
    output = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
        "entry", "initStart", "initEnd", "joinStart", "joinEnd", "inputMsg", "liveVideo", "userOnline", "publicChat",
        "anchorInfo",
        "completion","entry->liveVideo","entry->joinStart", "joinStart->liveVideo")
    f.write(output)
    totalCount = 0
    entryTotal = 0
    joinStartTotal = 0
    joinEndTotal = 0
    inputTotal = 0
    videoTotal = 0
    initStartTotal = 0
    initEndTotal = 0
    liveNpsStartLoadTotal = 0
    liveNpsEndLoadTotal = 0
    entranceEndLoadTotal = 0
    entranceStartLoadTotal = 0
    for item in result:
        sessionId, path = item
        print(sessionId)
        # print(path)
        try:
            entry =getAttr(path,'entry')
            if entry == 0:
                continue
            initStartNode = path.get('initStart')
            print("initStartNode %s" % initStartNode)
            if startMode == startMode_hot and initStartNode != None :
                print("过滤热起，不显示冷起的数据")
                continue
            initStart = 0
            if initStartNode !=None:
                  initStart = path.get('initStart').get('time')
            if startMode == startMode_cold and initStart ==0 :
                print("该冷起无效")
                continue
            print("initStart %s" % initStart)

            initEnd = getAttr(path,'initEnd')
            joinStart = getAttr(path,'joinStart')
            joinEndNode = path.get('joinEnd')
            if joinEndNode == None:
                continue
            print("joinEndNode %s" % joinEndNode)
            joinEnd = path.get('joinEnd').get('time')
            inputMsg = getAttr(path,'inputMsg')
            liveVideo = getAttr(path,'liveVideo')
            userOnline =  getAttr(path,'userOnline')
            publicChat = getAttr(path,'publicChat')
            anchorInfo = getAttr(path,'anchorInfo')
            completion = getAttr(path,'completion')

            liveNpsStartLoad = getAttr(path,'livenpsStartLoad')
            liveNpsEndLoad = getAttr(path,'livenpsEndLoad')
            entranceStartLoad = 0
            try:
                entranceStartLoad = path.get('entranceStartLoad').get('time')
            except:
                pass
            entranceEndLoad = 0
            try:
                entranceEndLoad = path.get('entranceEndLoad').get('time')
            except:
                pass
            output = "%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d,%d,%d,%d\n" % (
                entry, initStart, initEnd, joinStart, joinEnd, inputMsg, liveVideo, userOnline, publicChat, anchorInfo,
                completion,liveVideo - entry, joinStart-entry,liveVideo-joinStart)
            f.write(output)
            # print(entry)
            totalCount += 1
            entryTotal += entry
            joinStartTotal += joinStart
            joinEndTotal += joinEnd
            inputTotal += inputMsg
            videoTotal += liveVideo
            initStartTotal += initStart
            initEndTotal += initEnd
            liveNpsStartLoadTotal += liveNpsStartLoad
            liveNpsEndLoadTotal += liveNpsEndLoad

            entranceStartLoadTotal += entranceStartLoad
            entranceEndLoadTotal += entranceEndLoad
        except e:
            print("异常===============")
            print("path %s" % path)
            print(e)
            pass
    # avg = "%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (
    #             0, 0, 0, (joinStartTotal - entryTotal) / totalCount, (joinEndTotal - entryTotal) / totalCount,  (inputTotal - entryTotal) / totalCount, (videoTotal - entryTotal) / totalCount, 0, 0, 0,
    #             0)
    # output = avg
    if totalCount ==0:
        totalCount =1
    avgStr = "count:%d, entry->initStart:%d, entry->initEnd:%d, joinStart:%d, joinEnd:%d, entry->input:%d, entry->video:%d, join->video:%d, liveNpsLoad:%d, entry->liveNpsEnd:%d, entry->entranceStart:%d, entry->entranceEnd:%d\n" % (
                totalCount, (initStartTotal - entryTotal) / totalCount, 
                (initEndTotal - entryTotal) / totalCount, (joinStartTotal - entryTotal) / totalCount, (joinEndTotal - entryTotal) / totalCount,  (inputTotal - entryTotal) / totalCount, (videoTotal - entryTotal) / totalCount, 
                (videoTotal - joinStartTotal) / totalCount, (liveNpsStartLoadTotal - entryTotal)/totalCount, (liveNpsEndLoadTotal - entryTotal)/totalCount,
                (entranceStartLoadTotal - entryTotal)/totalCount, (entranceEndLoadTotal - entryTotal)/totalCount)
    
    print("\n\n\n\n")
    print(avgStr)
    print("\n\n\n\n")
    f.write(output)
    f.close()


if "__main__" == __name__:
    # 
    # android_1634527515778_decry 2.8  count:10, initStart:674, initEnd:2129, joinStart:4335, joinEnd:6899, input:5901, entry->video:6101, join->video:1766, 0, 0, 0
    # android_1634529197463_decry 2.9  count:11, initStart:654, initEnd:2018, joinStart:4201, joinEnd:7307, input:5659, entry->video:5817, join->video:1615, 0, 0, 0
    # android_1634526025781_decry 2.9  count:6, initStart:548, initEnd:1884, joinStart:3949, joinEnd:6881, input:5377, entry->video:5546, join->video:1597, 0, 0, 0
    # android_1634525520176_decry 2.9  count:17, initStart:780, initEnd:2113, joinStart:4177, joinEnd:7177, input:5611, entry->video:5772, join->video:1595, 0, 0, 0
    # android_1635406681287_decry 2.10 count:12, initStart:615, initEnd:1846, joinStart:3564, joinEnd:6150, input:4734, entry->video:4849, join->video:1285, 0, 0, 0
    # android_1635304865962_decry 2.10 count:13, initStart:596, initEnd:1817, joinStart:3396, joinEnd:5873, input:4493, entry->video:4611, join->video:1215, 0, 0, 0
#     android_1635772214776_decry 210
    # android_1635503612381_decry split count:10, initStart:449, initEnd:1738, joinStart:3082, joinEnd:5571, input:4462, entry->video:4571, join->video:1489, 0, 0, 0
    
    # android_1638362656591_decry 212 count:15, initStart:281, initEnd:654, joinStart:1174, joinEnd:1580, input:1463, entry->video:1580, join->video:406, 0, 0, 0
    # android_1637304138508_decry 211 count:17, initStart:300, initEnd:648, joinStart:1133, joinEnd:2022, input:1351, entry->video:2520, join->video:1386, 0, 0, 0

    # unionbaidu-android_1640760468854_decry.zip 新 count:16, entry->initStart:346, entry->initEnd:754, joinStart:1142, joinEnd:1431, entry->input:1335, entry->video:1601, join->video:458, liveNpsLoad:2, entry->liveNpsEnd:260, 0
    # unionbaidu-android_1639453349095_decry.zip 旧 count:12, entry->initStart:267, entry->initEnd:620, joinStart:1124, joinEnd:1724, entry->input:1284, entry->video:1449, join->video:324, liveNpsLoad:1, entry->liveNpsEnd:165, entry->entranceStart:189, entry->entranceEnd:233
  

   # unionbaidu-android_1641975964493_2.15_decry  count:3, entry->initStart:164, entry->initEnd:526, joinStart:844, joinEnd:1128, entry->input:1019, entry->video:1227, join->video:383, liveNpsLoad:1, entry->liveNpsEnd:110, entry->entranceStart:-1641975007457, entry->entranceEnd:-1641975007457
   #unionbaidu-android_1646811527759_2.18_decry   count:3, entry->initStart:166, entry->initEnd:411, joinStart:1191, joinEnd:2454, entry->input:1589, entry->video:1793, join->video:601, liveNpsLoad:1, entry->liveNpsEnd:99, entry->entranceStart:-1646810999785, entry->entranceEnd:-1646810999785



    yylib = '/Users/xson/Documents/2.17/unionbaidu-android_1646919512851_2.17_纯YYdecry'
    filterLogs(yylib, "unionbaidu-android_1646919512851_2.17_纯YYdecry","16777217",startMode_hot)
