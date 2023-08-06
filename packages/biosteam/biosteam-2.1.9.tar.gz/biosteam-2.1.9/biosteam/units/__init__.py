#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 20:39:46 2018

@author: Yoel Rene Cortes-Pena
"""
from . import _flash
from . import _liquids_centrifuge
from .._graphics import Graphics
from ._mixer import Mixer
from ._splitter import Splitter, InvSplitter
from ._pump import Pump
from ._hx import HXutility, HXprocess
from ._flash import *
from ._flash import Flash
from ._multi_effect_evaporator import MultiEffectEvaporator
from ._liquids_centrifuge import *
from ._distillation import Distillation
from ._tank import Tank, StorageTank, MixTank
from ._transesterification import Transesterification
from ._fermentation import Fermentation
from ._enzyme_treatment import EnzymeTreatment
from ._clarifier import Clarifier
from ._solids_centrifuge import SolidsCentrifuge
from ._crushing_mill import CrushingMill
from ._rvf import RVF
from ._molecular_sieve import MolecularSieve
from ._balance import MassBalance
from ._conveying_belt import ConveyingBelt
from ._shredder import Shredder
from ._magnetic_separator import MagneticSeparator
from ._screw_feeder import ScrewFeeder
from ._vibrating_screen import VibratingScreen
from ._junction import Junction
from ._solids_separator import SolidsSeparator
from ._vent_scrubber import VentScrubber

# %% All units

__all__ = ['Mixer', 'Splitter', 'InvSplitter', 'MixTank', 'StorageTank', 'HXutility', 'HXprocess', 'Pump', 'Distillation', 'Transesterification', 'Fermentation', 'MultiEffectEvaporator', 'EnzymeTreatment', 'CrushingMill', 'RVF', 'MolecularSieve', 'SolidsCentrifuge', 'Clarifier', 'MassBalance', 'ConveyingBelt', 'Shredder', 'MagneticSeparator', 'ScrewFeeder', 'VibratingScreen', 'Junction', 'SolidsSeparator', 'VentScrubber']
__all__.extend(_flash.__all__)
__all__.extend(_liquids_centrifuge.__all__)

from lazypkg import LazyPkg
LazyPkg(__name__, ['decorators', 'design_tools', 'facilities'])


# %% Enhance Graphics

# Mixer
_mixgraphics = Mixer._graphics
_mixgraphics.edge_in = _mixgraphics.edge_in * 3
_mixgraphics.edge_out = _mixgraphics.edge_out * 3

# MixTank
_mixgraphics = MixTank._graphics
_mixgraphics.edge_in = _mixgraphics.edge_in * 3
_mixgraphics.edge_out = _mixgraphics.edge_out * 3

# Flash
edge_out = Flash._graphics.edge_out
edge_out[0]['tailport'] = 'n'
edge_out[1]['tailport'] = 's'
node = Flash._graphics.node
node['width'] = '1'
node['height'] = '1.1'

# Distillation
edge_out = Distillation._graphics.edge_out
edge_out[0]['tailport'] = 'n'
edge_out[1]['tailport'] = 's'
node = Distillation._graphics.node
node['width'] = '1'
node['height'] = '1.2'

# Single stream heat exchanger
HXutility._graphics = graphics = Graphics()
graphics.node['shape'] = 'circle'
graphics.node['color'] = 'none'
graphics.node['margin'] = '0'

def HXutility_node(hx):
    try:
        si = hx.ins[0]
        so = hx.outs[0]
        H_in = si.H
        H_out = so.H
        graphics = hx._graphics
        if H_in > H_out:
            graphics.node['fillcolor'] = '#cfecf0'
            graphics.node['gradientangle'] = '0'
            name = 'Cooling'
        elif H_in < H_out:
            graphics.node['gradientangle'] = '0'
            graphics.node['fillcolor'] = '#fad6d8'
            name = 'Heating'
        else:
            graphics.node['gradientangle'] = '90'
            graphics.node['fillcolor'] = '#cfecf0:#fad6d8'
            name = 'Heat exchanger'
    except:
        graphics = hx._graphics
        name = 'Heat exchange'
    return name

graphics.node_function = HXutility_node

# Double stream heat exchanger
HXprocess._graphics = graphics = Graphics()
graphics.name = 'HXprocess'
graphics.node['shape'] = 'circle'
graphics.node['color'] = 'none'
graphics.node['margin'] = '0'
graphics.node['gradientangle'] = '90'
graphics.node['fillcolor'] = '#cfecf0:#fad6d8'

# Mixer
Mixer._graphics.node['shape'] = 'triangle'
Mixer._graphics.node['orientation'] = '270'
Mixer._graphics.edge_out[0]['tailport'] = 'e'

# Splitter
Splitter._graphics.node['shape'] = 'triangle'
Splitter._graphics.node['orientation'] = '90'
Splitter._graphics.node['fillcolor'] = "#bfbfbf:white"
Splitter._graphics.edge_in[0]['headport'] = 'w'

# Balance
graphics = MassBalance._graphics
graphics.node['shape'] = 'note'
graphics.node['fillcolor'] = '#F0F0F0'
graphics.in_system = False

del HXutility_node, graphics, edge_out, node, Graphics