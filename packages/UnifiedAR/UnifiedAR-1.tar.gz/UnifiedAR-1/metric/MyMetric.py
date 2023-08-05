import math

import pandas as pd
from intervaltree import intervaltree
from matplotlib.pylab import plt
from pandas.core.frame import DataFrame
from prompt_toolkit.shortcuts import set_title
from wardmetrics.core_methods import eval_events

import result_analyse.SpiderChart as spiderchart


def eval(real_a_event, pred_a_event, acts,debug=0):
    revent = {}
    pevent = {}
    for act in acts:
        revent[act]=[]
        pevent[act]=[]
        
    sec1=pd.to_timedelta('1s').value
    for i,e in real_a_event.iterrows():
        revent[e.Activity].append((e.StartTime.value/sec1, e.EndTime.value/sec1))
    for i,e in pred_a_event.iterrows():
        pevent[e.Activity].append((e.StartTime.value/sec1,e.EndTime.value/sec1))

    result={}
    for act in acts:
        if debug :print(act,"======================")
        result[act] = eval_my_metric(revent[act], pevent[act],debug=debug)
        
    return result


def eval_my_metric(real,pred,alpha=1,debug=0):

        real_tree=_makeIntervalTree(real,'r')
        pred_tree=_makeIntervalTree(pred,'p')
        
        metric={}
        
        rcalc=[]
        for i in range(len(real)):
            r=real[i]
            
            rp=real[i-1] if i>0 else (0,0)
            rn=real[i+1] if(i<len(real)-1) else (r[1]*1000,r[1]*1000)
            info={'r':r,'length':r[1]-r[0], 'overlap':0, 'overfill_start':0,'overfill_end':0, 'underfill_start':0, 'underfill_end':0,'exist':0, 'fragment':0}
            rcalc.append(info)
            minp=r[1]*1000
            maxp=0
            for p in pred_tree[r[0]:r[1]]:
                info['exist']=1
                info['overlap']+=max(0,min(r[1],p[1])-max(r[0],p[0]))
                minp=min(minp,p[0])                
                maxp=max(maxp,p[1])                
                info['fragment']+=1
            info['overfill_start']  +=max(0,r[0]-minp) if info['exist'] else 0
            info['overfill_end']    +=max(0,maxp-r[1]) if info['exist'] else 0
            info['underfill_start'] +=max(0,minp-r[0]) if info['exist'] else 0
            info['underfill_end']   +=max(0,r[1]-maxp) if info['exist'] else 0
            info['overfill_start']  =min(info['overfill_start'],(r[0]-rp[1])/2)
            info['overfill_end']    =min(info['overfill_end'],(rn[0]-r[1])/2)

        orphan_pred=[]    
        pcalc=[]
        for p in pred:
            info={'p':p,'length':p[1]-p[0],'overlap':0, 'lenref':0.000001, 'nexist':1, 'merge':0}
            pcalc.append(info)
            for r in real_tree[p[0]:p[1]]:
                info['overlap']+=max(0,min(r[1],p[1])-max(r[0],p[0]))
                info['lenref']+=r[1]-r[0]
                info['merge'] +=1
                info['nexist']=0
        
            if info['nexist']:
                orphan_pred.append(p)

        if(debug):
            plot_events_with_event_scores([r['length'] for r in rcalc],[p['length'] for p in pcalc],real,pred,'length')
            plot_events_with_event_scores([r['overlap'] for r in rcalc],[p['overlap'] for p in pcalc],real,pred,'overlap')
            plot_events_with_event_scores([r['overlap']/r['length'] for r in rcalc],[p['overlap']/p['length'] for p in pcalc],real,pred,'overlap/length')
            plot_events_with_event_scores([(r['length']-r['overlap'])/r['length'] for r in rcalc],[min(1,(p['length']-p['overlap'])/p['lenref']) for p in pcalc],real,pred,'len-overlap/len & len-overlap/lenref')
            plot_events_with_event_scores([1-math.exp(-alpha * (r['overfill_start']+r['overfill_end'])/r['length']) for r in rcalc],[0 for p in pcalc],real,pred,'overfill rate')
            plot_events_with_event_scores([1-math.exp(-alpha * (r['underfill_start']+r['underfill_end'])/r['length']) for r in rcalc],[0 for p in pcalc],real,pred,'underfill rate')
        
        
        metric['existance']=_Existence(rcalc,pcalc)
        metric['length']=_Length(rcalc,pcalc)
        metric['overlap_rate']=_OverlapRate(rcalc,pcalc)
        metric['positional']=_Positional(rcalc,pcalc,alpha)
        if (len(real)==0 or len(pred)==0):
            metric['cardinality']={'tp':0,'fp':0,'fn':0}    
        else:
            real_scores, pred_scores, event_scores, standard_score_statistics=eval_events(real,pred)
            metric['cardinality']=_Cardinality(event_scores)

        for m in metric:
            metric[m]['recall']     =metric[m]['tp']/(metric[m]['tp']+metric[m]['fn']) if (metric[m]['tp']+metric[m]['fn'])!=0 else 0
            metric[m]['precision']  =metric[m]['tp']/(metric[m]['tp']+metric[m]['fp']) if (metric[m]['tp']+metric[m]['fp'])!=0 else 0
            metric[m]['f1']         =2*metric[m]['recall']*metric[m]['precision']/(metric[m]['recall']+metric[m]['precision']) if (metric[m]['recall']+metric[m]['precision'])!=0 else 0
        return metric


