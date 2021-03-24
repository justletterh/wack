import os,json,requests,sqlite3

fp=lambda *x:os.path.join(".",*x)
j=lambda *x:os.path.join(*x)
fetch=lambda u:requests.get(url=u).json()
div="-"*os.get_terminal_size().columns

cfgfp=fp("config.json")

def conf(s):
    global cfg,url,dbfp
    default='{"url":"https://gist.githubusercontent.com/justletterh/95c1ba0ab44040bf0221c861eb175700/raw/a6494e7e76b60c3406ff07036c29588743edec34/colors.json","db":"colors.db"}'
    if not os.path.exists(s):
        f=open(s,"w+")
        f.write(default)
        f.close()
    f=open(s,"r+")
    cfg=json.load(f)
    f.close()
    try:
        url=cfg["url"]
    except KeyError:
        url=cfg["url"]=json.loads(default)["url"]
    try:
        dbfp=fp(cfg["db"])
    except KeyError:
        cfg["db"]=json.loads(default)["db"]
        dbfp=cfg["db"]
    return cfg

def dodb(*,quiet=False,newdb=False):
    global db
    if newdb and os.path.exists(dbfp):
        os.remove(dbfp)
    tmp=os.path.exists(dbfp)
    db=sqlite3.connect(dbfp)
    if not tmp:
        c=db.cursor()
        c.execute("CREATE TABLE all_colors (id int,name text,r int,g int,b int,rgb text,hex text)")
        db.commit()
    del tmp

def main(*,quiet=False,newdb=False):
    l=fetch(url)
    if not quiet:
        print(f"Loaded {len(l)} Colors From The URL!!!")
    dodb(quiet=quiet,newdb=newdb)
    c=db.cursor()
    x=1
    for i in l:
        c.execute("INSERT INTO all_colors VALUES (?,?,?,?,?,?,?)",(x,i["name"],i["r"],i["g"],i["b"],i["rgb"],i["hex"]))
        x+=1
    tmp=len(c.execute("SELECT name FROM all_colors").fetchall())
    db.commit()
    print(f"{div}\nSaving {tmp} Colors...")
    del tmp

def init(*,quiet=False,newdb=False):
    print("\n".join([div,"Starting...",div]))
    conf(cfgfp)
    main(quiet=quiet,newdb=newdb)
    db.close()
    if not quiet:
        print("\n".join([div,"Done!!!",div]))

if __name__=="__main__":
    overwrite=True
    quiet=False
    init(quiet=quiet,newdb=overwrite)