import requests
import sqlite3
import json

def defPhone():
        malumot={}
        p="Biza mavjud brendlar⤵️\n\n"
        r=requests.get(f"https://api-mobilespecs.azharimm.site/v2/brands")
        if r.json()['status']:
            for res in r.json()['data']:
                malumot[str(res['brand_name']).title()]=res['brand_slug']
            return malumot
        else: return 

def TelefonNomi(chat_id):
    p={}
    con=sqlite3.connect("baza.db")
    cur=con.cursor()
    con.commit()
    cur.execute('SELECT brend FROM login WHERE id=?',[(chat_id)])
    b_name=cur.fetchone()[0]    
    set_p=f"https://api-mobilespecs.azharimm.site/v2/brands/{b_name}"
    rr=requests.get(set_p)
    for one in rr.json()['data']['phones']:
        p[str(one['phone_name'])]=str(one['slug'])
    return p 

def TelefonHaqida(chat_id,tekst):  
    try:
        con=sqlite3.connect("baza.db")
        cur=con.cursor()
        con.commit()
        cur.execute('SELECT telefon FROM login WHERE id=?',[(chat_id)])
        t_name=cur.fetchone()[0]
        t=json.loads(str(t_name).replace("'", '"'))
        req=requests.get(f"http://api-mobilespecs.azharimm.site/v2/{t[tekst]}")
        baza={}
        tel=""
        tel+=f"▶️Brendi:{(req.json()['data']['brand']).title()}\n▶️Telefon nomi:{(req.json()['data']['phone_name']).title()}\n\n"
        spec=req.json()['data']['specifications']
        for i in range(len(spec)):
            s=spec[i]['specs']
            tel+="➡️"+spec[i]['title']+"\n"
            for j in range(len(s)):
                ss=s[j]['val'][0]
                tel+=f"{s[j]['key']}: {ss}\n"
            tel+="\n"
        baza['malumot']=tel
        baza['brend']=req.json()['data']['brand']
        baza['rasm']=req.json()['data']['phone_images'][0]
        return baza
    except: return 

