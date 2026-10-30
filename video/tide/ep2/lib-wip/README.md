# งานค้างของ lib สำหรับ ทะเลลด EP.2 (หยุดกลางทางเพราะโควตาการใช้งานหมด 30 ต.ค. 2026)

ยังไม่ผ่านการตรวจ อย่าเอาไปทับ `video/tide/lib/` ตรงๆ (EP.1 ใช้ lib นั้นอยู่) ให้ทดสอบกับ EP.2 ก่อน

- `tide.js` (ต่อจาก `video/tide/lib/tide.js`): คลื่นลูกใหญ่ `Tide.bigWave` · น้ำท่วมค้างในหมู่บ้าน `Tide.hillFlood` ·
  น้ำท่วมหน้าโรงแรม `Tide.landFlood` (ห่วงเป็ดลอย `o.duck`) · `tideHill` / `tideBeach` รับ `shop: "gone"`, `flood`, `mark`, `line` ถึง 2
  เอกสาร API อยู่หัวไฟล์ครบ แต่ตัวโค้ดเขียนยังไม่เสร็จทุกส่วน ต้องถ่ายภาพนิ่งตรวจทีละฟังก์ชัน
- `tide2.js` (ไฟล์ใหม่ โหลดต่อจาก tide.js): ช็อตแทรกมือตาจุ่นคว้าข้อมือ `Sets.tideGrab` + `Tide.grab` (เสร็จ) ·
  นักท่องเที่ยวเกาะกระติก `Sets.tideRaft` + `Tide.raft` (เสร็จ) · หน้าร้านยายถือรูป `Sets.tideShopFront` (ยังไม่ได้ทำ)
- `tidecast.js`: ท่า `grabHold` · `yanked` · `lookUp` (เพิ่มแล้ว ยังไม่ได้ตรวจในตอน)
