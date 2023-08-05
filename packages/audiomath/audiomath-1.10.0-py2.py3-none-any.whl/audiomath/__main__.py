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
If no options are supplied, `-s` is assumed---i.e., an IPython
shell will be opened on the console, with `audiomath` and `numpy`
already imported (both under their full names and under their
respective abbreviated names, `am` and `np`).

If options are supplied, the shell will not be opened unless the
`-s` option is explicitly present among them.
"""
import argparse
		
parser = argparse.ArgumentParser( prog='python -m ' + __package__, description=__doc__ )
parser.add_argument( "-v", "--version", action='store_true', default=False, help='print the version number' )
parser.add_argument( "-V", "--versions", action='store_true', default=False, help='print package and dependency version information' )
parser.add_argument( "-a", "--apis", "--host-apis", action='store_true', default=False, help='print a list of host APIs' )
parser.add_argument( "-l", "--list-devices", "--devices", action='store_true', default=False, help='print a list of devices' )
parser.add_argument( "-2", "--twoChannelTest", action='store_true', default=False, help='same as -t2, i.e. play a 2-channel test stimulus on an endless loop' )
parser.add_argument( "-8", "--eightChannelTest", action='store_true', default=False, help='same as -t8, i.e. play an 8-channel test stimulus on an endless loop' )
parser.add_argument( "-t", "--test",  metavar='NUMBER_OF_CHANNELS', action='store', default=0, type=int, help='play a test stimulus with the specified number of channels (up to 8) on an endless loop' )
parser.add_argument( "-s", "--shell", action='store_true', default=False, help='open an IPython shell, even if other flags are supplied' )
parser.add_argument( "-d", "--device",  metavar='DEVICE_INDEX',  action='store', default=None, help='specify which device should be used for playback in the --eightChannelTest' )
parser.add_argument(       "--install-ffmpeg",  metavar='PATH_TO_FFMPEG_BINARY',  action='store', default=None, type=str, help='call `ffmpeg.Install()` on the specified path' )
parser.add_argument(       "--install-sox",  metavar='PATH_TO_SOX_BINARY', action='store', default=None, type=str, help='call `sox.Install()` on the specified path' )
args = parser.parse_args()

openShell = True
player = None
playerName = 'p'

if args.version:
	openShell = args.shell
	import audiomath
	print( audiomath.__version__ )

if args.versions:
	openShell = args.shell
	import audiomath
	print( '' )
	audiomath.ReportVersions()

if args.apis:
	openShell = args.shell
	import audiomath
	print( '' )
	print( audiomath.GetHostApiInfo() )

if args.list_devices:
	openShell = args.shell
	import audiomath
	print( '' )
	print( audiomath.GetDeviceInfo() )

if args.eightChannelTest and not args.test: args.test = 8
if args.twoChannelTest   and not args.test: args.test = 2
if args.test:
	openShell = args.shell
	import audiomath
	player = audiomath.Player( audiomath.TestSound( list( range( args.test ) ) ), device=args.device )
	print( player._report( with_repr='short', indent=playerName + ' = ' ) )
	if openShell:
		player.Play( loop=True, wait=False )
	else:
		if 0:
			print( 'press ctrl-C to stop/exit' )
			player.Play( loop=True, wait=True )
		else:
			player.Play( loop=True, wait=False )
			try: ask = raw_input # dammit Guido
			except: ask = input
			try: ask( 'press return to stop/exit: ' )
			except EOFError: pass
			player.Stop()
		if not openShell: del player
		import time; time.sleep( 0.25 )

if args.install_ffmpeg:
	openShell = args.shell
	import audiomath
	try: audiomath.ffmpeg.Install( args.install_ffmpeg )
	except Exception as err: sys.sterr.write( '%s\n' % err )

if args.install_sox:
	openShell = args.shell
	import audiomath
	try: audiomath.sox.Install( args.install_sox )
	except Exception as err: sys.sterr.write( '%s\n' % err )

if openShell:
	def Shell():
		if player: locals()[ playerName ] = player
		import os, sys, time, IPython, numpy, numpy as np, audiomath, audiomath as am
		del sys.argv[ 1: ]
		print( '' )
		IPython.start_ipython( user_ns=locals() )	
	Shell()
