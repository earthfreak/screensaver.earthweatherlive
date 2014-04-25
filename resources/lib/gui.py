#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2013 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import urllib
import random
import datetime
import time
import os

import xbmcaddon
import xbmcgui
import xbmc

import controller


addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')
addon_path = addon.getAddonInfo('path')
image_dir = xbmc.translatePath( os.path.join( addon_path, 'resources', 'skins', 'default', 'media' ,'').encode("utf-8") ).decode("utf-8")



#lightSizeNormal = 50
#lightPaddingNormal = 2
#blockPaddingLarge = 50
#blockPaddingSmall = 10
blockSizeNormal = 3
blockSizeSeconds = 8


scriptId   = 'screensaver.unaryclock'



class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback, log_callback):
            self.exit_callback = exit_callback
	    self.log_callback = log_callback

        def onScreensaverDeactivated(self):
            #self.log_callback('sending exit_callback')
            self.exit_callback()
        def onAbortRequested(self):
	    #self.log_callback('abort requested')
	    self.exit_callback()
                

    def showClock(self):
        now = datetime.datetime.today()
        #urllib.urlretrieve('http://p1.pichost.me/i/27/1503466.jpg', '/tmp/a.jpg')
        #urllib.urlretrieve('http://www.kguttag.com/wp-content/uploads/2012/02/res-chart-KGOT-1280x720-002.png', '/tmp/b.png')
        #urllib.urlretrieve('http://www.kguttag.com/wp-content/uploads/2012/02/res-chart-KGOT-848x480-002.png', '/tmp/b.png')
        #urllib.urlretrieve('http://www.themacfaq.com/wp-content/uploads/2013/05/1920x1080_overscan.gif', '/tmp/b.gif')
        #urllib.urlretrieve('http://p1.pichost.me/i/27/1503466.jpg', '/tmp/b.jpg')
        
        if self.waitcounter ==  10 or self.waitcounter > 20:
            #' + self.projection + '
            if self.projection == 'moon':
                urllib.urlretrieve('http://static.die.net/moon/512.jpg', '/tmp/' + str(self.waitcounter) + '.map')
            else:    
                urllib.urlretrieve('http://static.die.net/earth/' + self.projection + '/1600.jpg', '/tmp/' + str(self.waitcounter) + '.map')
            self.background.setImage('/tmp/' + str(self.waitcounter) + '.map') 
        if self.waitcounter > 20:    
            self.waitcounter = 0
        #elif self.waitcounter > 20:
        #    urllib.urlretrieve('http://static.die.net/earth/' + self.projection + '/1600.jpg', '/tmp/bb.map')
        #    self.background .setImage('/tmp/bb.map')  
        #    self.waitcounter = 0                
        
        self.waitcounter += 1              
            

    def onInit(self):
        self.log("Screensaver starting")
        self.addon = xbmcaddon.Addon(scriptId)
        self.showSeconds = True
        self.redrawInterval = int(self.addon.getSetting('setting_redraw_interval'))
        self.projection = self.addon.getSetting('projection')
        self.resolution = self.addon.getSetting('resolution')
        self.background = self.getControl(30020)
        
        self.monitor = self.ExitMonitor(self.exit, self.log)

        #self.background = self.getControl(30020)
        self.waitcounter = 100000

        self.showClock()
        self.cont = controller.Controller(self.log, self.showClock,  self.redrawInterval)
        self.cont.start() 
    

    def exit(self):
        self.log('Exit requested')
        self.cont.stop()
    	del self.monitor
        del self.cont
        self.close()
    
    def log(self, msg):
        xbmc.log(u'Unary Clock Screensaver: %s' % msg)
		

