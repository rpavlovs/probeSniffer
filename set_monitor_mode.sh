#!/bin/bash

iface="wlan1"

ifconfig $iface down
iwconfig $iface mode monitor
ifconfig $iface up

# airmon-ng start wlan0
