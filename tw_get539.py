import requests
import os
import re
import time
import datetime
import pymysql

# 使用chrome瀏覽器資訊
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
}

# 創建網路連接
s = requests.Session()
url = 'https://www.taiwanlottery.com.tw/Lotto/Dailycash/history.aspx'

# 需先獲取網頁查詢資訊"認證"及可查詢最大年份 ;
r = s.get(url=url, headers=headers)
__VIEWSTATEGENERATORpat = re.compile('<input.*?id="__VIEWSTATEGENERATOR" value="(.*?)" />')
__VIEWSTATEGENERATOR = __VIEWSTATEGENERATORpat.findall(r.text)[0]
__VIEWSTATEpat = re.compile('<input.*?id="__VIEWSTATE" value="(.*?)" />')
__VIEWSTATE = __VIEWSTATEpat.findall(r.text)[0]
__EVENTVALIDATIONpat = re.compile('<input.*?id="__EVENTVALIDATION" value="(.*?)" />')
__EVENTVALIDATION = __EVENTVALIDATIONpat.findall(r.text)[0]

# 從此年開始抓取各年份完整紀錄,官網最早只能選從103年開始
start_year = 103
last_year = 109

# 資料儲存成檔案設定,預設儲存在 D 磁碟跟目錄下存成 SuperLotto638_日期.txt 文件
# 儲存路徑
filepath = 'c:\\a\\'
# 儲存檔案名稱
today = str(datetime.date.today()).replace('-', '')
filename = 'Lotto539' + '_' + today + '.txt'
# 將路徑和檔案名稱結合成完整路徑
savepath = os.path.join(filepath, filename)

