import re
import json
from password import ocpassword
import owncloud
import os
import requests

def filterbottom(oc, p):
    print(p)
    if re.match('mvol/\d{4}/\d{4}/\d{4}/?$', p):
        return 'IIIF_Files/' + p

def runutil(oc, file_info):
    for entry in oc.list(file_info.get_path()):
        if entry.get_name() == 'ready':
            oc.delete(entry)
            os.utime("queue")
            oc.put_file(file_info, "queue")
            break

username = "ldr_oc_admin"
password = ocpassword
oc = owncloud.Client('https://s3.lib.uchicago.edu/owncloud')
oc.login(username, password)

r = requests.get('https://www2.lib.uchicago.edu/keith/tmp/cai.json')
r = r.json()
#allreadies = r['ready']
'''
allreadies =[

"mvol/0004/1914/0130/",
"mvol/0004/1914/0131/",
"mvol/0004/1914/0203/",
"mvol/0004/1914/0204/",
"mvol/0004/1914/0205/",
"mvol/0004/1914/0206/",
"mvol/0004/1914/0207/",
"mvol/0004/1914/0210/",
"mvol/0004/1914/0211/",
"mvol/0004/1914/0212/",
"mvol/0004/1914/0214/",
"mvol/0004/1914/0217/",
"mvol/0004/1914/0218/",
"mvol/0004/1914/0219/",
"mvol/0004/1914/0220/",
"mvol/0004/1914/0221/",
"mvol/0004/1914/0224/",
"mvol/0004/1914/0225/",
"mvol/0004/1914/0226/",
"mvol/0004/1914/0227/",
"mvol/0004/1914/0228/",
"mvol/0004/1914/0303/",
"mvol/0004/1914/0304/",
"mvol/0004/1914/0305/",
"mvol/0004/1914/0306/",
"mvol/0004/1914/0307/",
"mvol/0004/1914/0310/",
"mvol/0004/1914/0311/",
"mvol/0004/1914/0312/",
"mvol/0004/1914/0313/",
"mvol/0004/1914/0314/",
"mvol/0004/1914/0317/",
"mvol/0004/1914/0318/",
"mvol/0004/1914/0331/",
"mvol/0004/1914/0401/",
"mvol/0004/1914/0402/",
"mvol/0004/1914/0403/",
"mvol/0004/1914/0404/",
"mvol/0004/1914/0407/",
"mvol/0004/1914/0408/",
"mvol/0004/1914/0409/",
"mvol/0004/1914/0410/",
"mvol/0004/1914/0411/",
"mvol/0004/1914/0414/",
"mvol/0004/1914/0415/",
"mvol/0004/1914/0416/",
"mvol/0004/1914/0417/",
"mvol/0004/1914/0418/",
"mvol/0004/1914/0421/",
"mvol/0004/1914/0422/",
"mvol/0004/1914/0423/",
"mvol/0004/1914/0424/",
"mvol/0004/1914/0425/",
"mvol/0004/1914/0428/",
"mvol/0004/1914/0429/",
"mvol/0004/1914/0430/",
"mvol/0004/1914/0501/",
"mvol/0004/1914/0502/",
"mvol/0004/1914/0505/",
"mvol/0004/1914/0506/",
"mvol/0004/1914/0507/",
"mvol/0004/1914/0508/",
"mvol/0004/1914/0509/",
"mvol/0004/1914/0512/",
"mvol/0004/1914/0513/",
"mvol/0004/1914/0514/",
"mvol/0004/1914/0515/",
"mvol/0004/1914/0516/",
"mvol/0004/1914/0519/",
"mvol/0004/1914/0520/",
"mvol/0004/1914/0521/",
"mvol/0004/1914/0522/",
"mvol/0004/1914/0523/",
"mvol/0004/1914/0526/",
"mvol/0004/1914/0527/",
"mvol/0004/1914/0528/",
"mvol/0004/1914/0529/",
"mvol/0004/1914/0530/",
"mvol/0004/1914/0602/",
"mvol/0004/1914/0603/",
"mvol/0004/1914/0604/",
"mvol/0004/1914/0605/",
"mvol/0004/1914/0606/",
"mvol/0004/1914/0609/",
"mvol/0004/1914/0610/",
"mvol/0004/1914/0930/",
"mvol/0004/1914/1001/",
"mvol/0004/1914/1002/",
"mvol/0004/1914/1003/",
"mvol/0004/1914/1006/",
"mvol/0004/1914/1007/",
"mvol/0004/1914/1008/",
"mvol/0004/1914/1009/",
"mvol/0004/1914/1010/",
"mvol/0004/1914/1013/",
"mvol/0004/1914/1014/",
"mvol/0004/1914/1015/",
"mvol/0004/1914/1016/",
"mvol/0004/1914/1017/",
"mvol/0004/1914/1020/",
"mvol/0004/1914/1021/",
"mvol/0004/1914/1022/",
"mvol/0004/1914/1023/",
"mvol/0004/1914/1024/",
"mvol/0004/1914/1027/",
"mvol/0004/1914/1028/",
"mvol/0004/1914/1029/",
"mvol/0004/1914/1030/",
"mvol/0004/1914/1031/",
"mvol/0004/1914/1103/",
"mvol/0004/1914/1104/",
"mvol/0004/1914/1105/",
"mvol/0004/1914/1106/",
"mvol/0004/1914/1107/",
"mvol/0004/1914/1110/",
"mvol/0004/1914/1111/",
"mvol/0004/1914/1112/",
"mvol/0004/1914/1113/",
"mvol/0004/1914/1114/",
"mvol/0004/1914/1117/",
"mvol/0004/1914/1118/",
"mvol/0004/1914/1119/",
"mvol/0004/1914/1120/",
"mvol/0004/1914/1121/",
"mvol/0004/1914/1124/",
"mvol/0004/1914/1125/",
"mvol/0004/1914/1126/",
"mvol/0004/1914/1128/",
"mvol/0004/1914/1201/",
"mvol/0004/1914/1202/",
"mvol/0004/1914/1203/",
"mvol/0004/1914/1204/",
"mvol/0004/1914/1205/",
"mvol/0004/1914/1208/",
"mvol/0004/1914/1209/",
"mvol/0004/1914/1210/",
"mvol/0004/1914/1211/",
"mvol/0004/1914/1212/",
"mvol/0004/1914/1215/",
"mvol/0004/1914/1216/",
"mvol/0004/1914/1217/",
"mvol/0004/1914/1218/",
"mvol/0004/1914/1219/",
"mvol/0004/1915/0105/",
"mvol/0004/1915/0106/",
"mvol/0004/1915/0107/",
"mvol/0004/1915/0108/",
"mvol/0004/1915/0109/",
"mvol/0004/1915/0112/",
"mvol/0004/1915/0113/",
"mvol/0004/1915/0114/",
"mvol/0004/1915/0115/",
"mvol/0004/1915/0116/",
"mvol/0004/1915/0119/",
"mvol/0004/1915/0120/",
"mvol/0004/1915/0121/",
"mvol/0004/1915/0122/",
"mvol/0004/1915/0123/",
"mvol/0004/1915/0126/",
"mvol/0004/1915/0127/",
"mvol/0004/1915/0128/",
"mvol/0004/1915/0129/",
"mvol/0004/1915/0130/",
"mvol/0004/1915/0202/",
"mvol/0004/1915/0203/",
"mvol/0004/1915/0204/",
"mvol/0004/1915/0205/",
"mvol/0004/1915/0206/",
"mvol/0004/1915/0209/",
"mvol/0004/1915/0211/",
"mvol/0004/1915/0212/",
"mvol/0004/1915/0216/",
"mvol/0004/1915/0217/",
"mvol/0004/1915/0218/",
"mvol/0004/1915/0219/",
"mvol/0004/1915/0220/",
"mvol/0004/1915/0224/",
"mvol/0004/1915/0225/",
"mvol/0004/1915/0226/",
"mvol/0004/1915/0227/",
"mvol/0004/1915/0302/",
"mvol/0004/1915/0303/",
"mvol/0004/1915/0304/",
"mvol/0004/1915/0305/",
"mvol/0004/1915/0306/",
"mvol/0004/1915/0309/",
"mvol/0004/1915/0310/",
"mvol/0004/1915/0311/",
"mvol/0004/1915/0312/",
"mvol/0004/1915/0313/",
"mvol/0004/1915/0316/",
"mvol/0004/1915/0317/",
"mvol/0004/1915/0330/",
"mvol/0004/1915/0331/",
"mvol/0004/1915/0401/",
"mvol/0004/1915/0402/",
"mvol/0004/1915/0403/",
"mvol/0004/1915/0406/",
"mvol/0004/1915/0407/",
"mvol/0004/1915/0408/",
"mvol/0004/1915/0409/",
"mvol/0004/1915/0410/",
"mvol/0004/1915/0413/",
"mvol/0004/1915/0414/",
"mvol/0004/1915/0415/",
"mvol/0004/1915/0416/",
"mvol/0004/1915/0417/",
"mvol/0004/1915/0420/",
"mvol/0004/1915/0421/",
"mvol/0004/1915/0422/",
"mvol/0004/1915/0423/",
"mvol/0004/1915/0424/",
"mvol/0004/1915/0427/",
"mvol/0004/1915/0428/",
"mvol/0004/1915/0429/",
"mvol/0004/1915/0430/",
"mvol/0004/1915/0501/",
"mvol/0004/1915/0504/",
"mvol/0004/1915/0505/",
"mvol/0004/1915/0506/",
"mvol/0004/1915/0507/",
"mvol/0004/1915/0508/",
"mvol/0004/1915/0511/",
"mvol/0004/1915/0512/",
"mvol/0004/1915/0513/",
"mvol/0004/1915/0514/",
"mvol/0004/1915/0515/",
"mvol/0004/1915/0518/",
"mvol/0004/1915/0519/",
"mvol/0004/1915/0520/",
"mvol/0004/1915/0521/",
"mvol/0004/1915/0522/",
"mvol/0004/1915/0525/",
"mvol/0004/1915/0526/",
"mvol/0004/1915/0527/",
"mvol/0004/1915/0528/",
"mvol/0004/1915/0529/",
"mvol/0004/1915/0602/",
"mvol/0004/1915/0603/",
"mvol/0004/1915/0604/",
"mvol/0004/1915/0605/",
"mvol/0004/1915/0608/",
"mvol/0004/1915/0609/",
"mvol/0004/1915/0610/",
"mvol/0004/1915/0611/",
"mvol/0004/1915/0612/",
"mvol/0004/1915/0615/",
"mvol/0004/1915/0616/",
"mvol/0004/1915/1001/",
"mvol/0004/1915/1002/",
"mvol/0004/1915/1005/",
"mvol/0004/1915/1006/",
"mvol/0004/1915/1007/",
"mvol/0004/1915/1008/",
"mvol/0004/1915/1009/",
"mvol/0004/1915/1012/",
"mvol/0004/1915/1013/",
"mvol/0004/1915/1014/",
"mvol/0004/1915/1015/",
"mvol/0004/1915/1016/",
"mvol/0004/1915/1019/",
"mvol/0004/1915/1020/",
"mvol/0004/1915/1021/",
"mvol/0004/1915/1022/",
"mvol/0004/1915/1023/",
"mvol/0004/1915/1026/",
"mvol/0004/1915/1027/",
"mvol/0004/1915/1028/",
"mvol/0004/1915/1029/",
"mvol/0004/1915/1030/",
"mvol/0004/1915/1102/",
"mvol/0004/1915/1103/",
"mvol/0004/1915/1104/",
"mvol/0004/1915/1105/",
"mvol/0004/1915/1106/",
"mvol/0004/1915/1109/",
"mvol/0004/1915/1110/",
"mvol/0004/1915/1111/",
"mvol/0004/1915/1112/",
"mvol/0004/1915/1113/",
"mvol/0004/1915/1116/",
"mvol/0004/1915/1117/",
"mvol/0004/1915/1118/",
"mvol/0004/1915/1119/",
"mvol/0004/1915/1120/",
"mvol/0004/1915/1123/",
"mvol/0004/1915/1124/",
"mvol/0004/1915/1125/",
"mvol/0004/1915/1127/",
"mvol/0004/1915/1130/",
"mvol/0004/1915/1201/",
"mvol/0004/1915/1202/",
"mvol/0004/1915/1203/",
"mvol/0004/1915/1209/",
"mvol/0004/1915/1210/",
"mvol/0004/1915/1211/",
"mvol/0004/1915/1214/",
"mvol/0004/1915/1215/",
"mvol/0004/1915/1216/",
"mvol/0004/1915/1217/",
"mvol/0004/1916/0104/",
"mvol/0004/1916/0105/",
"mvol/0004/1916/0106/",
"mvol/0004/1916/0107/",
"mvol/0004/1916/0108/",
"mvol/0004/1916/0111/",
"mvol/0004/1916/0112/",
"mvol/0004/1916/0113/",
"mvol/0004/1916/0114/",
"mvol/0004/1916/0115/",
"mvol/0004/1916/0118/",
"mvol/0004/1916/0119/",
"mvol/0004/1916/0120/",
"mvol/0004/1916/0121/",
"mvol/0004/1916/0122/",
"mvol/0004/1916/0125/",
"mvol/0004/1916/0126/",
"mvol/0004/1916/0127/",
"mvol/0004/1916/0128/",
"mvol/0004/1916/0129/",
"mvol/0004/1916/0201/",
"mvol/0004/1916/0202/",
"mvol/0004/1916/0203/",
"mvol/0004/1916/0204/",
"mvol/0004/1916/0205/",
"mvol/0004/1916/0208/",
"mvol/0004/1916/0209/",
"mvol/0004/1916/0210/",
"mvol/0004/1916/0211/",
"mvol/0004/1916/0212/",
"mvol/0004/1916/0215/",
"mvol/0004/1916/0217/",
"mvol/0004/1916/0218/",
"mvol/0004/1916/0219/",
"mvol/0004/1916/0222/",
"mvol/0004/1916/0224/",
"mvol/0004/1916/0225/",
"mvol/0004/1916/0226/",
"mvol/0004/1916/0229/",
"mvol/0004/1916/0301/",
"mvol/0004/1916/0302/",
"mvol/0004/1916/0303/",
"mvol/0004/1916/0304/",
"mvol/0004/1916/0307/",
"mvol/0004/1916/0308/",
"mvol/0004/1916/0309/",
"mvol/0004/1916/0310/",
"mvol/0004/1916/0311/",
"mvol/0004/1916/0314/",
"mvol/0004/1916/0315/",
"mvol/0004/1916/0316/",
"mvol/0004/1916/0317/",
"mvol/0004/1916/0318/",
"mvol/0004/1916/0321/",
"mvol/0004/1916/0322/",
"mvol/0004/1916/0404/",
"mvol/0004/1916/0405/",
"mvol/0004/1916/0406/",
"mvol/0004/1916/0407/",
"mvol/0004/1916/0408/",
"mvol/0004/1916/0411/",
"mvol/0004/1916/0412/",
"mvol/0004/1916/0413/",
"mvol/0004/1916/0414/",
"mvol/0004/1916/0415/",
"mvol/0004/1916/0418/",
"mvol/0004/1916/0419/",
"mvol/0004/1916/0420/",
"mvol/0004/1916/0421/",
"mvol/0004/1916/0422/",
"mvol/0004/1916/0425/",
"mvol/0004/1916/0426/",
"mvol/0004/1916/0427/",
"mvol/0004/1916/0428/",
"mvol/0004/1916/0502/",
"mvol/0004/1916/0503/",
"mvol/0004/1916/0504/",
"mvol/0004/1916/0505/",
"mvol/0004/1916/0506/",
"mvol/0004/1916/0509/",
"mvol/0004/1916/0510/",
"mvol/0004/1916/0511/",
"mvol/0004/1916/0512/",
"mvol/0004/1916/0513/",
"mvol/0004/1916/0516/",
"mvol/0004/1916/0517/",
"mvol/0004/1916/0518/",
"mvol/0004/1916/0519/",
"mvol/0004/1916/0520/",
"mvol/0004/1916/0523/",
"mvol/0004/1916/0524/",
"mvol/0004/1916/0525/",
"mvol/0004/1916/0526/",
"mvol/0004/1916/0527/",
"mvol/0004/1916/0530/",
"mvol/0004/1916/0531/",
"mvol/0004/1916/0601/",
"mvol/0004/1916/0602/",
"mvol/0004/1916/0603/",
"mvol/0004/1916/0606/",
"mvol/0004/1916/0607/",
"mvol/0004/1916/0608/",
"mvol/0004/1916/0609/",
"mvol/0004/1916/0610/",
"mvol/0004/1916/1002/",
"mvol/0004/1916/1003/",
"mvol/0004/1916/1004/",
"mvol/0004/1916/1005/",
"mvol/0004/1916/1006/",
"mvol/0004/1916/1007/",
"mvol/0004/1916/1010/",
"mvol/0004/1916/1011/",
"mvol/0004/1916/1012/",
"mvol/0004/1916/1013/",
"mvol/0004/1916/1014/",
"mvol/0004/1916/1017/",
"mvol/0004/1916/1018/",
"mvol/0004/1916/1019/",
"mvol/0004/1916/1020/",
"mvol/0004/1916/1021/",
"mvol/0004/1916/1024/",
"mvol/0004/1916/1025/",
"mvol/0004/1916/1026/",
"mvol/0004/1916/1027/",
"mvol/0004/1916/1028/",
"mvol/0004/1916/1031/",
"mvol/0004/1916/1101/",
"mvol/0004/1916/1102/",
"mvol/0004/1916/1103/",
"mvol/0004/1916/1104/",
"mvol/0004/1916/1107/",
"mvol/0004/1916/1108/",
"mvol/0004/1916/1109/",
"mvol/0004/1916/1110/",
"mvol/0004/1916/1111/",
"mvol/0004/1916/1114/",
"mvol/0004/1916/1115/",
"mvol/0004/1916/1116/",
"mvol/0004/1916/1117/",
"mvol/0004/1916/1118/",
"mvol/0004/1916/1121/",
"mvol/0004/1916/1122/",
"mvol/0004/1916/1123/",
"mvol/0004/1916/1124/",
"mvol/0004/1916/1125/",
"mvol/0004/1916/1128/",
"mvol/0004/1916/1129/",
"mvol/0004/1916/1130/",
"mvol/0004/1916/1202/",
"mvol/0004/1916/1205/",
"mvol/0004/1916/1206/",
"mvol/0004/1916/1207/",
"mvol/0004/1916/1208/",
"mvol/0004/1916/1209/",
"mvol/0004/1916/1212/",
"mvol/0004/1916/1213/",
"mvol/0004/1916/1214/",
"mvol/0004/1916/1215/",
"mvol/0004/1916/1216/",
"mvol/0004/1916/1219/"
]
'''
allreadies = ["mvol/0004/1913/0206"]
allreadiesfiltered = []
for rt in allreadies:
    allreadiesfiltered = allreadiesfiltered + [filterbottom(oc, rt)]

for rt in allreadiesfiltered:
    runutil(oc, oc.file_info(rt))
