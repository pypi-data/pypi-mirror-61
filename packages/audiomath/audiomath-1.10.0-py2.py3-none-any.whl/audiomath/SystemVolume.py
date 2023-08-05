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
Utilities for manipulating the operating-system master volume
and/or mixer.

- On Windows, this requires the third-party packages
  `comtypes` and `psutil` (via our fork of Andre Miras' `pycaw`,
  which is included).
  
- On macOS, it uses Applescript.

- On Linux, there is a highly-experimental implementation based
  on `pacmd` and `pactl` (so these PulseAudio command-line
  utilities must be installed).
  
Because of its dependencies, this submodule is not imported
by default---you must explicitly `import audiomath.SystemVolume`.

The recommended way to use this module is via the `SystemVolumeSetting`
context-manager object::

    import audiomath
    from audiomath.SystemVolume import SystemVolumeSetting
    p = audiomath.Player(audiomath.TestSound())
    with SystemVolumeSetting(0.1, mute=False):
        p.Play(wait=True)

"""

__all__ = [
	'GetVolume',
	'SetVolume',
	'SystemVolumeSetting',
	'MAX_VOLUME',
	'GetAllSessions',
]

import os
import re
import sys
import ast
import math
import copy
import subprocess

GetVolume = None
SetVolume = None
def GetAllSessions(): raise NotImplementedError( 'this functionality is only available on Windows' )

if sys.platform.lower().startswith( 'win' ):
	GetAllSessions = None
	try:
		from . import pycaw_fork; from .pycaw_fork import GetMasterVolumeController, AudioUtilities
	except ImportError as err:
		print( 'could not create master volume controller: ' + str( err ) )
	else:
		GetAllSessions = AudioUtilities.GetAllSessions
		def GetVolume( dB=False, session='master' ):
			"""
			Query volume level and mute settings.
			
			If you want to query volume settings, change them,
			and later change them back, `SystemVolumeSettings`
			is a more usable option.
			"""
			return SetVolume( dB=dB, session=session )
		def SetVolume( level=None, dB=False, mute=None, session='master' ):
			"""
			Sets volume level and/or mute status.
			
			Consider using the context-manager class
			`SystemVolumeSetting` instead.  For a description
			of the input arguments, see `SystemVolumeSetting`.
			"""
			context = None
			dB = bool( dB )
			if level is not None:
				if dB: level = 10 ** level / 10.0
				level = max( 0.0, min( 1.0, float( level ) ) )
			change = ( level is not None or mute is not None )
			if isinstance( session, str ) and session.lower() in [ 'master', 'master volume' ]:
				controller = GetMasterVolumeController()
				if change: previousLevel = controller.GetMasterVolumeLevelScalar()
				if change: previousMute = bool( controller.GetMute() )
				if level is not None:
					for iChannel in range( controller.GetChannelCount() ):
						controller.SetChannelVolumeLevelScalar( iChannel, level, context )
				level = controller.GetMasterVolumeLevelScalar()
				if mute is not None:
					controller.SetMute( bool( mute ), context )
				mute = bool( controller.GetMute() )
			else:
				sessions = GetAllSessions()
				if isinstance( session, int ):
					match = [ x for x in sessions if x.ProcessId == session ]
					if not match: raise ValueError( 'could not find an audio "session" with .ProcessId=%r' % session )
					session = match[ 0 ]
				elif isinstance( session, str ):
					key = session.lower()
					return [
						SetVolume( level=level, dB=dB, mute=mute, session=x )
						for x in sessions
						if key == '*' or x.DisplayName.lower() == key or ( x.Process and x.Process.name().lower() == key )
					]
				controller = session.SimpleAudioVolume
				if change: previousLevel = controller.GetMasterVolume()
				if change: previousMute = bool( controller.GetMute() )
				if level is not None: controller.SetMasterVolume( level, context )
				level = controller.GetMasterVolume()
				if mute is not None: controller.SetMute( bool( mute ), context )
				mute = bool( controller.GetMute() )
				session = session.ProcessId
			if dB:
				level = 10 * math.log10( level )
				if change: previousLevel = 10 * math.log10( previousLevel )
			result = dict( level=level, dB=dB, mute=mute, session=session )
			if change: result.update( dict( previousLevel=previousLevel, previousMute=previousMute ) )
			return result
elif sys.platform.lower().startswith( 'darwin' ):
	def RunApplescript( applescript ):
		sp = subprocess.Popen( [ 'osascript' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False )
		out, err = [ x if isinstance( x, str ) else x.decode( 'ascii', errors='ignore' ) for x in sp.communicate( applescript.encode( 'utf-8' ) ) ]
		if err or sp.returncode: raise OSError( 'Applescript returned error code ' + str( sp.returncode ) + ( ': ' if err else '' ) + err  )
		try: result = ast.literal_eval( out )
		except Exception as err: raise OSError( 'Applescript output could not be interpreted with ast.literal_eval(%r)' % out )
		if 'error' in result: raise OSError( result[ 'error' ] )
		return result
	def GetVolume( dB=False, session='master' ):
		"""
		Query volume level and mute settings.
		
		If you want to query volume settings, change them,
		and later change them back, `SystemVolumeSettings`
		is a more usable option.
		"""
		return SetVolume( dB=dB, session=session )
	def SetVolume( level=None, dB=False, mute=None, session='master' ):
		"""
		Sets volume level and/or mute status.
		
		Consider using the context-manager class
		`SystemVolumeSetting` instead.  For a description
		of the input arguments, see `SystemVolumeSetting`.
		"""
		dB = bool( dB )
		if level is not None:
			if dB: level = 10 ** level / 10.0
			level = max( 0.0, min( 1.0, float( level ) ) )
		if not isinstance( session, str ) or session.lower() not in [ 'master', 'master volume' ]:
			raise ValueError( "on macOS the only supported session value is session='master'" )
		change = ( level is not None or mute is not None )
		result = RunApplescript("""
