#!/usr/bin/env python3
"""Numba-accelerated exact implementation of the frozen Campaign-1 beam objective."""
from __future__ import annotations
import hashlib,json,math
from collections import Counter
import numpy as np
from numba import njit

BOS_NAME='<BOS>';EOS_NAME='<EOS>';UNK_NAME='<UNK>'

@njit(cache=True)
def _fit_counts(flat,offs,T):
    # ids: targets 0..T-1, UNK=T, EOS=T+1, BOS=T+2
    UNK=T;EOS=T+1;BOS=T+2;S=T+3;V=T+2
    counts=np.zeros((S,S,V),dtype=np.int64)
    totals=np.zeros((S,S),dtype=np.int64)
    for k in range(len(offs)-1):
        p2=BOS;p1=BOS
        for j in range(offs[k],offs[k+1]):
            y=flat[j]
            counts[p2,p1,y]+=1;totals[p2,p1]+=1
            p2=p1;p1=y
        counts[p2,p1,EOS]+=1;totals[p2,p1]+=1
    return counts,totals

def build_lm_table(target_sequences,alpha=0.25):
    inventory=sorted({u for s in target_sequences for u in s})
    idx={u:i for i,u in enumerate(inventory)};T=len(inventory)
    offs=np.zeros(len(target_sequences)+1,dtype=np.int64)
    total=sum(len(s) for s in target_sequences)
    flat=np.empty(total,dtype=np.int16);q=0
    for i,s in enumerate(target_sequences):
        for x in s:flat[q]=idx[x];q+=1
        offs[i+1]=q
    counts,totals=_fit_counts(flat,offs,T)
    V=T+2;S=T+3
    nll=np.empty((S,S,V),dtype=np.float64)
    for a in range(S):
        for b in range(S):
            den=totals[a,b]+alpha*V
            for y in range(V):
                nll[a,b,y]=-math.log2((counts[a,b,y]+alpha)/den)
    h=hashlib.sha256()
    h.update(json.dumps(inventory,separators=(',',':')).encode())
    h.update(counts.tobytes());h.update(np.float64(alpha).tobytes())
    return inventory,nll,h.hexdigest()

def compile_voynich(stream,source_order=None):
    # Distinct token types with counts, independent token phonotactic scoring.
    cnt=Counter()
    unitfreq=Counter()
    for p in stream:
        for line in p['lines']:
            for tok in line['tokens']:
                u=tuple(tok['units']);cnt[u]+=1;unitfreq.update(u)
    if source_order is None:source_order=sorted(unitfreq,key=lambda u:(-unitfreq[u],u))
    uid={u:i for i,u in enumerate(source_order)}
    types=sorted(cnt)
    offs=np.zeros(len(types)+1,dtype=np.int64)
    flat=np.empty(sum(len(t) for t in types),dtype=np.int16)
    weights=np.empty(len(types),dtype=np.int64);q=0
    affected=[[] for _ in source_order]
    unit_occ=np.zeros(len(source_order),dtype=np.int64)
    for ti,t in enumerate(types):
        weights[ti]=cnt[t]
        seen=set()
        for x in t:
            j=uid[x];flat[q]=j;q+=1;unit_occ[j]+=cnt[t]
            if j not in seen:affected[j].append(ti);seen.add(j)
        offs[ti+1]=q
    return {'order':source_order,'flat':flat,'offs':offs,'weights':weights,
            'affected':[np.array(x,dtype=np.int32) for x in affected],'unit_occ':unit_occ,
            'token_types':len(types),'token_occurrences':sum(cnt.values())}

@njit(cache=True)
def _token_loss(flat,offs,ti,mapping,nll,T,override_uid=-1,override_val=-3):
    UNK=T;EOS=T+1;BOS=T+2
    p2=BOS;p1=BOS;loss=0.0
    for j in range(offs[ti],offs[ti+1]):
        u=flat[j]
        v=override_val if u==override_uid else mapping[u]
        if v==-1: continue
        y=UNK if v==-2 else v
        loss+=nll[p2,p1,y];p2=p1;p1=y
    loss+=nll[p2,p1,EOS]
    return loss

@njit(cache=True)
def _root_loss(flat,offs,weights,nll,T,n_units):
    m=np.full(n_units,-2,dtype=np.int16);s=0.0
    for ti in range(len(weights)):s+=weights[ti]*_token_loss(flat,offs,ti,m,nll,T)
    return s

