"""Hand fixes of caption phrase breaks after build_bk0.py (run after every rebuild)."""
import json
C=json.load(open('script/captions.json'))
def merge(a,b,new=None):
    for i in range(len(C)-1):
        if C[i]['text']==a and C[i+1]['text']==b:
            C[i]['text']=new or a+b; C[i]['end']=C[i+1]['end']; del C[i+1]; return
    raise SystemExit('not found '+a+b)
def split_retext(a,b,na,nb):
    for i in range(len(C)-1):
        if C[i]['text']==a and C[i+1]['text']==b: C[i]['text'],C[i+1]['text']=na,nb; return
    raise SystemExit('not found '+a+b)
split_retext('คืออย่างนี้นะปี','1915','คืออย่างนี้นะ','ปี 1915')
merge('สนามเพลาะได้','จริง')
split_retext('ถังน้ำสี่สิบ','เก้าคัน','ถังน้ำ','49 คัน')
split_retext('ไปถึงแค่','สามสิบสอง','ไปถึงแค่','32 คัน')
split_retext('หนักยี่สิบแปดตัน','แต่บอกคนงาน','หนัก 28 ตัน','แต่บอกคนงาน')
split_retext('สิบห้ากันยา','1916','15 กันยา','1916')
split_retext('ปืนใหญ่หกปอนด์','แล้วตอกลังไม้','ปืนใหญ่ 6 ปอนด์','แล้วตอกลังไม้')
merge('ที่ที่คนข้าม','ไม่ได้')
merge('กลางเมือง','แฟลร์')
merge('เดินตามก้น','มัน')
json.dump(C,open('script/captions.json','w'),ensure_ascii=False,indent=0)
print(len(C),max(len(c['text']) for c in C))
