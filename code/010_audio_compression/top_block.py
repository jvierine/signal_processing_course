#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Wed Sep 16 18:11:49 2020
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 44100

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_f(
        	self.GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/4,
        	fft_size=2048,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('/home/sdr/Dropbox/Work/Documents/2020/FYS-2006/book/code/signal_processing/010_audio_compression/compressed_signal.wav', True)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(4, 1)
        self.audio_sink_0 = audio.sink(samp_rate, '', True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_integrate_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_integrate_xx_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate/4)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
