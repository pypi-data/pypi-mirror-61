# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:47:33 2018

This module includes classes and functions relating Stream objects.

@author: Yoel Cortes-Pena
"""
__all__ = ('MissingStream', 'Ins', 'Outs',
           'Sink', 'Source')

# # For later use in this module
# def missing_method(self, *args, **kwargs):
#     raise TypeError(f'Method not supported for {type(self).__name__} object.')


# %% Dummy Stream object

class MissingStreamType:
    """Create a MissingStream object that acts as a dummy in Ins and Outs objects until replaced by an actual Stream object."""
    _sink = None
    _source = None
    
    def __new__(cls):
        return MissingStream
    
    def __bool__(self):
        return False
    
    def __setattr__(self, key, value): pass
    
    def __getattr__(self, key):
        raise AttributeError(type(self).__name__)

    def __repr__(self):
        return f'MissingStream'
    
    def __str__(self):
        return 'missing stream'

MissingStream = object.__new__(MissingStreamType)


# %% List objects for input and output streams

class Ins(list):
    """Create a Ins object which serves as a list of input streams for a Unit object."""
    __slots__ = ('sink',)

    def __init__(self, sink, streams=()):
        self.sink = sink #: Unit object where Ins object is attached
        self._clear_sink(sink)
        super().__init__(streams)
        self._fix_sink(sink)
    
    def pop(self, index):
        s = super().pop(index)
        s._sink = None
        return s
    
    def insert(self, index, stream):
        super().insert(index, stream)
        stream._sink = self.sink
    
    def remove(self, stream):
        super().remove(stream)
        stream._sink = None
    
    def _clear_sink(self, sink):
        """Remove sink from streams."""
        for s in self:
            if s._sink is sink: s._sink = None
    
    def _fix_sink(self, sink):
        """Set sink for all streams."""
        for s in self: s._sink = sink
    
    def __setitem__(self, index, stream):
        sink = self.sink
        if isinstance(index, int):
            s_old = self[index]
            if s_old._sink is sink: s_old._sink = None
            stream._sink = sink
            super().__setitem__(index, stream)
        elif isinstance(index, slice):
            self._clear_sink(sink)
            super().__setitem__(index, stream)
            self._fix_sink(sink)
        else:
            raise TypeError(f'Only intergers and slices are valid indices for {type(self).__name__} objects')
           
    def clear(self):
        self._clear_sink(self.sink)
        super().clear()
    
    def extend(self, iterable):
        sink = self.sink
        # Add sink to new streams
        for s in iterable: s._sink = sink
        super().extend(iterable)
        
    def append(self, stream):
        sink = self.sink
        # Add sink to new stream
        stream._sink = sink
        super().append(stream)
    

class Outs(list):
    """Create a Outs object which serves as a list of output streams for a Unit object."""
    __slots__ = ('source',)
    
    def __init__(self, source, streams=()):
        self.source = source #: Unit object where Outs object is attached
        self._clear_source(source)
        super().__init__(streams)
        self._fix_source(source)
            
    def pop(self, index):
        s = super().pop(index)
        s._source = None
        return s
    
    def insert(self, index, stream):
        super().insert(index, stream)
        stream._source = self.source
    
    def remove(self, stream):
        stream._source = None
        super().remove(stream)    
    
    def _clear_source(self, source):
        """Remove source from streams."""
        for s in self:
            if s._source is source: s._source = None
    
    def _fix_source(self, source):
        """Set source for all streams."""
        for s in self: s._source = source
            
    def __setitem__(self, index, stream):
        source = self.source
        if isinstance(index, int):
            s_old = self[index]
            if s_old._source is source: s_old._source = None
            super().__setitem__(index, stream)
            stream._source = source
        elif isinstance(index, slice):
            self._clear_source(source)
            super().__setitem__(index, stream)
            self._fix_source(source)
        else:
            raise TypeError(f'Only intergers and slices are valid indices for {type(self).__name__} objects')
        
    def clear(self):
        self._clear_source(self.source)
        super().clear()
    
    def extend(self, iterable):
        source = self.source
        # Add source to new streams
        for s in iterable: s._source = source
        super().extend(iterable)
        
    def append(self, stream):
        source = self.source
        # Add sink to new stream
        stream._source = source
        super().append(stream)


# %% Sink and Source object for piping notation

class Sink:
    """Create a Sink object that connects a stream to a unit using piping notation:
    
    Parameters
    ----------
    stream : Stream
    index : int
        
    Examples
    --------
    First create a stream and a Mixer:
    
    .. code-block:: python
    
        >>> stream = Stream('s1')
        >>> unit = Mixer('M1')
    
    Sink objects are created using -pipe- notation:
        
    .. code-block:: python
    
        >>> stream-1
        <Sink: s1-1>
    
    Use pipe notation to create a sink and connect the stream:
    
    .. code-block:: python
    
        >>> stream-1-unit
        >>> M1.show()
        
        Mixer: M1
        ins...
        [0] Missing stream
        [1] s1
            phase: 'l', T: 298.15 K, P: 101325 Pa
            flow:  0
        outs...
        [0] d27
            phase: 'l', T: 298.15 K, P: 101325 Pa
            flow:  0
    
    """
    __slots__ = ('stream', 'index')
    def __init__(self, stream, index):
        self.stream = stream
        self.index = index

    # Forward pipping
    def __sub__(self, unit):
        unit.ins[self.index] = self.stream
        return unit
    
    # Backward pipping
    __pow__ = __sub__
    
    def __repr__(self):
        return '<' + type(self).__name__ + ': ' + self.stream.ID + '-' + str(self.index) + '>'


class Source:
    """Create a Source object that connects a stream to a unit using piping notation:
    
    Parameters
    ----------
    stream : Stream
    index : int
    
    Examples
    --------
    First create a stream and a Mixer:
    
    .. code-block:: python
    
        >>> stream = Stream('s1')
        >>> unit = Mixer('M1')
    
    Source objects are created using -pipe- notation:
        
    .. code-block:: python
    
        >>> 1**stream
        <Source: 1-s1>
    
    Use -pipe- notation to create a source and connect the stream:
    
    .. code-block:: python
    
        >>> unit**0**stream
        >>> M1.show()
        
        Mixer: M1
        ins...
        [0] Missing stream
        [1] Missing stream
        outs...
        [0] s1
            phase: 'l', T: 298.15 K, P: 101325 Pa
            flow:  0
    
    """
    __slots__ = ('stream', 'index')
    def __init__(self, stream, index):
        self.stream = stream
        self.index = index

    # Forward pipping
    def __rsub__(self, unit):
        unit.outs[self.index] = self.stream
        return unit
    
    # Backward pipping
    __rpow__ = __rsub__
    
    def __repr__(self):
        return '<' + type(self).__name__ + ': ' + str(self.index) + '-' + self.stream.ID + '>'




