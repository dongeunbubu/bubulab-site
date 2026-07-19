import sys,re,os
FN=sys.argv[1]
text=open(FN,encoding="utf-8").read()
SIG={
 3:":)",11:":)",13:":)",22:":)",26:":)",46:":)",47:":)",50:":)",53:":)",81:":)",
 89:":)",92:":)",110:":)",116:":)",117:":)",132:":)",142:":)",161:":)",
 6:",,",16:",,",19:",,",24:",,",25:",,",28:",,",33:",,",43:",,",56:",,",69:",,",
 70:",,",76:",,",85:",,",100:",,",108:",,",114:",,",118:",,",125:",,",128:",,",
 32:"HH",34:"HH",60:"HH",103:"HH",136:"HH",150:"HH",48:"CMB",
}
END={":)":" :)</p>",",,":",,</p>","HH":" ㅎㅎ</p>"}
pars=re.findall(r'<p class="cx-rd-p">.*?</p>',text,re.S)
for idx,mk in sorted(SIG.items()):
    old=pars[idx]
    if mk=="CMB":
        assert old.endswith(",,</p>"), f"p{idx}:{old[-14:]!r}"
        new=old[:-6]+",, ㅎㅎ</p>"
    else:
        assert old.endswith(".</p>"), f"p{idx}:{old[-14:]!r}"
        new=old[:-5]+END[mk]
    assert text.count(old)==1, f"p{idx} not unique"
    text=text.replace(old,new,1)
open(FN+".tmp","w",encoding="utf-8").write(text); os.replace(FN+".tmp",FN)
print("signatures applied to",len(SIG),"paragraphs")
