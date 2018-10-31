#!
"""
* @desc 商品分析-商品明细-总条数
* @serviceName getBrandProductDetailCount
* @dimensions LogicFlag_BrandId_ThirdIndId_VirtualId_ShopType_TerminalId_STime_ETime_[SkuId]
* @indicators PV_UV_AvgVisitNum_AvgStayTime_ToCartNum_ToCartRate_DealNum_DealAmt_DealPriceAvg_DealUser_DealProNum_DealRate
* @attributes nan
* @options nan
* @note 返回Count-总条数

* @desc 交易分析-交易详情(分页）
* @serviceName getBrandTradeDetailPage
* @dimensions LogicFlag_BrandId_ThirdIndId_VirtualId_ShopType_TerminalId_STime_ETime_[SkuId]
* @indicators PV_UV_DealUser_DealNum_DealProNum_DealAmt_OrdUser_OrdNum_OrdProNum_OrdAmt
* @attributes nan
* @options PageNum_RowNum
* @note 不支持排序，按照默认的维度排序
"""

targetFile = "ck_interface_definition.txt"
lineStarter = "     * @"


def buildSerivceList(targetFile, lineStarter):
    serviceDefinition = []
    with open(targetFile, mode='r', encoding='utf-8') as tfd:
        cnt = 0
        data = dict()
        for line in tfd:
            if not line.startswith(lineStarter):
                continue
            index = cnt % 7
            data[index] = line.replace(lineStarter, "")
            # print("index=%s, line=%s" % (index, line))
            if index is 6:
                serviceDefinition.append(data)
                data = dict()  # init to empty
            cnt = cnt+1

    return serviceDefinition


services = buildSerivceList(targetFile, lineStarter)

print(len(services))
print(services[0])


def transfer_line(value, keep_opts=True):
    parts = value.split('_')
    if len(parts) is 0:
        return "Collections.emptyList()"
    elif len(parts) is 1:
        if parts[0] is "nan\n":
            return "Collections.<String>emptyList()"
        else:
            return 'Collections.singletonList("' + parts[0].replace("\n", "") + '")'
    else:
        if "[" in value:
            result = 'Arrays.asList('
            l = []
            if keep_opts:
                for val in parts:
                    if "[" not in val:
                        continue
                    val = val.replace("\n", "")
                    val = val.replace("[", "")
                    val = val.replace("]", "")
                    l.append(val)
                result = result + \
                    ",".join(list(map(lambda x: '"'+x+'"', l))) + ')'
            else:  # 不保留opts的
                for val in parts:
                    if "[" in val:
                        continue
                    val = val.replace("\n", "")
                    l.append(val)
                result = result + \
                    ",".join(list(map(lambda x: '"'+x+'"', l))) + ')'
            return result
        else:
            if keep_opts:
                return "Collections.<String>emptyList()"
            else:
                return "Arrays.asList(" + ','.join(['"'+val.replace("\n", "")+'"' for val in parts]) + ")"


def transfer_by_index(value, index, opts):
    if index is 0 or index is 1 or index is 6:
        return value.replace("\n", "")
    elif index is 2:
        return transfer_line(value, opts)
    elif index is 3 or index is 4 or index is 5:
        return transfer_line(value)

    return ""


def getPart(data, index, opt=True):
    parts = data[index].split(' ')
    value = ""
    if parts is None:
        print("skip... unknown format, %s" % data[index])
    elif len(parts) is 1:
        value = ""
    elif len(parts) is 2:
        value = parts[1]
    else:
        value = "".join(parts[1:])
    return transfer_by_index(value, index, opt)


template = '//%s\n%s("%s",\n %s,\n %s,\n %s,\n %s,\n %s,\n "%s"),'
for item in services:
    cmt = getPart(item, 0)
    sn = getPart(item, 1)
    di = getPart(item, 2, opt=False)
    di_opt = getPart(item, 2)
    ind = getPart(item, 3)
    attr = getPart(item, 4)
    opts = getPart(item, 5)
    note = getPart(item, 6)
    print(template % (cmt, sn, sn, di, di_opt, ind, attr, opts, note))