def plot_events_with_event_scores(gt_event_scores, detected_event_scores, ground_truth_events, detected_events, label=None):
    fig,ax = plt.subplots(figsize=(10, 3))
    ax.set_title(label)
    maxsize=10
    for i in range(min(maxsize,len(detected_events))):
        d = detected_events[i]
        plt.axvspan(d[0], d[1], 0, 0.5,linewidth=1,edgecolor='k',facecolor='r', alpha=.6)
        plt.text((d[1] + d[0]) / 2, 0.2, "%g" %round(detected_event_scores[i],2 if detected_event_scores[i]<10 else 0), horizontalalignment='center', verticalalignment='center')

    for i in range(min(maxsize,len(ground_truth_events))):
        gt = ground_truth_events[i]
        plt.axvspan(gt[0], gt[1], 0.5, 1,linewidth=1,edgecolor='k',facecolor='g', alpha=.6)
        plt.text((gt[1] + gt[0]) / 2, 0.8, "%g" %round(gt_event_scores[i],2 if gt_event_scores[i]<10 else 0), horizontalalignment='center', verticalalignment='center')

    plt.tight_layout()

    
    plt.show()
    

def _makeIntervalTree(evnt,label):
    
    tree = intervaltree.IntervalTree()
    for e in evnt:
        tree[e[0]:e[1]] = e
    return tree


def _Existence(rcalc,pcalc):
    m={'tp':0,'fp':0,'fn':0}        
    for r in rcalc:
        m['tp']+=r['exist']
        m['fn']+=1-r['exist']
    for p in pcalc:
        m['fp']+=p['nexist']

    return m


def _Length(rcalc,pcalc):
    m={'tp':0,'fp':0,'fn':0}        
    for r in rcalc:
        m['tp']+=r['overlap']
        m['fn']+=r['length']-r['overlap']
    for p in pcalc:
        m['fp']+=p['length']-p['overlap']

    return m

def _OverlapRate(rcalc,pcalc):
    m={'tp':0,'fp':0,'fn':0}        
    for r in rcalc:
        m['tp']+=r['overlap']/r['length']
        m['fn']+=(r['length']-r['overlap'])/r['length']
    for p in pcalc:
        m['fp']+=min(1,(p['length']-p['overlap'])/p['lenref'])

    return m

def _Positional(rcalc,pcalc,alpha):
    m={'tp':0,'fp':0,'fn':0}        
    for r in rcalc:
        fp=1-math.exp(-alpha * (r['overfill_start']+r['overfill_end'])/r['length']) 
        fn=1-math.exp(-alpha * (r['underfill_start']+r['underfill_end'])/r['length']) if r['exist'] else 1
        m['tp']+=1-min(1,fp+fn)
        m['fn']+=fn
        m['fp']+=fp

    for p in pcalc:
        m['fp']+=p['nexist']
    return m

def _Cardinality(event_scores):
    m={'tp':0,'fp':0,'fn':0}        
    m['tp']=2*event_scores['C']
    m['fp']=event_scores["I'"]+event_scores['M']+event_scores["M'"]+(event_scores["FM'"]+event_scores["FM"])/2
    m['fn']=event_scores['D']+event_scores['F']+event_scores["F'"]+(event_scores["FM'"]+event_scores["FM"])/2
    return m

def testMyMetric(real,pred):
    
    metrics=eval_my_metric(real,pred,debug=1)
    df=DataFrame(metrics)
    print(df)
    df=df.drop(['tp','fp','fn'])
    spiderchart.plot(df,[0.25,.5,.75])
    #plotSpiderChart(df[df.index=='precision'],[0.25,.5,.75])
    #plotSpiderChart(df[df.index=='f1'],[0.25,.5,.75])
    print(metrics)
