# $BEGIN_AUDIOMATH_LICENSE$
# 
# This file is part of the audiomath project, a Python package for
# recording, manipulating and playing sound files.
# 
# Copyright (c) 2008-2020 Jeremy Hill
# 
# audiomath is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/ .
# 
# The audiomath distribution includes binaries from the third-party
# AVbin and PortAudio projects, released under their own licenses.
# See the respective copyright, licensing and disclaimer information
# for these projects in the subdirectories `audiomath/_wrap_avbin`
# and `audiomath/_wrap_portaudio` . It also includes a fork of the
# third-party Python package `pycaw`, released under its original
# license (see `audiomath/pycaw_fork.py`).
# 
# $END_AUDIOMATH_LICENSE$

__all__ = [
	
]

from . import Base; from .Base import Sound, ACROSS_CHANNELS
from . import DependencyManagement; from .DependencyManagement import Require
librosa = Require( 'librosa' )

#from audiomath import Sound, ACROSS_CHANNELS
#try: import librosa
#except ImportError: raise ImportError( "the third-party package 'librosa' is needed for this functionality" )

def TimeStretch( s, speed=2, **kwargs ):
	s.y = s[ :0, :0 ].Stack( librosa.effects.time_stretch( si.y.ravel(), rate=speed, **kwargs ) for si in s.SplitChannels() ).y
	return s
Sound.TimeStretch = TimeStretch
	
def PitchShift( s, semitones, **kwargs ):
	sub = [ slice( None ), slice( None ) ]
	for sub[ ACROSS_CHANNELS ] in range( s.NumberOfChannels() ):
		tsub = tuple( sub )
		s.y[ tsub ] = librosa.effects.pitch_shift( s.y[ tsub ], sr=s.fs, n_steps=semitones, **kwargs )
	return s
Sound.PitchShift = PitchShift
