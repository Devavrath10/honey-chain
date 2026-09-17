from datetime import datetime, timezone
from hashlib import sha256
from typing import Literal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app=FastAPI(title='Honey Chain API',version='0.1.0')
app.add_middleware(CORSMiddleware,allow_origins=['*'],allow_methods=['*'],allow_headers=['*'])

class Telemetry(BaseModel):
    hive_id:str
    temperature:float=Field(ge=-20,le=70)
    humidity:float=Field(ge=0,le=100)
    weight:float=Field(gt=0)

class BatchCreate(BaseModel):
    batch_id:str
    beekeeper:str
    hive_id:str
    floral_source:str
    quantity_kg:float=Field(gt=0)

HIVES={}
BATCHES={
 'HC-TG-2026-001':{'batch_id':'HC-TG-2026-001','beekeeper':'Demo Rural Beekeeper','hive_id':'HIVE-101','floral_source':'Multi-flora','quantity_kg':28,'status':'VERIFIED','events':['Hive registered','Harvest recorded','Quality test passed','Packaged','QR issued']}
}

def health(t,h,w):
    score=100; alerts=[]
    if t>36: score-=18; alerts.append('High hive temperature')
    if t<31: score-=15; alerts.append('Low hive temperature')
    if h>70: score-=15; alerts.append('High humidity; inspection recommended')
    if w<30: score-=12; alerts.append('Low hive weight')
    risk='LOW' if score>=90 else 'MEDIUM' if score>=70 else 'HIGH'
    return {'score':max(score,0),'risk':risk,'alerts':alerts}

def digest(obj): return sha256(repr(sorted(obj.items())).encode()).hexdigest()

@app.get('/health')
def api_health(): return {'service':'honey-chain','status':'ok'}

@app.post('/api/v1/telemetry')
def ingest(x:Telemetry):
    reading=x.model_dump(); reading['recorded_at']=datetime.now(timezone.utc).isoformat(); reading['ai']=health(x.temperature,x.humidity,x.weight); reading['payload_hash']=digest(x.model_dump())
    HIVES[x.hive_id]=reading
    return reading

@app.get('/api/v1/hives')
def list_hives(): return list(HIVES.values())

@app.post('/api/v1/batches',status_code=201)
def create_batch(x:BatchCreate):
    if x.batch_id in BATCHES: raise HTTPException(409,'Batch already exists')
    b=x.model_dump(); b['status']='CREATED'; b['events']=['Batch created']; b['record_hash']=digest(x.model_dump()); BATCHES[x.batch_id]=b
    return b

@app.get('/api/v1/batches/{batch_id}')
def verify_batch(batch_id:str):
    b=BATCHES.get(batch_id.upper())
    if not b: raise HTTPException(404,'Batch not found')
    return {'authentic':True,**b}

@app.post('/api/v1/batches/{batch_id}/events')
def add_event(batch_id:str,event:Literal['Harvest recorded','Quality test passed','Packaged','QR issued','Dispatched','Received']):
    b=BATCHES.get(batch_id.upper())
    if not b: raise HTTPException(404,'Batch not found')
    b['events'].append(event); b['last_event_hash']=sha256((batch_id+event+str(len(b['events']))).encode()).hexdigest()
    if event=='QR issued': b['status']='VERIFIED'
    return b
