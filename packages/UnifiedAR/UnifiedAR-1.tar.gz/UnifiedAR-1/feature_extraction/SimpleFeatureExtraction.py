from feature_extraction.feature_abstract import FeatureExtraction
import numpy as np
class SimpleFeatureExtraction(FeatureExtraction):
    def featureExtract(self,win):
        window=win['window']
        f=np.zeros(sum(1 for x in self.datasetdscr.sensor_id_map))  
        for i in range(0,window.shape[0]):
            f[self.datasetdscr.sensor_id_map_inverse[window.iat[i,0]]]=1   #f[sensor_id_map_inverse[x.SID]]=1
        return f

    def featureExtract2(self,s_event_list,idx):
        window=s_event_list
        f=np.zeros(sum(1 for x in self.datasetdscr.sensor_id_map))  
        for i in range(0,len(idx)):
            f[self.datasetdscr.sensor_id_map_inverse[window[idx[i],0]]]=1   #f[sensor_id_map_inverse[x.SID]]=1
        return f
        