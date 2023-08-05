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
	'NotInstalled',  # ffmpeg.NotInstalled and sox.NotInstalled are subclasses of this
	'ffmpeg', 'sox',
]

import os
import re
import sys
import time
import wave
import glob
import shlex
import struct
import shutil
import tempfile
import threading
import subprocess

from . import Base;  from .Base import Sound, Silence, ACROSS_SAMPLES
from . import Meta; from .Meta import FindFile, PackagePath
from . import Dependencies; from .Dependencies import numpy

def EndianSwap( s, nbytes ):
	if   nbytes == 1 or sys.byteorder == 'little': return s
	elif nbytes == 2: fmt = 'H'
	elif nbytes == 4: fmt = 'L'
	else: raise ValueError( "failed to swap endianness for %d-byte values" % nbytes )
	fmt = str( int( len(s) / nbytes ) ) + fmt
	return struct.pack( '<' + fmt, *struct.unpack( '>' + fmt, s ) )

def ReadWav(self, filename):
	wf = wave.open( filename, 'rb' )
	nbytes = wf.getsampwidth()
	nChannels = wf.getnchannels()
	nSamples = wf.getnframes()
	fs = wf.getframerate()
	comptype = ( wf.getcomptype(), wf.getcompname() )
	strdat = wf.readframes( nSamples )
	wf.close()
	strdat = EndianSwap( strdat, nbytes )
	self.bits = nbytes * 8
	self.fs = fs
	self.filename = os.path.realpath( filename )
	self.compression = comptype
	self.y = self.str2dat( strdat, nSamples, nChannels )
	if strdat != self.dat2str():
		print( "warning: data mismatch in %s" % self._short_repr() )
	return self

def WriteWav( self, filename=None, headerOnly=False ):
	"""
	Write the sound waveform in uncompressed `'.wav'`
	format, to the specified `filename`.  If `filename`
	is unspecified, `self.filename` is used, if present.
	"""
	if filename is None: filename = self.filename
	if filename is None: raise TypeError( 'no filename supplied' )
	wf = wave.open( filename, 'wb' )
	wf.setsampwidth( self.nbytes )
	wf.setnchannels( self.NumberOfChannels() )
	#wf.setnframes( self.NumberOfSamples() )
	wf.setframerate( self.fs )
	wf.setcomptype( *self.compression )
	if headerOnly:
		self._wavFileHandleOpenForWriting = wf
	else:
		s = self.dat2str()
		s = EndianSwap( s, self.nbytes )
		wf.writeframes( s )
		wf.close()
	if not isinstance( filename, str ):
		try: filename = filename.name
		except: pass
	self.filename = os.path.realpath( filename ) if isinstance( filename, str ) else None
	return self

def AppendWavFrames( self, data ):
	# h = am.Recorder(10, start=0)
	# def hook( data, *blx ): href().Set( head=0 ).sound.Append( data ) 
	# import weakref; href = weakref.ref( h ); h.sound.Write('blah.wav', headerOnly=1); h.hook = hook; h.Record() 
	# h.Stop(); h.hook = None; h.sound._wavFileHandleOpenForWriting.close()
	wf = self._wavFileHandleOpenForWriting
	if not wf: raise ValueError( 'no wav file open for appending' )
	wf.writeframes( EndianSwap( self.dat2str( data ), self.nbytes ) )

def AppendRaw( self, data, fileHandle, translateNumericType=False, ensureLittleEndian=False ):
	nbytes = None
	if translateNumericType:
		data = self.dat2str( data )
		nbytes = self.nbytes
	elif hasattr( data, 'tostring' ):
		data = data.tostring()
		nbytes = data.dtype.itemsize
	if ensureLittleEndian and nbytes:
		data = EndianSwap( data, nbytes )
	fileHandle.write( data )

avbin = None
def Load_AVBin( tolerateFailure=False ):
	global avbin
	if avbin: return avbin
		
	from . import _wrap_avbin as avbin # nowadays, this will simply throw an exception if it fails
	if avbin: return avbin
	
	# ...but here's the old logic, just in case we every want to reinstate the pyglet-based fallback
	if 'pyglet' not in sys.modules: os.environ[ 'PYGLET_SHADOW_WINDOW' ] = '0'
	try: import pyglet.media.sources.avbin as avbin
	except: pass
	if avbin: return avbin
	try: import pyglet.media.avbin as avbin
	except: pass
	if avbin: return avbin
		
	if avbin: print( 'failed to import _wrap_avbin submodule - falling back on pyglet' )
	elif not tolerateFailure: raise ImportError( 'failed to import avbin either from _wrap_avbin or pyglet (is pyglet installed?)' )
	return avbin
	
