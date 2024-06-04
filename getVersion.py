import chardet

givepath=f"F:/MiniDL_v0.4.5_ZHCN/MiniDL_Data/globalgamemanagers"
# givepath=f"F:\MimiDL_pjm998_v0.1.5\Demo_v0.1.5\MiniDL_Data\globalgamemanagers"
gp=open(givepath,'rb')
# 偏移量 4660
gp.seek(4660,0)
gf=gp.read(7)
print(chardet.detect(gf))
print(f"{gf.decode('utf-8','ignore')}")