set level to {level}
set mute to "{mute}"

set VolumeSettings to ( get volume settings )
set previousLevel to ( output volume of VolumeSettings )
set previousMute to "False"
if ( output muted of VolumeSettings ) then set previousMute to "True"

if( level >= 0 ) then set volume   output volume   level  -- what a triumph of natural-language readability

if( mute = "None" ) then set mute to previousMute
if ( mute = "True" ) then
	set volume with output muted
else
	set volume without output muted
end if

set VolumeSettings to ( get volume settings )
set level to ( output volume of VolumeSettings )
set mute to "False"
if ( output muted of VolumeSettings ) then set mute to "True"

return "{{\
  'level': " & level / 100.0 & ", \
  'dB': False, \
  'mute': "  & mute & ", \
  'session': 'master', \
  'previousLevel': " & previousLevel / 100.0 & ", \
  'previousMute': "  & previousMute  & ", \
}}"
		""".format(
			level = ( -1 if level is None else int( round( 100 * level ) ) ),
			mute  = ( None if mute is None else bool( mute ) ),
		) )
		if dB:
			result[ 'dB' ] = True
			result[ 'level' ] = 10 * math.log10( result[ 'level' ] )
			result[ 'previousLevel' ] = 10 * math.log10( result[ 'previousLevel' ] )
		if not change: del result[ 'previousLevel' ], result[ 'previousMute' ]
		return result
elif sys.platform.lower().startswith( 'linux' ):
	from . import Meta; from .Meta import Bang
	
	def _FirstMatch( output, pattern, flags=re.I ):
		matches = [ match for line in output.split( '\n' ) for match in [ re.match( pattern, line.strip(), flags ) ] if match ]
		if not matches: raise OSError( "no matches for r'%s' in command output" % pattern )
		return matches[ 0 ]
	def _GetMute( output ):
		mute = _FirstMatch( output, r'muted:\s*(?P<result>.+)' ).group( 'result' )
		return { 'yes' : True, 'no' : False }.get( mute.lower() )
	def _GetLevel( output ):
		volumes = _FirstMatch( output, r'volume:\s*(?P<result>.+)' ).group( 'result' )
		volumes = [ float( x.rstrip( '%' ) ) / 100.0 for x in re.findall( r'\b[\.0-9]+\%', volumes ) ]
		base_volume = _FirstMatch( output, r'base volume:\s*(?P<result>.+)' ).group( 'result' )
		base_volume = [ float( x.rstrip( '%' ) ) / 100.0 for x in re.findall( r'\b[\.0-9]+\%', base_volume ) ]
		return base_volume[ 0 ] * sum( volumes ) / len( volumes )
		
	def GetVolume( dB=False, session='master' ):
		"""
		Query volume level and mute settings.
		
		If you want to query volume settings, change them,
		and later change them back, `SystemVolumeSettings`
		is a more usable option.
		
		The Linux implementation uses Pulse Audio utility
		`pacmd`.  It is likely to break whenever the text
		format of `pacmd list-sinks` changes in future
		versions.
		"""
		return SetVolume( dB=dB, session=session )
	def SetVolume( level=None, dB=False, mute=None, session='master' ):
		"""
		Sets volume level and/or mute status.
		
		Consider using the context-manager class
		`SystemVolumeSetting` instead.  For a description
		of the input arguments, see `SystemVolumeSetting`.
		
		The Linux implementation uses Pulse Audio utilities
		`pacmd` and `pactl`.  It is likely to break whenever
		the text format of `pacmd list-sinks` changes in
		future versions.
		"""
		dB = bool( dB )
		if level is not None:
			if dB: level = 10 ** level / 10.0
			level = max( 0.0, min( 1.0, float( level ) ) )
		if not isinstance( session, str ) or session.lower() not in [ 'master', 'master volume' ]:
			raise ValueError( "on Linux the only supported session value is session='master'" )
		change = ( level is not None or mute is not None )
		previousLevel = previousMute = 1.0
		if change:
			_, details, _ = Bang( 'pacmd list-sinks', raiseException=True )
			previousLevel = _GetLevel( details )
			previousMute = _GetMute( details )
		if level is not None: Bang( 'pactl set-sink-volume @DEFAULT_SINK@ %d%%' % round( 100.0 * level ), raiseException=True )
		if mute is not None: Bang( 'pactl set-sink-mute @DEFAULT_SINK@ %d' % bool( mute ), raiseException=True )
		_, details, _ = Bang( 'pacmd list-sinks', raiseException=True )
		level = _GetLevel( details )
		mute = _GetMute( details )
		result = dict( level=level, mute=mute, dB=False, previousLevel=previousLevel, previousMute=previousMute )
		if dB:
			result[ 'dB' ] = True
			result[ 'level' ] = 10 * math.log10( result[ 'level' ] )
			result[ 'previousLevel' ] = 10 * math.log10( result[ 'previousLevel' ] )
		if not change: del result[ 'previousLevel' ], result[ 'previousMute' ]
		return result

else:
	print( 'Global SetVolume() and GetVolume() are not implemented on %s' % sys.platform )

class SystemVolumeSetting( object ):
	"""
	This class is a context-manager. It allows you to change
	the system volume temporarily, such that it automatically
	changes back to its previous setting when you are done::
	
	    import audiomath
	    from audiomath.SystemVolume import SystemVolumeSetting
	    p = audiomath.Player( audiomath.TestSound() )
	    with SystemVolumeSetting(0.1, mute=False):
	        p.Play( wait=True )
	        
	        # NB: `wait=True` is necessary for the purposes of 
	        # this simple example---with `wait=False`, control
	        # would exit the `with` clause before any sound 
	        # samples are actually streamed and you would not 
	        # hear the difference

	For your convenience, `MAX_VOLUME` is a ready-instantiated
	`SystemVolumeSetting` made with `level=1.0` and `mute=False`::
	
	    from audiomath.SystemVolume import MAX_VOLUME
	    with MAX_VOLUME:
	        p.Play( wait=True )
	
	`SystemVolumeSetting` instances can be combined together
	with the `&` operator. This is only really useful on Windows
	where session-by-session control is possible::
	
	    MUTE_FIREFOX = SystemVolumeSetting(mute=True, session='Mozilla Firefox')
	    with MAX_VOLUME & MUTE_FIREFOX:
	        p.Play( wait=True )
	
	"""
	def __init__( self, level=None, dB=False, mute=None, session='master', verbose=False ):
		"""
		Args:
			level (float, None):
				volume setting, from 0.0 to 1.0 (assuming `dB=False`)
				or from negative infinity to 0.0 (with `dB=True`).
				Use `None` if you want to leave the level untouched
				and manipulate only the `mute` setting.
			dB (bool):
				By default, `level` values are interpreted and
				expressed as relative power values from 0 to 1.
				However, with `dB=True` you can choose to have
				them interpreted and expressed in decibels,
				i.e. `10*log10(power)`, with 0.0 as the maximum.
			mute (bool, None):
				Whether or not to mute the output. Use `None` to
				leave the mute setting untouched and manipulate
				only the `level`.
			session (str, int):
				(Windows only): control one individual "session"
				within the Windows mixer.  A string will match
				all sessions with the specified `.DisplayName`
				or `.Process.name()`.  An integer will match
				only the audio session with the specified
				`.ProcessId`. A list of sessions instances can
				be retrieved by `GetAllSessions()`.
		"""
		if isinstance( level, SystemVolumeSetting ):
			self.__dict__.update( copy.deepcopy( level.__dict__ ) )
		else:
			self.args = [ dict( level=level, dB=dB, mute=mute, session=session ) ]
			self.state = []
			self.verbose = verbose
		
	def copy( self ):
		return self.__class__( self )
		
	def __enter__( self ):
		if not self.state:
			if SetVolume:
				for args in self.args:
					state = SetVolume( **args )
					if not isinstance( state, list ): state = [ state ]
					for s in state:
						if self.verbose: print( 'setting %r' % s )
					self.state += state
			else:
				print( 'could not manipulate system volume: no %s.SetVolume implementation' % __name__ )
		return self
	def __exit__( self, *blx ):
		while self.state:
			args = self.state.pop( -1 )
			args[ 'level' ] = args.pop( 'previousLevel', args[ 'level' ] )
			args[ 'mute'  ] = args.pop( 'previousMute',  args[ 'mute'  ] )
			if self.verbose: print( 'reverting to %r' % args )
			SetVolume( **args )
	
	def __add__( self, other ): return self.copy().__iadd__( other )
	def __and__( self, other ): return self.copy().__iand__( other )
	def __iadd__( self, other ): self.args += other.copy().args; return self
	__iand__ = __iadd__
	
MAX_VOLUME = SystemVolumeSetting( level=1.0, mute=False )
