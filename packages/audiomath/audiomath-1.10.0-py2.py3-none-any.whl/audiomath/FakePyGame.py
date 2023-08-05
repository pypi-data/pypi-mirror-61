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

"""
This submodule is not imported by default. If imported
explicitly, it provides a duck-typed partial clone of the
`pygame.mixer.Sound` object.

If you say::

    from audiomath.FakePyGame import mixer, Sound

then the interface is similar to what you get from saying::

    from pygame import mixer; from pygame.mixer import Sound

`mixer.init()` is a necessary call for pygame, but in
FakePyGame it simply does nothing.  Our `Player` objects
become known as Sound (not to be confused with our `Sound`
class), and they gain methods with pygame-like names such
as `get_length()` or`set_volume()`.
"""

__all__ = [
	'mixer', 'Sound',
]

from . import BackEnd as _BackEnd
_impl = _BackEnd.Load()

class Sound( _impl.Player ):
	def play( self, loops=0, maxtime=0, fade_ms=0 ): self.Play() # TODO: support args
	def stop( self ): self.Pause()
	#def fadeout( self, msec ): pass # TODO: stops after fading out over specified time
	def set_volume( self, vol ): self.volume = vol
	def get_volume( self ): return self.volume
	#def get_num_channels( self ): pass # TODO - number of concurrently playing instances of this sound, probably cannot implement any equivalent
	def get_length( self ): return self.sound.Duration()

def init():
	pass

class mixer( object ):
	init = init
	Sound = Sound
