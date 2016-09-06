#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: chat@jat.email -*-

import iptc


def init_iptables():
    if iptc.Table(iptc.Table.FILTER).is_chain('auto_proxy'):
        iptc.Chain(iptc.Table(iptc.Table.FILTER), 'auto_proxy').flush()
    else:
        iptc.Table(iptc.Table.FILTER).create_chain('auto_proxy')

        init_rule('tcp')
        init_rule('udp')


def init_rule(protocol):
    rule = iptc.Rule()
    rule.out_interface = 'eth0'
    rule.protocol = protocol
    rule.target = iptc.Target(rule, 'auto_proxy')
    iptc.Chain(iptc.Table(iptc.Table.FILTER), 'OUTPUT').insert_rule(rule)


def add_rule(ip):
    rule = iptc.Rule()
    rule.src = ip

    target = rule.create_target('DNAT')
    target.to_destination = '127.0.0.1:8000'

    iptc.Chain(iptc.Table(iptc.Table.FILTER), 'auto_proxy').insert_rule(rule)