@njit(cache=True)
def _expand(mapping_states,total_losses,emitted,complexities,null_counts,target_counts,
            depth,affected,flat,offs,weights,nll,T,unit_occ,max_null,lam,null_cost,merge_cost):
    B=mapping_states.shape[0]; maxC=T+1
    nrows=0
    for b in range(B):nrows+=T+(1 if null_counts[b]<max_null else 0)
    Js=np.empty(nrows,np.float64);Ls=np.empty(nrows,np.float64);Es=np.empty(nrows,np.int64)
    Cs=np.empty(nrows,np.float64);Ns=np.empty(nrows,np.int16);Parents=np.empty(nrows,np.int32);Vals=np.empty(nrows,np.int16)
    q=0
    for b in range(B):
        old=0.0
        for kk in range(len(affected)):
            ti=affected[kk];old+=weights[ti]*_token_loss(flat,offs,ti,mapping_states[b],nll,T)
        for val in range(T+1):
            if val==T:
                if null_counts[b]>=max_null:continue
                vv=-1;newE=emitted[b]-unit_occ[depth];newC=complexities[b]+null_cost;newN=null_counts[b]+1
            else:
                vv=val;newE=emitted[b];newC=complexities[b]+(merge_cost if target_counts[b,val]>0 else 0.0);newN=null_counts[b]
            new=0.0
            for kk in range(len(affected)):
                ti=affected[kk];new+=weights[ti]*_token_loss(flat,offs,ti,mapping_states[b],nll,T,depth,vv)
            L=total_losses[b]-old+new
            H=L/newE if newE>0 else np.inf
            Js[q]=H+lam*newC;Ls[q]=L;Es[q]=newE;Cs[q]=newC;Ns[q]=newN;Parents[q]=b;Vals[q]=vv;q+=1
    return Js,Ls,Es,Cs,Ns,Parents,Vals

@njit(cache=True)
def _full_score(mapping,flat,offs,weights,nll,T):
    loss=0.0;emit=0
    for ti in range(len(weights)):
        w=weights[ti];loss+=w*_token_loss(flat,offs,ti,mapping,nll,T)
        # emitted count per type
        n=0
        for j in range(offs[ti],offs[ti+1]):
            if mapping[flat[j]]!=-1:n+=1
        emit+=w*n
    return loss,emit

def _lex_key(assign,order,target_names,depth):
    d={order[i]:assign[i] for i in range(depth+1)}
    return tuple((u,'' if d[u]==-1 else target_names[d[u]]) for u in sorted(d))

def fast_beam_search(train_stream,val_stream,target_sequences,beam_width=256,alpha=.25,max_null=2,lam=.015,null_cost=2.0,merge_cost=.5):
    target_names,nll,lm_sha=build_lm_table(target_sequences,alpha);T=len(target_names)
    train=compile_voynich(train_stream);order=train['order'];N=len(order)
    val=compile_voynich(val_stream,order)
    rootL=_root_loss(train['flat'],train['offs'],train['weights'],nll,T,N)
    rootE=int(sum(train['unit_occ']))
    maps=np.full((1,N),-2,dtype=np.int16);losses=np.array([rootL]);emits=np.array([rootE],dtype=np.int64)
    comps=np.array([0.0]);nulls=np.array([0],dtype=np.int16);tc=np.zeros((1,T),dtype=np.int16)
    for d in range(N):
        Js,Ls,Es,Cs,Ns,Parents,Vals=_expand(maps,losses,emits,comps,nulls,tc,d,train['affected'][d],train['flat'],train['offs'],train['weights'],nll,T,train['unit_occ'],max_null,lam,null_cost,merge_cost)
        # Exact frozen tie-break: J then lexicographically sorted source/target pairs.
        rows=[]
        for q in range(len(Js)):
            par=int(Parents[q]);v=int(Vals[q]);a=maps[par].copy();a[d]=v
            rows.append((float(Js[q]),_lex_key(a,order,target_names,d),q,a))
        rows.sort(key=lambda x:(x[0],x[1]));rows=rows[:beam_width]
        K=len(rows);newmaps=np.empty((K,N),dtype=np.int16);newtc=np.empty((K,T),dtype=np.int16)
        idx=np.empty(K,dtype=np.int64)
        for k,(_,_,q,a) in enumerate(rows):
            idx[k]=q;newmaps[k]=a;par=int(Parents[q]);newtc[k]=tc[par]
            v=int(Vals[q]);
            if v>=0:newtc[k,v]+=1
        maps=newmaps;tc=newtc;losses=Ls[idx];emits=Es[idx];comps=Cs[idx];nulls=Ns[idx]
    finals=[]
    for b in range(len(maps)):
        L,E=_full_score(maps[b],val['flat'],val['offs'],val['weights'],nll,T)
        H=L/E if E else math.inf;J=H+lam*float(comps[b])
        finals.append((J,_lex_key(maps[b],order,target_names,N-1),b,H,E))
    finals.sort(key=lambda x:(x[0],x[1]));J,_,b,H,E=finals[0]
    mapping={order[i]:(None if maps[b,i]==-1 else target_names[int(maps[b,i])]) for i in range(N)}
    canon=json.dumps(sorted((k,'NULL' if v is None else v) for k,v in mapping.items()),ensure_ascii=False,separators=(',',':')).encode()
    msha=hashlib.sha256(canon).hexdigest()
    trainL,trainE=_full_score(maps[b],train['flat'],train['offs'],train['weights'],nll,T)
    return {'mapping':mapping,'mapping_sha256':msha,'target_lm_sha256':lm_sha,'target_inventory':target_names,
            'source_unit_order':order,'complexity':float(comps[b]),'null_count':int(nulls[b]),
            'train_loss':float(trainL/trainE),'validation_loss':float(H),'validation_objective':float(J),
            'train_emitted_symbols':int(trainE),'validation_emitted_symbols':int(E),
            'beam_survivors':len(maps),'train_token_types':train['token_types'],'validation_token_types':val['token_types']}
