from datatool.dataset_abstract import Dataset
import os
import wget
import pandas as pd
from intervaltree.intervaltree import IntervalTree
import json
from general.utils import Data
import numpy as np


class CASAS(Dataset):
    def __init__(self,data_path,data_dscr):
        super().__init__(data_path,data_dscr);

    def _load(self):
        rootfolder= self.data_path
        #rootfolder='datasetfiles/CASAS/'+name+'/'
        datafile = rootfolder+"/data.txt"

        all = pd.read_csv(datafile, r"\s+", None, header=None,
                          names=["date", "time", "SID", "value", "activity", "hint"])
        all.time = pd.to_datetime(all.date+" " + all.time,
                                  format='%Y-%m-%d %H:%M:%S')
        all = all.drop(columns=['date'])

        sensor_events = all
        sensor_events=sensor_events.sort_values(['time'])
        

        activity_events = []
        start = {}
        seit=sensor_events[sensor_events.hint == sensor_events.hint].iterrows()
        for i, e in seit:

            if(e.hint == 'begin'):
                start[e.activity] = e

            elif(e.hint == 'end'):
                if not(e.activity in start):
                    continue

                actevent = {"StartTime": start[e.activity].time,	"EndTime": e.time,
                            "Activity": e.activity, 'Duration': e.time-start[e.activity].time}
                # actevent=[start[splt[0]].time,e.time,splt[0]]
                # start[splt[0]]=None
                activity_events.append(actevent)
                del start[e.activity]

        activity_events=pd.DataFrame(data=activity_events,
            columns=["StartTime", "EndTime", "Activity", 'Duration'])
        activity_events = activity_events.sort_values(['StartTime', 'EndTime'])
        
        activities = activity_events['Activity'].unique()
        
        # 3
        # sensor_events=sensor_events.drop(columns=['activity_hint'])

        sensor_events = sensor_events.drop(columns=['activity', 'hint'])
        sensor_events = sensor_events[["SID", "time", "value"]]
        sensor_desc = pd.DataFrame(columns=['ItemId', 'ItemName', 'Cumulative',
                                            'Nominal', 'OnChange', 'ItemRange', 'Location', 'Object', 'SensorName'])
        tmp_sensors = sensor_events['SID'].unique()
        for s in tmp_sensors:
            item = {'ItemId': s, 'ItemName': s, 'Cumulative': 0, 'Nominal': 1, 'OnChange': 1, 'ItemRange': {
                'range': ['OFF', 'ON']}, 'Location': 'None', 'Object': 'None', 'SensorName': 'None'}
            if(s[0] == 'I'):
                item['ItemRange'] = {'range': ['ABSENT', 'PRESENT']}
            if(s[0] == 'D'):
                item['ItemRange'] = {'range': ['CLOSE', 'OPEN']}
            if(s[0] == 'E'):
                item['ItemRange'] = {
                    'range': ['STOP_INSTRUCT', 'START_INSTRUCT']}
            if(s == 'asterisk'):
                item['ItemRange'] = {'range': ['END', 'START']}
            if(s.startswith('AD1')):
                item['Nominal'] = 0
                item['ItemRange'] = {"max": 3.0, "min": 0.0}
            sensor_desc = sensor_desc.append(item, ignore_index=True)

        
        #sensor_desc.ItemRange=sensor_desc.ItemRange.apply(lambda x: json.loads(x))
        
        return activity_events,activities,sensor_events,sensor_desc
        

