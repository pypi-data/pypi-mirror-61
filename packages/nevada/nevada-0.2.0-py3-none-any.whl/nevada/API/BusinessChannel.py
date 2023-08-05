from nevada.Common.Connector import *
from typing import List
import jsonpickle
import json

class BusinessInfo:
    def __init__(self, json_def):
        if type(json_def) is str:
            json_def = json.loads(json_def)
        s = json_def
        self.isMobileNaverLogin = None if 'isMobileNaverLogin' not in s else s['isMobileNaverLogin']
        self.isMobileNaverPay = None if 'isMobileNaverPay' not in s else s['isMobileNaverPay']
        self.isMobileNaverTalkTalk = None if 'isMobileNaverTalkTalk' not in s else s['isMobileNaverTalkTalk']
        self.isNaverLogin = None if 'isNaverLogin' not in s else s['isNaverLogin']
        self.isNaverPay = None if 'isNaverPay' not in s else s['isNaverPay']
        self.isNaverTalkTalk = None if 'isNaverTalkTalk' not in s else s['isNaverTalkTalk']
        self.isStoreFarm = None if 'isStoreFarm' not in s else s['isStoreFarm']
        self.mobileCertStatus = None if 'mobileCertStatus' not in s else s['mobileCertStatus']
        self.naAccountId = None if 'naAccountId' not in s else s['naAccountId']
        self.naAccountType = None if 'naAccountType' not in s else s['naAccountType']
        self.originalPath = None if 'originalPath' not in s else s['originalPath']
        self.site = None if 'site' not in s else s['site']
        self.thumbnailPath = None if 'thumbnailPath' not in s else s['thumbnailPath']
        self.useNaverPayNaScript = None if 'useNaverPayNaScript' not in s else s['useNaverPayNaScript']
        self.useSaNaScript = None if 'useSaNaScript' not in s else s['useSaNaScript']
        self.useStoreFarmNaScript = None if 'useStoreFarmNaScript' not in s else s['useStoreFarmNaScript']

class UpdateBusinessChannelObject:
    def __init__(self, nccBusinessChannelId, site_url, name):
        self.businessInfo = {'site' : site_url}
        self.channelTp = 'SITE'
        self.inspectRequestMsg = None
        self.name = name
        self.nccBusinessChannelId = nccBusinessChannelId

class CreateBusinessChannelObject:
    def __init__(self, site_url, name):
        self.businessInfo = {'site' : site_url}
        self.channelTp = 'SITE'
        self.inspectRequestMsg = None
        self.name = name

class BusinessChannelObject:
    def __init__(self, json_def):
        if type(json_def) is str:
            json_def = json.loads(json_def)
        s = json_def
        self.adultStatus = None if 'adultStatus' not in s else s['adultStatus']
        self.blackStatus = None if 'blackStatus' not in s else s['blackStatus']
        self.businessInfo = None if 'businessInfo' not in s else BusinessInfo(s['businessInfo'])
        self.channelKey = None if 'adultStatus' not in s else s['adultStatus']
        self.channelTp = None if 'adultStatus' not in s else s['adultStatus']
        self.customerId = None if 'customerId' not in s else s['customerId']
        self.delFlag = None if 'delFlag' not in s else s['delFlag']
        self.editTm = None if 'editTm' not in s else s['editTm']
        self.enabled = None if 'enabled' not in s else s['enabled']
        self.firstChargeTm = None if 'firstChargeTm' not in s else s['firstChargeTm']
        self.inspectTm = None if 'inspectTm' not in s else s['inspectTm']
        self.mobileInspectStatus = None if 'mobileInspectStatus' not in s else s['mobileInspectStatus']
        self.name = None if 'name' not in s else s['name']
        self.nccBusinessChannelId = None if 'nccBusinessChannelId' not in s else s['nccBusinessChannelId']
        self.pcInspectStatus = None if 'pcInspectStatus' not in s else s['pcInspectStatus']
        self.regTm = None if 'regTm' not in s else s['regTm']
        self.status = None if 'status' not in s else s['status']
        self.statusReason = None if 'statusReason' not in s else s['statusReason']


class BusinessChannel:
    def __init__(self, base_url: str, api_key: str, secret_key: str, customer_id: int):
        self.conn = Connector(base_url, api_key, secret_key, customer_id)

    BusinessChannelObjectList = List[BusinessChannelObject]
    BusinessChannelIdList = List[str]

    def get_business_channel_list(self) -> BusinessChannelObjectList:
        result = self.conn.get('/ncc/channels')

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)

        return business_channel_list

    def get_business_channel_list_by_type(self, tp: str) -> BusinessChannelObjectList:
        result = self.conn.get('/ncc/channels', {'channelTp': tp})

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)

        return business_channel_list

    def get_business_channel_list_by_ids(self, ids: BusinessChannelIdList) -> BusinessChannelObjectList:
        ids = ",".join(ids)
        query = {'ids': ids}
        result = self.conn.get('/ncc/channels', query)

        business_channel_list = []
        for arr in result:
            channel = BusinessChannelObject(arr)
            business_channel_list.append(channel)
        return business_channel_list

    def get_business_channel(self, businessChannelId) -> BusinessChannelObject:
        result = self.conn.get('/ncc/channels/' + businessChannelId)
        result = BusinessChannelObject(result)

        return result

    def create_business_channel(self, CreateBusinessChannelObj: CreateBusinessChannelObject) -> BusinessChannelObject:

        data = jsonpickle.encode(CreateBusinessChannelObj, unpicklable=False)
        data = json.loads(data)
        data = CommonFunctions.dropna(data)
        data_str = json.dumps(data)
        result = self.conn.post('/ncc/channels', data_str)
        result = BusinessChannelObject(result)
        return result

    def update_business_channel(self, fields,
                                UpdateBusinessChannelObj: UpdateBusinessChannelObject) -> BusinessChannelObject:
        data = jsonpickle.encode(UpdateBusinessChannelObj, unpicklable=False)
        data = json.loads(data)
        data = CommonFunctions.dropna(data)
        data_str = json.dumps(data)
        result = self.conn.put('/ncc/channels', data_str, fields)
        result = BusinessChannelObject(result)
        return result

    def delete_business_channel(self, businessChannelId: str):
        self.conn.delete('/ncc/channels/' + businessChannelId)
        return True

    def delete_business_channel_by_ids(self, ids: BusinessChannelIdList):
        ids = ",".join(ids)
        query = {'ids': ids}
        self.conn.delete('/ncc/channels', query)
        return True