def Read_AVBin( self, filename, duration=None, verbose=False ):
	if not avbin: Load_AVBin()
	sourceHandle = avbin.AVbinSource( filename )
	audioFormat = sourceHandle.audio_format
	if not audioFormat: # this can happen with .ogg files written by older libraries
		raise IOError( 'failed to interpret audio format details from %s' % filename )
	self.bits = audioFormat.sample_size
	self.fs = int( audioFormat.sample_rate )
	numberOfChannels = int( audioFormat.channels )
	bytesPerSample = int( audioFormat.bytes_per_sample )
	if duration is None: duration = sourceHandle.duration
	else: duration = min( duration, sourceHandle.duration )
	totalNumberOfSamples = int( round( duration * self.fs ) )
	cumulativeNumberOfSamples = 0
	self.filename = os.path.realpath( filename )
	subsDst = [ slice( None ), slice( None ) ]
	subsSrc = [ slice( None ), slice( None ) ]
	if verbose: print( 'reserving space for %g sec: %d channels, %d samples @ %g Hz = %g MB' % ( duration, numberOfChannels, totalNumberOfSamples, self.fs, totalNumberOfSamples * numberOfChannels * 4 / 1024 ** 2.0 ) )
	y = Silence( totalNumberOfSamples, numberOfChannels, 'float32' )
	t0 = 0.0
	while cumulativeNumberOfSamples < totalNumberOfSamples:
		if verbose:
			t = time.time()
			if not t0 or t > t0 + 0.5: t0 = t; print( '    read %.1f%%' % ( 100.0 * cumulativeNumberOfSamples / float( totalNumberOfSamples ) ) )
		dataPacket = sourceHandle.get_audio_data( 4096 )
		if dataPacket is None: break
		numberOfSamplesThisPacket = int( dataPacket.length / bytesPerSample )
		subsDst[ ACROSS_SAMPLES ] = slice( cumulativeNumberOfSamples, cumulativeNumberOfSamples + numberOfSamplesThisPacket )
		subsSrc[ ACROSS_SAMPLES ] = slice( 0, min( numberOfSamplesThisPacket,  totalNumberOfSamples - cumulativeNumberOfSamples ) )
		cumulativeNumberOfSamples += numberOfSamplesThisPacket
		data = self.str2dat( dataPacket.data, numberOfSamplesThisPacket, numberOfChannels )
		y[ tuple( subsDst ) ] = data[ tuple( subsSrc ) ]
	self.y = y
	return self
		
def Read( self, source, raw_dtype=None ):
	"""
	Args:
		source:
			A filename, or a byte string containing raw audio data.
			With filenames, files are decoded according to their file extension,
			unless the `raw_dtype` argument is explicitly specified, in which case files
			are assumed to contain raw data without header, regardless of extension.
			
		raw_dtype (str):
			If supplied, `source` is interpreted either as raw audio data, or
			as the name of a file *containing* raw audio data without a header.
			If `source` is a byte string containing raw audio data, and `raw_dtype` is
			unspecified, `raw_dtype` will default to `self.dtype_encoded`.
			Examples might be `float32` or even `float32*2`---the latter explicitly
			overrides the current value of `self.NumberOfChannels()` and interprets the
			raw data as 2-channel.
			
	"""
	isFileName = False
	for i in range( 32 ):
		try: nonprint = chr( i ) in source
		except: break
		if nonprint: break
	else:
		isFileName = True
	if isFileName:
		resolvedFileName = FindFile( source )
		source = resolvedFileName if resolvedFileName else os.path.realpath( source )
	isExistingFile = isFileName and os.path.isfile( source )
	if isFileName and not isExistingFile: raise IOError( 'could not find file %s' % source )
	
	if not isExistingFile or raw_dtype:
		if isExistingFile:
			self.filename = os.path.realpath( source )
			source = open( source, 'rb' )
		else:
			self.filename = ''
		if hasattr( source, 'read' ): source = source.read()
		nChannels = None # default is self.NumberOfChannels()
		if not isinstance( raw_dtype, str ):
			raw_dtype = None  # default will be self.dtype_encoded
		elif '*' in raw_dtype:
			raw_dtype, count = raw_dtype.split( '*', 1 )
			if count: nChannels = int( count )
		self.y = self.str2dat( source, nSamples=None, nChannels=nChannels, dtype=raw_dtype )
		return self
	
	if source.lower().endswith( '.wav' ): return ReadWav( self, source )
	
	return Read_AVBin( self, source )

