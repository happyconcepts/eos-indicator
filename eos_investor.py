#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://github.com/happyconcepts/eos-investor
# mit license

VERSION = '1.1'
APPID 	= 'EOS-investor'

import os
import requests
import gi
import signal
from datetime import datetime
import json
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
gi.require_version('GdkPixbuf', '2.0')
from gi.repository.GdkPixbuf import Pixbuf
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as AppIndicator

PROJECTDIR = os.path.dirname(os.path.realpath(__file__))

dir = os.path.expanduser("~") +"/.eos-investor"
if not os.path.exists(dir):
    os.makedirs(dir)
prefFile = os.path.join(dir, 'prefs.json')

test = False
if test == True:
    print ("test mode")

class EOSindicator(object):
    def __init__(self):
        self.ind = AppIndicator.Indicator.new(APPID,
	PROJECTDIR + "/icons/eos.png",AppIndicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        # local user preferences
        try:
            with open(prefFile, 'r') as f:
                print ("loading saved settings...")
                prefs = json.load(f)

        except IOError as e:
	    #Does not exist OR no read permissions...
            print ("no saved settings found")
            if test == True:
                print ("Unable to access prefs.json")
                print ("prefs: " +dir +"/")
                print (e)
            print ("creating settings file ...")
            with open(prefFile, 'w') as uf:
                uf.write('{"version":"'+VERSION+'","base":"USD","interval":"5","modified":"'+datetime.now().strftime('%m/%d %H:%M:%S')+'"}\n')
            with open(prefFile, 'r') as f:
                prefs = json.load(f) # read prefs.

        self.price_active = True

        if prefs:
            self.interval = int(prefs['interval'])
            self.base = prefs['base']
            self.base_last = prefs['base']
        else:
            self.interval = 5
            self.base = 'USD'
            self.base_last = 'USD'

        self.symbol = 'EOS'

        self.menu = Gtk.Menu()
        self.build_menu()

        self.price_update()
        self.testid = GLib.timeout_add_seconds(60 * self.interval, self.price_update)

    def build_menu(self):

        item_settings = Gtk.MenuItem()
        item_settings.set_label("Settings...")
        item_settings.connect("activate", self.handler_settings_callback)
        item_settings.show()
        self.menu.append(item_settings)

        item_refresh = Gtk.MenuItem()
        item_refresh.set_label("Update Prices")
        item_refresh.connect("activate", self.handler_menu_reload)
        item_refresh.show()
        self.menu.append(item_refresh)

        item_about = Gtk.MenuItem()
        item_about.set_label("About ...")
        item_about.connect("activate", self.about)
        item_about.show()
        self.menu.append(item_about)

        item = Gtk.MenuItem()
        item.set_label("Exit")
        item.connect("activate", self.handler_menu_exit)
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

    def handler_settings_callback (self, source):

        win = SettingsWindow()
        win.set_keep_above(True)
        win.connect("destroy", self.handler_settings)
        win.show_all()

    @staticmethod
    def handler_menu_exit(evt):
        Gtk.main_quit()
        print (APPID +" has quit.")

    def handler_menu_reload(self, source):
        ind.base_last = ind.base
        self.price_update()

    def handler_settings(self, source):
        if (test == True):
            print ("ind.base: " +ind.base)
            print ("ind.base_last: " +ind.base_last)
            print ("ind.interval: " +str(ind.interval))
            print ("ind.interval_last: " +str(ind.interval_last))
            #print testing.dump(source)

        if (ind.base_last != ind.base) or (ind.interval_last != ind.interval):
            ind.base_last = ind.base
            self.save_settings()
            self.price_update()

    def about(self, source):
        dialog = Gtk.AboutDialog()
        dialog.set_border_width(10)
        dialog.set_program_name('EOS-investor')
        dialog.set_version(VERSION)
        dialog.set_license('MIT License\n\n' + ' A copy of the license is available at https://github.com/happyconcepts/eos-investor/blob/master/LICENSE' )
        dialog.set_wrap_license(True)
        dialog.set_copyright('Copyright 2018 Ben Bird and contributors')
        dialog.set_comments('Track the latest price of EOS \n'+'with this free open source Linux desktop indicator!\n'+'Loaded with Python '+ str(sys.version_info[0]) +'\n\n'+'Your donations help:\n\n' + 'BTS: eos-indicator\n' +'Bitcoin: 1FZhqidv4oMRoiry9mGASFL7JSgdB27Mmn')
        dialog.set_website('https://github.com/happyconcepts/eos-investor/')
        pixbuf = Pixbuf.new_from_file_at_size("icons/eos-investor.png", 203, 105)
        dialog.set_logo(pixbuf)
        dialog.run()
        dialog.destroy()

    def save_settings(self):

        with open(prefFile, 'w') as uf:
            uf.write('{"version":"1.0","base":"' +ind.base +'","interval":"'+str(ind.interval)+'","modified":"'+datetime.now().strftime('%m/%d %H:%M:%S')+'"}\n')

    def price_update(self):
        timestamp = datetime.now().strftime('%m/%d %H:%M:%S')

        try:
            if self.price_active == True:
                self.b = binance(self.symbol)

                if self.base =='EUR':
                    self.c = coinmktcap(self.symbol, self.base)
                    self.ind.set_label(self.c.run() + " ~BTC: "+ self.b.run() , "")
                    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/eos.png")
                    print (timestamp + " EOS price: "+ self.c.price())

                elif self.base =='CNY':
                    self.c = coinmktcap(self.symbol, self.base)
                    self.ind.set_label(self.c.run() + " ~BTC: "+ self.b.run() , "")
                    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/eos.png")
                    print (timestamp + " EOS price: "+ self.c.price())

                else :
                    self.g = gate(self.symbol, self.base)
                    self.ind.set_label(self.g.run() + " ~BTC: "+ self.b.run() , "")
                    self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/eos.png")
                    print (timestamp + " EOS price: "+ self.g.price())

                if (test == True):
                    print ("symbol/base: " +self.symbol +"/"+self.base)

            else:
                self.ind.set_label("Pricing is not active.","")

                print (timestamp + " prices not updated (not active)")
                if (test == True):
                    print ("update interval is " + str(self.interval) + " min")

        except Exception as e:

            self.ind.set_label("eos-investor","")
            self.ind.set_icon(os.path.dirname(os.path.realpath(__file__)) +"/icons/bell_on.png")

            print (timestamp + " prices not updated (check connection)")

            if test == True:
                print("error: " + str(e))

        return True

    def main(self):
        Gtk.main()

class gate:
    def __init__(self, coin='eos', base='usdt'):
        if base == 'USD':
            base = 'USDT'
        self.pair = coin +"_"+ base
        self.pair = self.pair.lower()

    def run(self):
        url = 'http://data.gate.io/api2/1/ticker/'+self.pair
        response = requests.get(url)
        json = response.json()

        if not json['result']:
            return "Gate says: "+ json['message']
        else:
            chg = json['percentChange']
            self.last = json['last']

            if chg.isnumeric():
            # its a number
                chg = str(json['percentChange'])

            # truncate @  6 char.
            chg = (chg[:5]) if len(chg) > 5 else chg

            if chg[:1] != '-':
                chg = " +"+ chg +"% "
            else:
                chg = " ("+chg+"%) "

            if self.last.isnumeric():
                self.last = round(json['last'],4)
                self.last = str(self.last)

            return '$'+self.last + " " +chg

    def price(self):
        return "$" +self.last

class binance:
    def __init__(self, coin='EOS', base='BTC'):
        self.pair = coin+base
        self.pair.upper()

    def run(self):
        url = 'https://api.binance.com/api/v3/ticker/price?symbol='+self.pair
        response = requests.get(url)
        json = response.json()

        if not json['price']:
            return "Error: binance (api): "+ json['msg']
        else:
            return u'\u0E3F'+str(json['price'])

class coinmktcap:
    def __init__(self, coin='eos', base='EUR'):
        if coin == 'EOS':
            coin = 'eos'

        self.pair = coin +"/?convert="+base
        self.base = base

    def run(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/'+self.pair
        response = requests.get(url)
        json = response.json()

        self.cmcfield = 'price_'+self.base.lower() # price_eur
        if not json[0][self.cmcfield]:
            return "Error: coinmarketcap (api): " + json[0]['error']

        else:
            self.last = round(float(json[0][self.cmcfield]),4)
            self.chg = round(float(json[0]['percent_change_24h']),1)
            self.chg = str(self.chg)

            if self.chg[:1] != '-':
                self.chg = " +"+ self.chg +"% "
            else:
                self.chg = " ("+self.chg+"%) "
            if self.base == 'EUR':
                return u'\u20AC' + str(self.last) + " "+ self.chg
            else:
                return u'\u00a5' + str(self.last) + " "+ self.chg # yuan
    def price(self):
        if self.base == 'EUR':
            return  u'\u20AC'+str(self.last)
        else:
            return  u'\u00a5'+str(self.last) # yuan

class SettingsWindow(Gtk.Window):
    def __init__(self):

        Gtk.Window.__init__(self, title="Settings")

        self.set_border_width(15)
        self.set_default_size(300, 160)
        self.set_position(Gtk.WindowPosition.CENTER)
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(box_outer)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label1 = Gtk.Label("Price Updates", xalign=0)
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        switch.set_active(True)
        hbox.pack_start(label1, True, True, 0)
        hbox.pack_start(switch, False, True, 0)

        box_outer.pack_start(hbox, True, True, 0)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label("Base currency:", xalign=0)
        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "$ USD")

        if ind.base == 'USD':
            button1.set_active(True)

        button1.connect("clicked", self.change_base, "USD")
        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(button1, False, False, 0)

        button2 = Gtk.RadioButton.new_from_widget(button1)
        button2.set_label(u'\u20AC' +" Euro")

        if ind.base == 'EUR':
            button2.set_active(True)

        button2.connect("clicked", self.change_base, "EUR")

        hbox.pack_start(button2, False, False, 0)

        button3 = Gtk.RadioButton.new_from_widget(button1)
        button3.set_label(u'\u00a5' +" Yuan")

        if ind.base == 'CNY':
            button3.set_active(True)

        button3.connect("clicked", self.change_base, "CNY")

        hbox.pack_start(button3, False, False, 0)

        box_outer.pack_start(hbox, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label3 = Gtk.Label("Update interval, minutes", xalign=0)
        combo = Gtk.ComboBoxText()
        combo.connect("changed", self.change_interval) ##
        combo.insert(0, "1", "1")
        combo.insert(1, "5", "5")
        combo.insert(2, "10", "10")
        combo.insert(3, "15", "15")
        combo.insert(4, "30", "30")
        combo.insert(5, "60", "60")
        combo.insert(6, "240", "240")

        if ind.interval == 1:
            combo.set_active(0)
        elif ind.interval == 5:
            combo.set_active(1)
        elif ind.interval == 10:
            combo.set_active(2)
        elif ind.interval == 15:
            combo.set_active(3)
        elif ind.interval == 30:
            combo.set_active(4)
        elif ind.interval == 60:
            combo.set_active(5)
        elif ind.interval == 240:
            combo.set_active(6)
        else:
            pass

        hbox.pack_start(label3, True, True, 0)
        hbox.pack_start(combo, False, True, 0)
        box_outer.pack_start(hbox, True, True, 0)


    def change_base(self, button, name):

        if button.get_active():
            ind.base_last = ind.base
            ind.base = name
            if test == True:
                print("base is set to " +ind.base)

    def change_interval(self, combo):

        self.interval_current = str(ind.interval)
        self.interval_new = combo.get_active_text()

        if self.interval_new is not None:
            try:
                GLib.source_remove(ind.testid)
                ind.interval_last = int(ind.interval)
                ind.interval = int(self.interval_new)
                ind.testid = GLib.timeout_add_seconds(60 * ind.interval, ind.price_update)

            except Exception as e:
                print ("could not change update interval")

def add (x,y):
    """Add function"""
    return x + y


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    print ("starting "+APPID +" v. "+VERSION)
    ind = EOSindicator()
    ind.main()
