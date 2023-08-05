# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 22:07:01 2018

@author: yoelr
"""
from ._tank import MixTank
from ._hx import HXutility

class EnzymeTreatment(MixTank):
    """Create an EnzymeTreatment unit that is cost as a MixTank with a heat exchanger."""
    _N_outs = 1
    
    #: Residence time (hr)
    _tau = 1
    
    def __init__(self, ID='', ins=None, outs=(), *, T):
        super().__init__(ID, ins, outs)
        self.T = T #: Operating temperature
        self._heat_exchanger = he = HXutility(None, None, T=T) 
        self.heat_utilities = he.heat_utilities
        he._ins = self._ins
        he._outs = self._outs
    
    def _run(self):
        feed = self.ins[0]
        out = self.outs[0]
        out.mol[:] = self.mol_in
        out.phase = feed.phase
        out.P = feed.P
        out.T = self.T
        
    def _design(self):
        super()._design()
        self._heat_exchanger._design()
        
    def _cost(self):
        super()._cost()
        he = self._heat_exchanger
        he._cost()
        self.purchase_costs['Heat exchanger'] = he.purchase_costs['Heat exchanger'] 
    