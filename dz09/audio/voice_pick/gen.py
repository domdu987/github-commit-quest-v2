import sys; sys.path.insert(0,'../th'); import tts_fal
T="ศูนย์ครับ คนเจ็บไม่ตอบสนอง... เดี๋ยว! เฮ้ย! แล้ววิทยุก็เงียบไป คืนวันศุกร์ ฝนถล่มกรุงเทพฯ บนทางด่วน รถชนกันเป็นแพ ยาวจนมองไม่เห็นปลายทาง พ่อมีเคสด่วนลูก รออีกแป๊บเดียว"
V={"1_Ohm":"tKtPl8obOBs5uPMei6yN","2_Framel":"roe71slHhRlwDI6IPvB6","3_Duang":"jucSqawHKM1rUNf78oZQ","4_Thanid":"3SQTl9c6zS9vh1r8maCI","5_Pikiir":"wwlSjZ6z5ZVMXPlwGV6Q"}
for k,v in V.items():
    try: tts_fal.synth(T,k,v,1.15)
    except SystemExit as e: print(k,"FAILED",e)
print(len(T),"chars each")
