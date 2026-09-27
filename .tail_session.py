
import json,sys
p=sys.argv[1]; n=int(sys.argv[2])
rows=[]
with open(p,'rb') as f:
    f.seek(0,2); size=f.tell(); f.seek(max(0,size-6_000_000)); data=f.read().decode('utf-8','ignore').splitlines()[1:]
for line in data:
    try: o=json.loads(line)
    except: continue
    t=o.get('type'); ts=o.get('timestamp','')[:19]
    m=o.get('message') or {}
    c=m.get('content')
    if t=='user':
        if isinstance(c,str): rows.append((ts,'USER',c))
        elif isinstance(c,list):
            for b in c:
                if b.get('type')=='text': rows.append((ts,'USER',b['text']))
    elif t=='assistant' and isinstance(c,list):
        for b in c:
            if b.get('type')=='text' and b['text'].strip(): rows.append((ts,'ASSIST',b['text']))
for ts,who,txt in rows[-n:]:
    print('['+ts+'] '+who+': '+txt[:1800].replace('\n',' / '))
    print()