def Write( self, filename=None, helper=None ):
	if filename is None: filename = self.filename
	if filename is None: raise TypeError( 'no filename supplied' )
	extension = os.path.splitext( filename )[ -1 ].lower()
	nativeSupport = [ '', '.wav' ]
	if extension not in nativeSupport:
		if helper is None:
			if ffmpeg.IsInstalled(): helper = 'ffmpeg'
			elif sox.IsInstalled(): helper = 'sox'
			else: helper = 'ffmpeg'
	if helper is None:
		WriteWav( self, filename )
	elif helper == 'ffmpeg':
		if not ffmpeg.IsInstalled(): raise ffmpeg.NotInstalled( 'cannot save in formats other than uncompressed .wav' )
		ffmpeg( filename, source=self )( self )
	elif helper == 'sox':
		if not sox.IsInstalled(): raise sox.NotInstalled( 'cannot save in formats other than uncompressed .wav' )
		sox( filename, source=self )( self )
	return self
	
Sound.Read  = Read
Sound.Write = Write
Sound.Append = AppendWavFrames

AUXBIN = PackagePath( 'aux-bin' )

# needs threading, subprocess, shutil---and ffmpeg subclass also needs re and numpy for GrokFormat
class AuxiliaryBinaryInterface( object ):
	"""
	Abstract base class for classes like `ffmpeg` and `sox`
	that provide an interface to an external "auxiliary"
	command-line binary.
	"""
	verbose = False
	tempformat = '.wav'
	
	@classmethod
	def GetExecutablePath( cls, searchPath=False ):
		if os.path.isabs( cls.executable ): return cls.executable
		projectName = cls.executable
		basename = projectName + ( '.exe' if sys.platform.lower().startswith( 'win' ) else '' )
		for candidate in [
			os.path.join( AUXBIN, basename ),
			os.path.join( AUXBIN, projectName, basename ),
			PackagePath( projectName, basename ),
			PackagePath( basename ),
		]:
			if os.path.isfile( candidate ): return candidate
		x = cls.executable
		if os.path.isabs( x ) or not searchPath: return x
		locator = 'where' if sys.platform.lower().startswith( 'win' ) else 'which'
		sp = subprocess.Popen( [ locator, x ], stdout=subprocess.PIPE, stderr=subprocess.PIPE )
		stdout, stderr = sp.communicate()
		if sp.returncode or stderr: return None
		if not isinstance( stdout, str ): stdout = stdout.decode( 'utf-8' )
		return stdout.strip()
	
	@classmethod
	def IsInstalled( cls ):
		"""
		Return `True` or `False` depending on whether the auxiliary
		binary executable managed by this class (`ffmpeg` or `sox`)
		is accessible and executable, either inside the `audiomath`
		package (see `Install()`) or on the operating system's
		search path.
		
		See also:  `Install()`
		"""
		try: process = subprocess.Popen( [ cls.GetExecutablePath(), '-version' ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
		except OSError: return False
		process.communicate()
		return True
		
	@classmethod
	def Install( cls, pathToDownloadedExecutable, deleteOriginal=False, preview=False ):
		"""
		Auxiliary command-line binaries (like `ffmpeg` or `sox`) can
		be large relative to the rest of `audiomath`. Therefore, they
		are not included in the package by default. You should
		download what you need from the respective project websites
		(e.g. https://ffmpeg.org or http://sox.sourceforge.net )
		
		If the binary managed by this class is already installed
		somewhere on the operating-system's search path, `audiomath`
		will be able to find it, so then you probably do not need this
		helper function. However, if you have just downloaded, say, a
		statically-linked build of `ffmpeg.exe`, are looking for
		somewhere to put it, and want to put it inside the `audiomath`
		package directory itself, then this function will do it for
		you (it will actually put it inside an automatically-created
		sub-directory called `aux-bin`). `audiomath` will find it there,
		and it will also be included in the output of
		`Manifest('pyinstaller')` which helps if you want to use
		`pyinstaller` to freeze your application.
		
		NB: if the utility consists of multiple files (e.g. `sox.exe`
		and its many associated `.dll` files on Windows) then 
		`pathToDownloadedExecutable` should be a path to the
		*directory* that contains them all. 
		"""
		pathToDownloadedExecutable = os.path.realpath( pathToDownloadedExecutable )
		if  os.path.isfile( pathToDownloadedExecutable ): originals = [ pathToDownloadedExecutable ]
		elif os.path.isdir( pathToDownloadedExecutable ): originals = glob.glob( os.path.join( pathToDownloadedExecutable, '*' ) )
		else: raise IOError( 'could not find file/directory ' + pathToDownloadedExecutable )
		singleFile = len( originals ) == 1
			
		old = cls.GetExecutablePath( searchPath=False )
		if not os.path.isabs( old ): old = ''
		if not singleFile: old = ''
			
		dstDir = AUXBIN
		projectName = cls.executable
		dstBaseName = projectName + ( '.exe' if sys.platform.lower().startswith( 'win' ) else '' )
		if not singleFile: dstDir = os.path.join( dstDir, projectName )
			
		print( '' )
		if not os.path.isdir( dstDir ):
			print( '{verb} directory {dstDir}\n'.format( dstDir=dstDir, verb='would create' if preview else 'creating' ) )
			if not preview: os.makedirs( dstDir )
			
		for src in originals:
			dst = os.path.join( dstDir, dstBaseName if singleFile else os.path.basename( src ) )
			print( """{verb}\n    from: {src}\n      to: {dst}""".format( src=src, dst=dst, verb='would copy' if preview else 'copying' ) )
			if not preview: shutil.copy2( src, dst )
			if deleteOriginal:
				print( '{verb} original {src}'.format( src=src, verb='would remove' if preview else 'removing' ) )
				if not preview: os.remove( src )
			print( '' )
			if old and os.path.realpath( dst ) == os.path.realpath( old ): old = ''
		if old and os.path.isfile( old ):
			print( '{verb} old file {old}\n'.format( old=old, verb='would remove' if preview else 'removing' ) )
			if not preview: os.remove( old )
		
	@classmethod
	def Run( cls, args='', stdin=None, verbose=None, capture=False ):
		execpath = cls.GetExecutablePath()
		if verbose is None: verbose = cls.verbose
		if verbose: print( ( ( "%s" % execpath ) if ' ' in execpath else execpath ) + ' ' + ( args if isinstance( args, str ) else ' '.join( '"%s"' % arg for arg in args ) ) )
		outputOptions = dict( stdout=subprocess.PIPE, stderr=subprocess.PIPE ) if capture else {}
		if isinstance( args, str ): args = shlex.split( args )
		try: process = subprocess.Popen( [ execpath ] + args, stdin=subprocess.PIPE, **outputOptions )
		except OSError:
			if not cls.IsInstalled(): raise cls.NotInstalled()
			return -1
		outputStreams = process.communicate( stdin )
		if not capture: return process.returncode
		out = {}
		out[ 'stdout' ], out[ 'stderr' ] = [ x.decode( 'utf8' ).rstrip() if hasattr( x, 'decode' ) and not isinstance( x, str ) else x for x in outputStreams ]
		out[ 'returnCode' ] = process.returncode
		return out
		
	def RunAsynchronously( self, *args ):
		if not isinstance( self, AuxiliaryBinaryInterface ):
			raise TypeError( 'this is an instance method---maybe you were thinking of the class method Run()?' )
		args = [ arg for item in args for arg in ( item if isinstance( item, ( tuple, list ) ) else [ item ] ) ] 
		executable = self.GetExecutablePath()
		cmd = [ executable ] + list( str( arg ) for arg in args )
		if self.verbose: print( ' '.join( cmd ) )
		
		try: self.process = subprocess.Popen( cmd, stdin=subprocess.PIPE, stdout=self.pipeOut if self.pipeOut else subprocess.PIPE, stderr=subprocess.PIPE if self.pipeOut else subprocess.STDOUT )
		except OSError as error:
			if not self.IsInstalled(): raise self.NotInstalled()
			raise OSError( 'failed to launch %s - %s' % ( executable, error ) )
		self.output = []
		threadParams = self.threadParams = dict( processConsoleOutput=self.process.stderr if self.pipeOut else self.process.stdout, outputList=self.output, keepGoing=True, verbose=self.verbose )
		def Communicate():
			while threadParams[ 'keepGoing' ]:
				try:
					line = threadParams[ 'processConsoleOutput' ].readline()
					if not line: break
					if not isinstance( line, str ): line = line.decode( 'utf-8', errors='ignore' ) # NB: encoding could be anything in principle...
					if threadParams[ 'verbose' ]: print( line.rstrip() )
					threadParams[ 'outputList' ].append( line )
				except:
					break
		threading.Thread( target=Communicate ).start()
		
	def Close( self ):
		#if self.verbose: print( 'closing %s' % self._short_repr() )
		if self.process is not None: self.process.stdin.close()
		self.threadParams[ 'keepGoing' ] = False
		self.process.wait()
		
	def __del__( self ):
		if self.verbose: print( '%s is being deleted' % self._short_repr() )
		self.Close()
		
	_classNamePrefix = ''
	def _short_repr( self, *p ): return '<%s%s 0x%0*X>' % ( self._classNamePrefix, self.__class__.__name__, ( 16 if sys.maxsize > 2 ** 32 else 8 ), id( self ) )
	def _super_repr( self, *p ): return object.__repr__( self )
		
	@staticmethod
	def GrokFormat( format ):
		"""
		Convert a format specifier (anything that is accepted
		as an input to `numpy.dtype()`) into a string that
		specifies sample format in ffmpeg style (e.g. `'f32le'`).
		"""
		if not isinstance( format, str ) or not re.match( r'^[fsu](8|(16|24|32|48|64)(le|be))$', format, re.I ):
			dtype = numpy.dtype( format )
			format = '%s%d%s' % (
				's' if dtype.kind == 'i' else dtype.kind,
				dtype.itemsize * 8,
				'' if dtype.itemsize == 1 else 'be' if dtype.byteorder in '>!' or ( dtype.byteorder in '@=' and sys.byteorder != 'little' ) else 'le',
			)
		return format.lower()
			
	def __init__( self, destination, source=None, format=None, nChannels=None, fs=None, transform=None, verbose=None ):
		self.process = None
		self.threadParams = {}
		if verbose is not None: self.verbose = verbose # otherwise leave fall back on the class attribute
		self.transform = transform
		
		if isinstance( destination, str ):
			self.destinationFileName = destination
			self.pipeOut = None
		else:
			self.destinationFileName = '-'
			self.pipeOut = destination
			if isinstance( self.pipeOut, AuxiliaryBinaryInterface ) and source is None:
				source = self.pipeOut
			if hasattr( self.pipeOut, 'process' ): self.pipeOut = self.pipeOut.process
			if hasattr( self.pipeOut, 'stdin'   ): self.pipeOut = self.pipeOut.stdin
				
		if isinstance( source, str ):
			self.sourceFileName = source
			source = None  # .format, .nChannels and .fs will then be filled in inappropriately with default values, but these will not be used anyway
		else:
			self.sourceFileName = '-'
			
		# NB: interpretation of Stream object attributes, below, is specific to _wrap_portaudio
		if not format: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: format = source.stream.sampleFormat[ 'numpy' ]
			except: pass
		if not format: # see if source is itself a Stream instance
			try: format = source.sampleFormat[ 'numpy' ]
			except: pass
		if not format: # see if source is a Sound instance
			try: format = source.dtype_encoded
			except: pass
		if not format: # see if source is another AuxiliaryBinaryInterface
			try: format = source.format
			except: pass
		if not format:
			format = 'float32'
			
		if not nChannels: # see if source is a Player instance, with a Sound instance in source.sound
			try: nChannels = source.sound.nChannels
			except: pass
		if not nChannels: # see if source is itself a Sound instance (or another AuxiliaryBinaryInterface)
			try: nChannels = source.nChannels
			except: pass
		if not nChannels: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: nChannels = nChannels = source.stream.nInputChannels if source.stream.nInputChannels else source.stream.nOutputChannels
			except: pass
		if not nChannels: # see if source is itself a Stream instance
			try: nChannels = nChannels = source.nInputChannels if source.nInputChannels else source.nOutputChannels
			except: pass
		if not nChannels:
			nChannels = 2
		
		if not fs: # see if source is a Player or Recorder instance, with a Stream instance in source.stream
			try: fs = source.stream.fs
			except: pass
		if not fs: # see if source is a Player instance, with a Sound instance in source.sound
			try: fs = source.sound.fs
			except: pass
		if not fs: # see if source is itself a Sound or Stream instance (or another AuxiliaryBinaryInterface)
			try: fs = source.fs
			except: pass
		if not fs:
			fs = 44100
		
		self.format = self.GrokFormat( format )
		self.nChannels = nChannels
		self.fs = fs
		if self.verbose: print( '%s has been initialized' % self._short_repr() )
		
	def __call__( self, data, sampleNumber=None, fs=None ):
		if not self.process.stdin.closed:
			transform = self.transform
			if transform: data = transform( data, sampleNumber, fs )
			if hasattr( data, 'dat2str' ): data = data.dat2str()
			else: data = data[ :, :self.nChannels ].tostring()
			try: self.process.stdin.write( data )
			except:
				if not self.verbose:
					try: print( '\n'.join( self.threadParams[ 'outputList' ] ) )
					except Exception as error: print( error )
				raise
				
	@classmethod
	def Process( cls, snd, destination=None, **kwargs ):
		"""
		Whereas instances of `AuxiliaryBinaryInterface` subclasses
		are good for processing chunks of sound data sequentially,
		if you simply want to process a whole `Sound` instance in
		one go, it is easier to use this class method. Under the
		hood, it will create a temporary instance, using any
		specified `**kwargs`.
		
		You can direct its output to the file specified by
		`destination`. Alternatively you can leave `destination=None`
		and thereby receive the output (actually written to and
		read back from a temporary uncompressed `.wav` file) as
		a new `Sound` instance returned by this function.
		
		Example, using the `sox` subclass::
		
		    import audiomath as am
		    s = am.TestSound('12')
		    s2 = am.sox.Process(s, effects='loudness -10')
		    
		    # or, to take that example one stage further,
		    # the following will generally equalize the
		    # perceived loudness (according to ISO 226)
		    # across all channels of a Sound `s`:
		    
		    s = am.TestSound().AutoScale()
		    s2 = am.Stack(
		        am.sox.Process(eachChannel, effects='loudness -10')
		        for eachChannel in s.SplitChannels()
		    ).AutoScale() # finally rescale all channels together
		                  # according to their collective maximum
		"""
		tmp = None
		result = None
		if destination is None:
			with tempfile.NamedTemporaryFile( suffix=cls.tempformat, delete=False ) as tmp: pass
			destination = tmp.name
		instance = cls( destination=destination, source=snd, **kwargs )
		if instance.sourceFileName == '-':
			instance( snd )
		instance.Close()
		if tmp:
			result = Sound( destination )
			result.filename = result.label = None
			try: os.remove( tmp.name )
			except: pass # Windows can be sticky about this
		return result
	class NotInstalled( RuntimeError ): pass

NotInstalled = AuxiliaryBinaryInterface.NotInstalled
def SubclassNotInstalled( cls ):
	classname = cls.__name__
	executable = cls.executable
	class NotInstalled( AuxiliaryBinaryInterface.NotInstalled ):
		def __init__( self, message='' ):
			if message: message = message.strip() + '\n'
			message += 'You need to install the `%s` binary manually for this functionality.\nSee `%s.Install` for more help.' % ( executable, classname )
			super( self.__class__, self ).__init__( message )
	cls.NotInstalled = NotInstalled
	return cls

@SubclassNotInstalled
class ffmpeg( AuxiliaryBinaryInterface ):
	"""
	This class manages the auxiliary command-line binary `ffmpeg`
	(https://ffmpeg.org ).
	
	An instance of this class connects to the standalone `ffmpeg`
	executable, assuming that that `.IsInstalled()`. The instance
	can then be used to encode audio data to disk in a variety of
	formats. There are two main applications, illustrated in the
	following examples. Both of them implicitly use `ffmpeg`
	instances under the hood::
	
	    # saving a Sound in a format other than uncompressed .wav:
	    import audiomath as am
	    s = am.TestSound( '12' )
	    s.Write( 'example_sound.ogg' )
	    
	    # recording direct to disk:
	    import audiomath as am
	    s = am.Record(5, loop=True, filename='example_recording.mp3')
	    
	The latter example uses an `ffmpeg` instance as a callable
	`.hook` of a `Recorder` instance.  For more control (asynchronous
	functionality) you can do it more explicitly as follows::
	
		import audiomath as am
		h = am.Recorder(5, loop=True, start=False)
		h.Record(hook=am.ffmpeg('example_recording.mp3', source=h, verbose=True))
		
		h.Wait() # wait for ctrl-C (replace this line with whatever)
		# ...
		
		h.Stop(hook=None) # garbage-collection of the `ffmpeg` instance is one way to `.Close()` it
		s = h.Cut()
	
	The ffmpeg binary is large, so it is not included in the Python
	package by default. Installation is up to you.  You can install
	it like any other application, somewhere on the system path.
	Alternatively, if you want to, you can put it directly inside
	the `audiomath` package directory, or inside a subdirectory
	called `aux-bin`---the class method `ffmpeg.Install()` can help
	you do this.  If you install it inside the `audiomath` package,
	then this has two advantages: (a) audiomath will find it there
	when it attempts to launch it, and (b) it will be included in
	the output of `Manifest('pyinstaller')` which you can use to
	help you freeze your application.
	
	See also:
	
		`ffmpeg.Install()`,
		`ffmpeg.IsInstalled()`
	
	"""
	# TODO - known issues:
	# - extra samples at beginning (~25ms) and end (~20ms) when writing mp3 on macOS
	#   https://bitbucket.org/snapproject/audiomath-gitrepo/issues/3
	
	executable = 'ffmpeg'
	
	def __init__( self, destination, source=None, format=None, nChannels=None, fs=None, kbps=192, transform=None, verbose=None ):
		"""
		Args:
			destination (str, ffmpeg, sox):
				output filename---be sure to include the file
				extension so that ffmpeg can infer the desired
				output format; can alternatively use another
				instance of `ffmpeg` or `sox` as the destination
				(in that case, `format`, `nChannels` and `fs` will
				also be intelligently inferred from that instance
				if they are not otherwise specified);
			
			source (Sound, Recorder, Player, Stream):
				optional instance that can intelligently specify
				`format`, `nChannels` and `fs` all in one go;
			
			format (str):
				format of the raw data---should be either a valid
				ffmpeg PCM format string (e.g. `'f32le'`) or a
				construction argument for `numpy.dtype()` (e.g.
				`'float32'`, `'<f4'`);
			
			nChannels (int):
				number of channels to expect in each raw data
				packet;
				
			fs (int, float):
				sampling frequency, in Hz;
			
			kbps (int):
				kilobit rate for encoding;
			
			transform (None, function):
				an optional callable that can receives each data
				packet, along with the sample number and sampling
				frequency, and return a transformed version of the
				data packet to be send to `ffmpeg` in place of the
				original;
			
			verbose (bool):
				whether or not to print the standard output and
				standard error content produced by the binary.
		"""
		self.kbps = kbps
		super( ffmpeg, self ).__init__( destination=destination, source=source, format=format, nChannels=nChannels, fs=fs, transform=transform, verbose=verbose )
		self.RunAsynchronously(
			self.RawFormatOptions() if self.sourceFileName == '-' else [],
			'-i',   'pipe:' if self.sourceFileName == '-' else self.sourceFileName,
			
			'-b:a', '%dk' % self.kbps,
			'-vn',
			'-y',
			self.destinationFileName,
		)
	
	def RawFormatOptions( self ):
		return [
			'-f',   self.format,
			'-ac',  '%d'  % self.nChannels,
			'-ar',  '%g'  % self.fs,
		]
		
@SubclassNotInstalled
class sox( AuxiliaryBinaryInterface ):
	"""
	This class manages the auxiliary command-line binary `sox`
	(https://sox.sourceforge.net ).
	
	An instance of this class connects to the standalone `sox`
	executable, assuming that that `.IsInstalled()`. The instance
	can then be used to transform audio data in a wide variety of
	ways, and encode it to disk in a variety of formats (although
	typically fewer formats than `ffmpeg`).
	
	You may find the class method `sox.Process()` more useful
	than an instance.
	
	You can also chain processing from one `sox` instance to 
	another, or between a `sox` instance and a `ffmpeg` instance,
	by passing the other instance as this one's `destination`
	instead of specifying a filename.
	
	Here is an example of chaining. Let's say we want to use
	a sox effect and save the result as in mp3 format, but sox
	does not support the mp3 format. So instead we write out,
	on a pipe, to an `ffmpeg` process, which can save to mp3::
	
	    import audiomath as am
	    s = am.TestSound('12')
	    am.sox.Process(
	        s,
	        destination=am.ffmpeg( 'output.mp3', source=s ),
	        effects='loudness -10',
	    )
	    
	The sox binary is not included in the Python package by
	default. Installation is up to you.  You can install it like
	any other application, somewhere on the system path.
	Alternatively, if you want to, you can put it directly inside
	the `audiomath` package directory, or inside a subdirectory
	called `aux-bin`---the class method `sox.Install()` can help
	you do this.  If you install it inside the `audiomath` package,
	then this has two advantages: (a) audiomath will find it there
	when it attempts to launch it, and (b) it will be included in
	the output of `Manifest('pyinstaller')` which you can use to
	help you freeze your application.
	"""
	
	executable = 'sox'
	
	def __init__( self, destination, source=None, format=None, nChannels=None, fs=None, transform=None, effects='', verbose=None ):
		"""
		Args:
			destination (str, ffmpeg, sox):
				output filename---be sure to include the file
				extension so that ffmpeg can infer the desired
				output format; can alternatively use another
				instance of `ffmpeg` or `sox` as the destination
				(in that case, `format`, `nChannels` and `fs` will
				also be intelligently inferred from that instance
				if they are not otherwise specified);
			
			source (Sound, Recorder, Player, Stream):
				optional instance that can intelligently specify
				`format`, `nChannels` and `fs` all in one go;
			
			format (str):
				format of the raw data---should be either a valid
				ffmpeg PCM format string (e.g. `'f32le'`) or a
				construction argument for `numpy.dtype()` (e.g.
				`'float32'`, `'<f4'`);
			
			nChannels (int):
				number of channels to expect in each raw data
				packet;
				
			fs (int, float):
				sampling frequency, in Hz;
			
			effects (str, list, tuple):
				a string, or sequence of strings, specifying the
				effect names and effect options to be passed to
				sox on the command line;
			
			transform (None, function):
				an optional callable that can receive each data
				packet, along with the sample number and sampling
				frequency, and return a transformed version of the
				data packet to be send to `sox` in place of the
				original;
			
			verbose (bool):
				whether or not to print the standard output and
				standard error content produced by the binary.
		"""
		if not isinstance( effects, ( tuple, list ) ): effects = [ effects ]
		self.effects = [ arg for effect in effects for arg in ( effect if isinstance( effect, ( tuple, list ) ) else shlex.split( effect ) ) ]
		super( sox, self ).__init__( destination=destination, source=source, format=format, nChannels=nChannels, fs=fs, transform=transform, verbose=verbose )
		self.RunAsynchronously(
			# global_options,
			
			self.RawFormatOptions() if self.sourceFileName == '-' else [],
			self.sourceFileName,
			
			self.RawFormatOptions() if self.destinationFileName == '-' else [],
			self.destinationFileName,
			
			self.effects,
		)
		
	def RawFormatOptions( self, format=None ):
		if format: format = self.GrokFormat( format )
		else: format = self.format
		
		match = re.match( r'^(?P<encoding>\D)(?P<bits>\d+)(?P<endian>\D*)$', format, re.I ).groupdict()
		match[ 'encoding' ] = dict( s='signed-integer', u='unsigned-integer', f='floating-point' )[ match[ 'encoding' ] ]
		if match[ 'endian' ]: match[ 'endian' ] = dict( le='little', be='big' )[ match[ 'endian' ] ]
		else: del match[ 'endian' ]
		args = [ '--type', 'raw' ]
		args += [ arg for k, v in match.items() for arg in [ '--' + k, v ] ]
		args += [ '--channels', '%d' % self.nChannels, '--rate', '%g' % self.fs ]
		return args
		