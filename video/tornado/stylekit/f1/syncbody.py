# f1/body.part = the EP.1 part (everything before the ending's banner comment) + f1/ending.part
import os; S = os.path.dirname(os.path.abspath(__file__)) + "/"
b = open(S + "body.part").read(); e = open(S + "ending.part").read()
k = b.index("\n      // ================= เสียงรถไฟ ตอนจบ")
head = b[:k]
head = head[: head.rstrip("\n").__len__()]  # drop trailing blank lines
open(S + "body.part", "w").write(head + "\n" + e)
print("synced")
