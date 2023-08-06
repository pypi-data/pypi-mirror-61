"""

.. autoclass:: Peeler
   :members:

"""

import os
import json
from collections import OrderedDict, namedtuple
import time

import numpy as np
import scipy.signal


from .peeler_tools import _dtype_spike


from tqdm import tqdm

from .peeler_engine_classic import PeelerEngineClassic
from .peeler_engine_oldclassic import PeelerEngineOldClassic
from .peeler_engine_classic_cl import PeelerEngineClassicOpenCl
from .peeler_engine_testing import PeelerEngineTesting
from .peeler_engine_parallel import PeelerEngineParallel
from .peeler_engine_geometry import PeelerEngineGeometrical


#~ from .peeler_engine_strict import PeelerEngineStrict

peeler_engines = {
    'classic' : PeelerEngineClassic,
    # 'classic_opencl' : PeelerEngineClassicOpenCl,  ### not working
    'classic_old' : PeelerEngineOldClassic,
    'testing' : PeelerEngineTesting,
    # 'classic_parallel' : PeelerEngineParallel,    ### not working
    'geometrical' : PeelerEngineGeometrical,
    
}



class Peeler:
    """
    The peeler is core of spike sorting itself.
    It basically do a *template matching* on a signals.
    
    This class nedd a *catalogue* constructed by :class:`CatalogueConstructor`.
    Then the compting is applied chunk chunk on the raw signal itself.
    
    So this class is the same for both offline/online computing.
    
    At each chunk, the algo is basically this one:
      1. apply the processing chain (filter, normamlize, ....)
      2. Detect peaks
      3. Try to classify peak and detect the *jitter*
      4. With labeled peak create a prediction for the chunk
      5. Substract the prediction from the processed signals.
      6. Go back to **2** until there is no peak or only peaks that can't be labeled.
      7. return labeld spikes from this or previous chunk and the processed signals (for display or recoding)
    
    The main difficulty in the implemtation is to deal with edge because spikes 
    waveforms can spread out in between 2 chunk.
    
    Note that the global latency depend on this é paramters:
      * lostfront_chunksize
      * chunksize

    
    """
    def __init__(self, dataio):
        #for online dataio is None
        self.dataio = dataio

    def __repr__(self):
        t = "Peeler <id: {}> \n  workdir: {}\n".format(id(self), self.dataio.dirname)
        
        return t

    def change_params(self, catalogue=None, engine='classic', internal_dtype='float32', chunksize=1024, **params):
        assert catalogue is not None
        
        self.catalogue = catalogue
        self.internal_dtype = internal_dtype
        self.chunksize = chunksize
        self.engine_name = engine
        self.peeler_engine = peeler_engines[engine]()
        self.peeler_engine.change_params(catalogue=catalogue, internal_dtype=internal_dtype, chunksize=chunksize, **params)
    
    def process_one_chunk(self,  pos, sigs_chunk):
        return self.peeler_engine.process_one_chunk(pos, sigs_chunk)
    
    def initialize_online_loop(self, sample_rate=None, nb_channel=None, source_dtype=None):
        self.peeler_engine.initialize_before_each_segment(sample_rate=sample_rate, nb_channel=nb_channel, source_dtype=source_dtype, already_processed = False)
    
    def run_offline_loop_one_segment(self, seg_num=0, duration=None, progressbar=True):
        chan_grp = self.catalogue['chan_grp']

        if duration is not None:
            length = int(duration*self.dataio.sample_rate)
        else:
            length = self.dataio.get_segment_length(seg_num)
        
        # check if the desired length is already computed or not
        already_processed = self.dataio.already_processed(seg_num=seg_num, chan_grp=chan_grp, length=length)
        

        kargs = {}
        kargs['sample_rate'] = self.dataio.sample_rate
        kargs['nb_channel'] = self.dataio.nb_channel(chan_grp)
        if already_processed:
            kargs['source_dtype'] = self.internal_dtype
        else:
            kargs['source_dtype'] = self.dataio.source_dtype
        kargs['geometry'] = self.dataio.get_geometry(chan_grp)
        kargs['already_processed'] = already_processed
        self.peeler_engine.initialize_before_each_segment(**kargs)
        
        
        
        if already_processed:
            # ready from "processed'
            signal_type = 'processed'
        else:
            # read from "initial" 
            # activate signal processor
            signal_type = 'initial'
        
            #initialize engines
            self.dataio.reset_processed_signals(seg_num=seg_num, chan_grp=chan_grp, dtype=self.internal_dtype)
        
        self.dataio.reset_spikes(seg_num=seg_num, chan_grp=chan_grp, dtype=_dtype_spike)

        iterator = self.dataio.iter_over_chunk(seg_num=seg_num, chan_grp=chan_grp, chunksize=self.chunksize, 
                                                    i_stop=length, signal_type=signal_type)
        if progressbar:
            iterator = tqdm(iterable=iterator, total=length//self.chunksize)
        
        
        for pos, sigs_chunk in iterator:
            sig_index, preprocessed_chunk, total_spike, spikes = self.peeler_engine.process_one_chunk(pos, sigs_chunk)
            
            if sig_index<=0:
                continue
            
            if not already_processed:
                # save preprocessed_chunk to file
                self.dataio.set_signals_chunk(preprocessed_chunk, seg_num=seg_num,chan_grp=chan_grp,
                            i_start=sig_index-preprocessed_chunk.shape[0], i_stop=sig_index,
                            signal_type='processed')
            
            if spikes is not None and spikes.size>0:
                self.dataio.append_spikes(seg_num=seg_num, chan_grp=chan_grp, spikes=spikes)
        
        extra_spikes = self.peeler_engine.get_remaining_spikes()
        if extra_spikes is not None:
            
            if extra_spikes.size>0:
                self.dataio.append_spikes(seg_num=seg_num, chan_grp=chan_grp, spikes=extra_spikes)
        
        if not already_processed:
            self.dataio.flush_processed_signals(seg_num=seg_num, chan_grp=chan_grp, processed_length=int(sig_index))
            
        self.dataio.flush_spikes(seg_num=seg_num, chan_grp=chan_grp)

    def run(self, **kargs):
        assert hasattr(self, 'catalogue'), 'So peeler.change_params first'
        
        for seg_num in range(self.dataio.nb_segment):
            self.run_offline_loop_one_segment(seg_num=seg_num, **kargs)
    
    # old alias just in case
    run_offline_all_segment = run
        


    