# 查詢
def SuperLotto638(savedata, updatedb, nosort):
    url = 'https://www.taiwanlottery.com.tw/Lotto/Dailycash/history.aspx'
    
    # 查詢y年m月的開獎號碼
    for y in range(start_year, int(last_year) + 1):
        for m in range(1, 13):
            # 先將無資料旗標設定為假
            nodata_flog = False
            # 如果無資料旗標沒有變為True則進入資料查詢
            if not nodata_flog:
                # 查詢表單提交格式
                post_data = {
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__LASTFOCUS': '',
                    '__VIEWSTATE': __VIEWSTATE,
                    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
                    '__EVENTVALIDATION': __EVENTVALIDATION,
                    'D539Control_history1$DropDownList1': '5',
                    'D539Control_history1$chk': 'radYM',
                    'D539Control_history1$dropYear': y,
                    'D539Control_history1$dropMonth': m,
                    'D539Control_history1$btnSubmit': '查詢'
                }
                print ("submit ok.")

                # 建立請求對象
                request = s.get(url=url, headers=headers)
                # 發送資料請求
                lottodata = s.post(url=url, headers=headers, data=post_data)
                #print(lottodata.text) #確認是否有網頁數據資料

                # 確認是否有資料
                nodatapat = re.compile('<span id="D539Control_history1_Label1".*?>(.*?)</span>')
                nodata = nodatapat.findall(lottodata.text)[0]

                if nodata == "查無資料":
                    # 如果沒有資料則將無資料旗標改為True,並跳出循環
                    nodata_flog = True
                    print('%s年%s月份已經查無資料' % (y, m))
                    break
                print ("check get data ok.")

                # 期別
                DrawTermpat = re.compile(
                    r'<span id="D539Control_history1_dlQuery_D539_DrawTerm_\d{1,2}">(.*?)</span>')
                DrawTerm = DrawTermpat.findall(lottodata.text)
                # 開獎日
                DDatepat = re.compile(r'<span id="D539Control_history1_dlQuery_D539_DDate_\d{1,2}">(.*?)</span>')
                DDate = DDatepat.findall(lottodata.text)
                # 兌獎截止日
                EDatepat = re.compile(r'<span id="D539Control_history1_dlQuery_D539_EDate_\d{1,2}">(.*?)</span>')
                EDate = EDatepat.findall(lottodata.text)
                # 開獎大小順序 前6個號碼為第一區數字 第7個號碼為第二區數字
                No1pat = re.compile(r'<span id="D539Control_history1_dlQuery_No1_\d{1,2}">(.*?)</span>')
                No1 = No1pat.findall(lottodata.text)
                No2pat = re.compile(r'<span id="D539Control_history1_dlQuery_No2_\d{1,2}">(.*?)</span>')
                No2 = No2pat.findall(lottodata.text)
                No3pat = re.compile(r'<span id="D539Control_history1_dlQuery_No3_\d{1,2}">(.*?)</span>')
                No3 = No3pat.findall(lottodata.text)
                No4pat = re.compile(r'<span id="D539Control_history1_dlQuery_No4_\d{1,2}">(.*?)</span>')
                No4 = No4pat.findall(lottodata.text)
                No5pat = re.compile(r'<span id="D539Control_history1_dlQuery_No5_\d{1,2}">(.*?)</span>')
                No5 = No5pat.findall(lottodata.text)
                #No6pat = re.compile(r'<span id="D539Control_history1_dlQuery_No6_\d{1,2}">(.*?)</span>')
                #No6 = No6pat.findall(lottodata.text)
                #No7pat = re.compile(r'<span id="D539Control_history1_dlQuery_No7_\d{1,2}">(.*?)</span>')
                #No7 = No7pat.findall(lottodata.text)

                if nosort:
                    No1pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo1_\d{1,2}">(.*?)</span>')
                    No1 = No1pat.findall(lottodata.text)
                    No2pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo2_\d{1,2}">(.*?)</span>')
                    No2 = No2pat.findall(lottodata.text)
                    No3pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo3_\d{1,2}">(.*?)</span>')
                    No3 = No3pat.findall(lottodata.text)
                    No4pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo4_\d{1,2}">(.*?)</span>')
                    No4 = No4pat.findall(lottodata.text)
                    No5pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo5_\d{1,2}">(.*?)</span>')
                    No5 = No5pat.findall(lottodata.text)
                    #No6pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo6_\d{1,2}">(.*?)</span>')
                    #No6 = No6pat.findall(lottodata.text)
                    #No7pat = re.compile(r'<span id="D539Control_history1_dlQuery_SNo7_\d{1,2}">(.*?)</span>')
                    #No7 = No7pat.findall(lottodata.text)

                # 數據處理
                # 官網會先提供由大到小的期數,改為由小到大的期數順序
                for i in range(len(DrawTerm) - 1, -1, -1):

                    # 螢幕顯示處理數據
                    print('開始查詢%s年%s月份資訊 :' % (y, m))
                    print("第%s期威力彩, 開獎日期:%s,兌獎截止日期:%s" % (DrawTerm[i], DDate[i], EDate[i]))
                    print("號碼大小順序為 :%s,%s,%s,%s,%s" % (
                        No1[i], No2[i], No3[i], No4[i], No5[i]))
                    print('=' * 100)

                    # 將數據寫入文件
                    if savedata:

                        filedata = '"' + DrawTerm[i] + '"' + ',' + '"' + No1[i] + '"' + ',' + '"' + No2[i] + '"' + ',' + '"' + No3[i] + '"' + ',' + '"' + No4[i] + '"' + ',' + '"' + No5[
                            i] + '"' + '\n'
                        print (filedata)

                        with open(savepath, "a+", encoding="utf8") as f:
                            f.write(filedata)

                # 關閉資料庫連接
                if updatedb:
                    cursor.close()
                    conn.close()

                # 避免伺服器查詢負載過大,切換月份時延遲5秒再進行下一次查詢
                time.sleep(1)

def main():
    #想在電腦儲存檔案請將參數改為 savedata=True , 想將資料寫入數據庫請將updatedb = False改為updatedb = True
    # 抓取威力彩資料
    SuperLotto638(savedata = True, updatedb = False, nosort = True)

if __name__ == '__main__':
    main()
