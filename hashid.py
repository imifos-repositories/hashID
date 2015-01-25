#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2015 by c0re
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__  = "c0re"
__version__ = "3.0.0"
__github__  = "https://github.com/psypanda/hashID"
__license__ = "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>"

import re
import os
import io
import sys
import argparse
from collections import namedtuple

Prototype = namedtuple('Prototype', ['regex', 'modes'])
HashMode = namedtuple('HashMode', ['name', 'hashcat', 'john', 'extended'])

prototypes = [
    Prototype(
        regex=re.compile(r'^[a-f0-9]{4}$', re.IGNORECASE),
        modes=[
            HashMode(name='CRC-16', hashcat=None, john=None, extended=False),
            HashMode(name='CRC-16-CCITT', hashcat=None, john=None, extended=False),
            HashMode(name='FCS-16', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{8}$', re.IGNORECASE),
        modes=[
            HashMode(name='Adler-32', hashcat=None, john=None, extended=False),
            HashMode(name='CRC-32B', hashcat=None, john=None, extended=False),
            HashMode(name='FCS-32', hashcat=None, john=None, extended=False),
            HashMode(name='GHash-32-3', hashcat=None, john=None, extended=False),
            HashMode(name='GHash-32-5', hashcat=None, john=None, extended=False),
            HashMode(name='FNV-132', hashcat=None, john=None, extended=False),
            HashMode(name='Fletcher-32', hashcat=None, john=None, extended=False),
            HashMode(name='Joaat', hashcat=None, john=None, extended=False),
            HashMode(name='ELF-32', hashcat=None, john=None, extended=False),
            HashMode(name='XOR-32', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{6}$', re.IGNORECASE),
        modes=[
            HashMode(name='CRC-24', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$crc32\$[a-f0-9]{8}.)?[a-f0-9]{8}$', re.IGNORECASE),
        modes=[
            HashMode(name='CRC-32', hashcat=None, john='crc32', extended=False)]),
    Prototype(
        regex=re.compile(r'^\+[a-z0-9\/.]{12}$', re.IGNORECASE),
        modes=[
            HashMode(name='Eggdrop IRC Bot', hashcat=None, john='bfegg', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{13}$', re.IGNORECASE),
        modes=[
            HashMode(name='DES(Unix)', hashcat=1500, john='descrypt', extended=False),
            HashMode(name='Traditional DES', hashcat=1500, john='descrypt', extended=False),
            HashMode(name='DEScrypt', hashcat=1500, john='descrypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='MySQL323', hashcat=200, john='mysql', extended=False),
            HashMode(name='DES(Oracle)', hashcat=3100, john=None, extended=False),
            HashMode(name='Half MD5', hashcat=5100, john=None, extended=False),
            HashMode(name='Oracle 7-10g', hashcat=3100, john=None, extended=False),
            HashMode(name='FNV-164', hashcat=None, john=None, extended=False),
            HashMode(name='CRC-64', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco-PIX(MD5)', hashcat=2400, john='pix-md5', extended=False)]),
    Prototype(
        regex=re.compile(r'^\([a-z0-9\/+]{20}\)$', re.IGNORECASE),
        modes=[
            HashMode(name='Lotus Notes/Domino 6', hashcat=8700, john='dominosec', extended=False)]),
    Prototype(
        regex=re.compile(r'^_[a-z0-9\/.]{19}$', re.IGNORECASE),
        modes=[
            HashMode(name='BSDi Crypt', hashcat=None, john='bsdicrypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{24}$', re.IGNORECASE),
        modes=[
            HashMode(name='CRC-96(ZIP)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{24}$', re.IGNORECASE),
        modes=[
            HashMode(name='Crypt16', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$md2\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='MD2', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}(:.+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='MD5', hashcat=0, john='raw-md5', extended=False),
            HashMode(name='MD4', hashcat=900, john='raw-md4', extended=False),
            HashMode(name='Double MD5', hashcat=2600, john=None, extended=False),
            HashMode(name='LM', hashcat=3000, john='lm', extended=False),
            HashMode(name='RIPEMD-128', hashcat=None, john='ripemd-128', extended=False),
            HashMode(name='Haval-128', hashcat=None, john='haval-128-4', extended=False),
            HashMode(name='Tiger-128', hashcat=None, john=None, extended=False),
            HashMode(name='Snefru-128', hashcat=None, john='snefru-128', extended=False),
            HashMode(name='Skein-256(128)', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-512(128)', hashcat=None, john=None, extended=False),
            HashMode(name='Lotus Notes/Domino 5', hashcat=8600, john='lotus5', extended=False),
            HashMode(name='ZipMonster', hashcat=None, john=None, extended=True),
            HashMode(name='md5(md5(md5($pass)))', hashcat=3500, john=None, extended=True),
            HashMode(name='md5(strtoupper(md5($pass)))', hashcat=4300, john=None, extended=True),
            HashMode(name='md5(sha1($pass))', hashcat=4400, john=None, extended=True),
            HashMode(name='md5($pass.$salt)', hashcat=10, john=None, extended=True),
            HashMode(name='md5($salt.$pass)', hashcat=20, john=None, extended=True),
            HashMode(name='md5(unicode($pass).$salt)', hashcat=30, john=None, extended=True),
            HashMode(name='md5($salt.unicode($pass))', hashcat=40, john=None, extended=True),
            HashMode(name='HMAC-MD5 (key = $pass)', hashcat=50, john=None, extended=True),
            HashMode(name='HMAC-MD5 (key = $salt)', hashcat=60, john=None, extended=True),
            HashMode(name='md5(md5($salt).$pass)', hashcat=3610, john=None, extended=True),
            HashMode(name='md5($salt.md5($pass))', hashcat=3710, john=None, extended=True),
            HashMode(name='md5($pass.md5($salt))', hashcat=3720, john=None, extended=True),
            HashMode(name='md5($salt.$pass.$salt)', hashcat=3810, john=None, extended=True),
            HashMode(name='md5(md5($pass).md5($salt))', hashcat=3910, john=None, extended=True),
            HashMode(name='md5($salt.md5($salt.$pass))', hashcat=4010, john=None, extended=True),
            HashMode(name='md5($salt.md5($pass.$salt))', hashcat=4110, john=None, extended=True),
            HashMode(name='md5($username.0.$pass)', hashcat=4210, john=None, extended=True),
            HashMode(name='Skype', hashcat=23, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$NT\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='NTLM', hashcat=1000, john='nt', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}(:[^\\\/:*?"<>|]{1,20})?$', re.IGNORECASE),
        modes=[
            HashMode(name='Domain Cached Credentials', hashcat=1100, john='mscach', extended=False),
            HashMode(name='mscash', hashcat=1100, john='mscach', extended=True)]),
    Prototype(
        regex=re.compile(r'^(\$DCC2\$10240#[^\\\/:*?"<>|]{1,20}#)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='Domain Cached Credentials 2', hashcat=2100, john='mscach2', extended=False),
            HashMode(name='mscash2', hashcat=2100, john='mscach2', extended=True)]),
    Prototype(
        regex=re.compile(r'^{SHA}[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-1(Base64)', hashcat=101, john='nsldap', extended=False),
            HashMode(name='Netscape LDAP SHA', hashcat=101, john='nsldap', extended=False),
            HashMode(name='nsldap', hashcat=101, john='nsldap', extended=True)]),
    Prototype(
        regex=re.compile(r'^\$1\$[a-z0-9\/.]{0,8}\$[a-z0-9\/.]{22}(:.*)?$', re.IGNORECASE),
        modes=[
            HashMode(name='MD5 Crypt', hashcat=500, john='md5crypt', extended=False),
            HashMode(name='Cisco-IOS(MD5)', hashcat=500, john='md5crypt', extended=False),
            HashMode(name='FreeBSD MD5', hashcat=500, john='md5crypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='Lineage II C4', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$H\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashMode(name='phpBB v3.x', hashcat=400, john='phpass', extended=False),
            HashMode(name='Wordpress v2.6.0/2.6.1', hashcat=400, john='phpass', extended=False),
            HashMode(name="PHPass' Portable Hash", hashcat=400, john='phpass', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$P\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'Wordpress ≥ v2.6.2', hashcat=400, john=None, extended=False),
            HashMode(name=u'Joomla ≥ v2.5.18', hashcat=400, john=None, extended=False),
            HashMode(name="PHPass' Portable Hash", hashcat=400, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[a-z0-9]{2}$', re.IGNORECASE),
        modes=[
            HashMode(name='osCommerce', hashcat=21, john=None, extended=False),
            HashMode(name='xt:Commerce', hashcat=21, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$apr1\$[a-z0-9\/.]{0,8}\$[a-z0-9\/.]{22}$', re.IGNORECASE),
        modes=[
            HashMode(name='MD5(APR)', hashcat=1600, john=None, extended=False),
            HashMode(name='Apache MD5', hashcat=1600, john=None, extended=False),
            HashMode(name='md5apr1', hashcat=1600, john=None, extended=True)]),
    Prototype(
        regex=re.compile(r'^{smd5}[a-z0-9$\/.]{31}$', re.IGNORECASE),
        modes=[
            HashMode(name='AIX(smd5)', hashcat=6300, john='aix-smd5', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='WebEdition CMS', hashcat=3721, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{5}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'IP.Board ≥ v2+', hashcat=2811, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{8}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'MyBB ≥ v1.2+', hashcat=2811, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{34}$', re.IGNORECASE),
        modes=[
            HashMode(name='CryptoCurrency(Adress)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}(:.+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-1', hashcat=100, john='raw-sha1', extended=False),
            HashMode(name='Double SHA-1', hashcat=4500, john=None, extended=False),
            HashMode(name='RIPEMD-160', hashcat=6000, john='ripemd-160', extended=False),
            HashMode(name='Haval-160', hashcat=None, john=None, extended=False),
            HashMode(name='Tiger-160', hashcat=None, john=None, extended=False),
            HashMode(name='HAS-160', hashcat=None, john=None, extended=False),
            HashMode(name='LinkedIn', hashcat=190, john='raw-sha1-linkedin', extended=False),
            HashMode(name='Skein-256(160)', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-512(160)', hashcat=None, john=None, extended=False),
            HashMode(name='MangosWeb Enhanced CMS', hashcat=None, john=None, extended=True),
            HashMode(name='sha1(sha1(sha1($pass)))', hashcat=4600, john=None, extended=True),
            HashMode(name='sha1(md5($pass))', hashcat=4700, john=None, extended=True),
            HashMode(name='sha1($pass.$salt)', hashcat=110, john=None, extended=True),
            HashMode(name='sha1($salt.$pass)', hashcat=120, john=None, extended=True),
            HashMode(name='sha1(unicode($pass).$salt)', hashcat=130, john=None, extended=True),
            HashMode(name='sha1($salt.unicode($pass))', hashcat=140, john=None, extended=True),
            HashMode(name='HMAC-SHA1 (key = $pass)', hashcat=150, john=None, extended=True),
            HashMode(name='HMAC-SHA1 (key = $salt)', hashcat=160, john=None, extended=True),
            HashMode(name='sha1($salt.$pass.$salt)', hashcat=4710, john=None, extended=True)]),
    Prototype(
        regex=re.compile(r'^\*[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='MySQL5.x', hashcat=300, john='mysql-sha1', extended=False),
            HashMode(name='MySQL4.1', hashcat=300, john='mysql-sha1', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{43}$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco-IOS(SHA-256)', hashcat=5700, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^{SSHA}[a-z0-9\/+]{38}==$', re.IGNORECASE),
        modes=[
            HashMode(name='SSHA-1(Base64)', hashcat=111, john=None, extended=False),
            HashMode(name='Netscape LDAP SSHA', hashcat=111, john='ssha', extended=False),
            HashMode(name='nsldaps', hashcat=111, john=None, extended=True)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9=]{47}$', re.IGNORECASE),
        modes=[
            HashMode(name='Fortigate(FortiOS)', hashcat=7000, john='fortigate', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{48}$', re.IGNORECASE),
        modes=[
            HashMode(name='Haval-192', hashcat=None, john=None, extended=False),
            HashMode(name='Tiger-192', hashcat=None, john='tiger', extended=False),
            HashMode(name='SHA-1(Oracle)', hashcat=None, john=None, extended=False),
            HashMode(name='OSX v10.4', hashcat=122, john='xsha', extended=False),
            HashMode(name='OSX v10.5', hashcat=122, john='xsha', extended=False),
            HashMode(name='OSX v10.6', hashcat=122, john='xsha', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{51}$', re.IGNORECASE),
        modes=[
            HashMode(name='Palshop CMS', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{51}$', re.IGNORECASE),
        modes=[
            HashMode(name='CryptoCurrency(PrivateKey)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^{ssha1}[a-z0-9$\/.]{47}$', re.IGNORECASE),
        modes=[
            HashMode(name='AIX(ssha1)', hashcat=6700, john='aix-ssha1', extended=False)]),
    Prototype(
        regex=re.compile(r'^0x0100[a-f0-9]{48}$', re.IGNORECASE),
        modes=[
            HashMode(name='MSSQL(2005)', hashcat=132, john='mssql05', extended=False),
            HashMode(name='MSSQL(2008)', hashcat=132, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$md5,rounds=[0-9]+\$|\$md5\$rounds=[0-9]+\$|\$md5\$)[a-z0-9\/.]{0,16}(\$|\$\$)[a-z0-9\/.]{22}$', re.IGNORECASE),
        modes=[
            HashMode(name='Sun MD5 Crypt', hashcat=3300, john='sunmd5', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{56}$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-224', hashcat=None, john='raw-sha224', extended=False),
            HashMode(name='Haval-224', hashcat=None, john=None, extended=False),
            HashMode(name='SHA3-224', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-256(224)', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-512(224)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$2[axy]|\$2)\$[0-9]{0,2}?\$[a-z0-9\/.]{53}$', re.IGNORECASE),
        modes=[
            HashMode(name='Blowfish(OpenBSD)', hashcat=3200, john='bcrypt', extended=False),
            HashMode(name='Woltlab Burning Board 4.x', hashcat=None, john=None, extended=False),
            HashMode(name='BCrypt', hashcat=3200, john='bcrypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}:[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='Android PIN', hashcat=5800, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(S:)?[a-f0-9]{40}(:)?[a-f0-9]{20}$', re.IGNORECASE),
        modes=[
            HashMode(name='Oracle 11g/12c', hashcat=112, john='oracle11', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$bcrypt-sha256\$(2[axy]|2)\,[0-9]+\$[a-z0-9\/.]{22}\$[a-z0-9\/.]{31}$', re.IGNORECASE),
        modes=[
            HashMode(name='BCrypt(SHA-256)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{3}$', re.IGNORECASE),
        modes=[
            HashMode(name='vBulletin < v3.8.5', hashcat=2611, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:.{30}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'vBulletin ≥ v3.8.5', hashcat=2711, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$snefru\$)?[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='Snefru-256', hashcat=None, john='snefru-256', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{64}(:.+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-256', hashcat=1400, john='raw-sha256', extended=False),
            HashMode(name='RIPEMD-256', hashcat=None, john=None, extended=False),
            HashMode(name='Haval-256', hashcat=None, john='haval-256-3', extended=False),
            HashMode(name='GOST R 34.11-94', hashcat=6900, john='gost', extended=False),
            HashMode(name='SHA3-256', hashcat=5000, john='raw-keccak-256', extended=False),
            HashMode(name='Skein-256', hashcat=None, john='skein-256', extended=False),
            HashMode(name='Skein-512(256)', hashcat=None, john=None, extended=False),
            HashMode(name='Ventrilo', hashcat=None, john=None, extended=True),
            HashMode(name='sha256($pass.$salt)', hashcat=1410, john=None, extended=True),
            HashMode(name='sha256($salt.$pass)', hashcat=1420, john=None, extended=True),
            HashMode(name='sha256(unicode($pass).$salt)', hashcat=1430, john=None, extended=True),
            HashMode(name='sha256($salt.unicode($pass))', hashcat=1440, john=None, extended=True),
            HashMode(name='HMAC-SHA256 (key = $pass)', hashcat=1450, john=None, extended=True),
            HashMode(name='HMAC-SHA256 (key = $salt)', hashcat=1460, john=None, extended=True)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[a-z0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='Joomla < v2.5.18', hashcat=11, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f-0-9]{32}:[a-f-0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='SAM(LM_Hash:NT_Hash)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$chap\$0\*)?[a-f0-9]{32}[\*:][a-f0-9]{32}(:[0-9]{2})?$', re.IGNORECASE),
        modes=[
            HashMode(name='MD5(Chap)', hashcat=4800, john='chap', extended=False),
            HashMode(name='iSCSI CHAP Authentication', hashcat=4800, john='chap', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$episerver\$\*0\*[a-z0-9*\/=+]{52,53}$', re.IGNORECASE),
        modes=[
            HashMode(name='EPiServer 6.x < v4', hashcat=141, john='episerver', extended=False)]),
    Prototype(
        regex=re.compile(r'^{ssha256}[a-z0-9$\/.]{63}$', re.IGNORECASE),
        modes=[
            HashMode(name='AIX(ssha256)', hashcat=6400, john='aix-ssha256', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{80}$', re.IGNORECASE),
        modes=[
            HashMode(name='RIPEMD-320', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$episerver\$\*1\*[a-z0-9=*+]{68}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'EPiServer 6.x ≥ v4', hashcat=1441, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^0x0100[a-f0-9]{88}$', re.IGNORECASE),
        modes=[
            HashMode(name='MSSQL(2000)', hashcat=131, john='mssql', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{96}$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-384', hashcat=10800, john='raw-sha384', extended=False),
            HashMode(name='SHA3-384', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-512(384)', hashcat=None, john=None, extended=False),
            HashMode(name='Skein-1024(384)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^{SSHA512}[a-z0-9\/+]{96}$', re.IGNORECASE),
        modes=[
            HashMode(name='SSHA-512(Base64)', hashcat=1711, john='ssha512', extended=False),
            HashMode(name='LDAP(SSHA-512)', hashcat=1711, john='ssha512', extended=False)]),
    Prototype(
        regex=re.compile(r'^{ssha512}[0-9]{2}\$[a-z0-9\/.]{16,48}\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashMode(name='AIX(ssha512)', hashcat=6500, john='aix-ssha512', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{128}(:.+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-512', hashcat=1700, john='raw-sha512', extended=False),
            HashMode(name='Whirlpool', hashcat=6100, john='whirlpool', extended=False),
            HashMode(name='Salsa10', hashcat=None, john=None, extended=False),
            HashMode(name='Salsa20', hashcat=None, john=None, extended=False),
            HashMode(name='SHA3-512', hashcat=None, john='raw-keccak', extended=False),
            HashMode(name='Skein-512', hashcat=None, john='skein-512', extended=False),
            HashMode(name='Skein-1024(512)', hashcat=None, john=None, extended=False),
            HashMode(name='sha512($pass.$salt)', hashcat=1710, john=None, extended=True),
            HashMode(name='sha512($salt.$pass)', hashcat=1720, john=None, extended=True),
            HashMode(name='sha512(unicode($pass).$salt)', hashcat=1730, john=None, extended=True),
            HashMode(name='sha512($salt.unicode($pass))', hashcat=1740, john=None, extended=True),
            HashMode(name='HMAC-SHA512 (key = $pass)', hashcat=1750, john=None, extended=True),
            HashMode(name='HMAC-SHA512 (key = $salt)', hashcat=1760, john=None, extended=True)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{136}$', re.IGNORECASE),
        modes=[
            HashMode(name='OSX v10.7', hashcat=1722, john='xsha512', extended=False)]),
    Prototype(
        regex=re.compile(r'^0x0200[a-f0-9]{136}$', re.IGNORECASE),
        modes=[
            HashMode(name='MSSQL(2012)', hashcat=1731, john='msql12', extended=False),
            HashMode(name='MSSQL(2014)', hashcat=1731, john='msql12', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$ml\$[0-9]+\$[a-f0-9]{64}\$[a-f0-9]{128}$', re.IGNORECASE),
        modes=[
            HashMode(name='OSX v10.8', hashcat=7100, john='pbkdf2-hmac-sha512', extended=False),
            HashMode(name='OSX v10.9', hashcat=7100, john='pbkdf2-hmac-sha512', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}$', re.IGNORECASE),
        modes=[
            HashMode(name='Skein-1024', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^grub\.pbkdf2\.sha512\.[0-9]+\.[a-f0-9]{128,2048}\.[a-f0-9]{128}$', re.IGNORECASE),
        modes=[
            HashMode(name='GRUB 2', hashcat=7200, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^sha1\$[a-f0-9]{1,}\$[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(SHA-1)', hashcat=124, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{49}$', re.IGNORECASE),
        modes=[
            HashMode(name='Citrix Netscaler', hashcat=8100, john='citrix_ns10', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$S\$[a-z0-9\/.]{52}$', re.IGNORECASE),
        modes=[
            HashMode(name='Drupal > v7.x', hashcat=7900, john='drupal7', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$5\$(rounds=[0-9]+\$)?[a-z0-9\/.]{0,16}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-256 Crypt', hashcat=7400, john='sha256crypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{4}[a-f0-9]{16}[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='Sybase ASE', hashcat=8000, john='sybasease', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$6\$(rounds=[0-9]+\$)?[a-z0-9\/.]{0,16}\$[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-512 Crypt', hashcat=1800, john='sha512crypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$sha\$[a-z0-9]{1,16}\$([a-f0-9]{32}|[a-f0-9]{40}|[a-f0-9]{64}|[a-f0-9]{128}|[a-f0-9]{140})$', re.IGNORECASE),
        modes=[
            HashMode(name='Minecraft(AuthMe Reloaded)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^sha256\$[a-f0-9]{1,}\$[a-f0-9]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(SHA-256)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^sha384\$[a-f0-9]{1,}\$[a-f0-9]{96}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(SHA-384)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^crypt1:[a-z0-9+=]{12}:[a-z0-9+=]{12}$', re.IGNORECASE),
        modes=[
            HashMode(name='Clavister Secure Gateway', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{112}$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco VPN Client(PCF-File)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{1329}$', re.IGNORECASE),
        modes=[
            HashMode(name='Microsoft MSTSC(RDP-File)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[^\\\/:*?"<>|]{1,20}::[^\\\/:*?"<>|]{1,20}:[a-f0-9]{48}:[a-f0-9]{48}:[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='NetNTLMv1-VANILLA / NetNTLMv1+ESS', hashcat=5500, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[^\\\/:*?"<>|]{1,20}::[^\\\/:*?"<>|]{1,20}:[a-f0-9]{16}:[a-f0-9]{32}:[a-f0-9]+$', re.IGNORECASE),
        modes=[
            HashMode(name='NetNTLMv2', hashcat=5600, john='netntlmv2', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$(krb5pa|mskrb5)\$([0-9]{2})?\$.+\$[a-f0-9]{1,}$', re.IGNORECASE),
        modes=[
            HashMode(name='Kerberos 5 AS-REQ Pre-Auth', hashcat=7500, john='krb5pa-md5', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$scram\$[0-9]+\$[a-z0-9\/.]{16}\$sha-1=[a-z0-9\/.]{27},sha-256=[a-z0-9\/.]{43},sha-512=[a-z0-9\/.]{86}$', re.IGNORECASE),
        modes=[
            HashMode(name='SCRAM Hash', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}:[a-f0-9]{0,32}$', re.IGNORECASE),
        modes=[
            HashMode(name='Redmine Project Management Web App', hashcat=7600, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(.+)?\$[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='SAP CODVN B (BCODE)', hashcat=7700, john='sapb', extended=False)]),
    Prototype(
        regex=re.compile(r'^(.+)?\$[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='SAP CODVN F/G (PASSCODE)', hashcat=7800, john='sapg', extended=False)]),
    Prototype(
        regex=re.compile(r'^(.+\$)?[a-z0-9\/.]{30}(:.+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='Juniper Netscreen/SSG(ScreenOS)', hashcat=22, john='md5ns', extended=False)]),
    Prototype(
        regex=re.compile(r'^0x[a-f0-9]{60}\s0x[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='EPi', hashcat=123, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{40}:[^*]{1,25}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'SMF ≥ v1.1', hashcat=121, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$wbb3\$\*1\*)?[a-f0-9]{40}[:*][a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='Woltlab Burning Board 3.x', hashcat=8400, john='wbb3', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{130}(:[a-f0-9]{40})?$', re.IGNORECASE),
        modes=[
            HashMode(name='IPMI2 RAKP HMAC-SHA1', hashcat=7300, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{32}:[0-9]+:[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$', re.IGNORECASE),
        modes=[
            HashMode(name='Lastpass', hashcat=6800, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/.]{16}([:$].{1,})?$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco-ASA(MD5)', hashcat=2410, john='asa-md5', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$vnc\$\*[a-f0-9]{32}\*[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='VNC', hashcat=None, john='vnc', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9]{32}(:([a-z0-9-]+\.)?[a-z0-9-.]+\.[a-z]{2,7}:.+:[0-9]+)?$', re.IGNORECASE),
        modes=[
            HashMode(name='DNSSEC(NSEC3)', hashcat=8300, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(user-.+:)?\$racf\$\*.+\*[a-f0-9]{16}$', re.IGNORECASE),
        modes=[
            HashMode(name='RACF', hashcat=8500, john='racf', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$3\$\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='NTHash(FreeBSD Variant)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$sha1\$[0-9]+\$[a-z0-9\/.]{0,64}\$[a-z0-9\/.]{28}$', re.IGNORECASE),
        modes=[
            HashMode(name='SHA-1 Crypt', hashcat=None, john='sha1crypt', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{70}$', re.IGNORECASE),
        modes=[
            HashMode(name='hMailServer', hashcat=1421, john='hmailserver', extended=False)]),
    Prototype(
        regex=re.compile(r'^[:\$][AB][:\$]([a-f0-9]{1,8}[:\$])?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='MediaWiki', hashcat=3711, john='mediawiki', extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{140}$', re.IGNORECASE),
        modes=[
            HashMode(name='Minecraft(xAuth)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$pbkdf2-sha(1|256|512)\$[0-9]+\$[a-z0-9\/.]{22}\$([a-z0-9\/.]{27}|[a-z0-9\/.]{43}|[a-z0-9\/.]{86})$', re.IGNORECASE),
        modes=[
            HashMode(name='PBKDF2(Generic)', hashcat=None, john='pbkdf2-hmac-sha256', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$[0-9]+\$[a-z0-9\/+=-]+\$[a-z0-9\/+-]{27}=$', re.IGNORECASE),
        modes=[
            HashMode(name='PBKDF2(Cryptacular)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$p5k2\$[0-9]+\$[a-z0-9\/.]+\$[a-z0-9\/.]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='PBKDF2(Dwayne Litzenberger)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^{FSHP[0123]\|[0-9]+\|[0-9]+}[a-z0-9\/+=]+$', re.IGNORECASE),
        modes=[
            HashMode(name='Fairly Secure Hashed Password', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$PHPS\$.+\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='PHPS', hashcat=2612, john='phps', extended=False)]),
    Prototype(
        regex=re.compile(r'^[0-9]{4}:[a-f0-9]{16}:[a-f0-9]{2080}$', re.IGNORECASE),
        modes=[
            HashMode(name='1Password(Agile Keychain)', hashcat=6600, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{64}:[a-f0-9]{32}:[0-9]{5}:[a-f0-9]{608}$', re.IGNORECASE),
        modes=[
            HashMode(name='1Password(Cloud Keychain)', hashcat=8200, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='IKE-PSK MD5', hashcat=5300, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{256}:[a-f0-9]{256}:[a-f0-9]{16}:[a-f0-9]{16}:[a-f0-9]{320}:[a-f0-9]{16}:[a-f0-9]{40}:[a-f0-9]{40}:[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='IKE-PSK SHA1', hashcat=5400, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashMode(name='PeopleSoft', hashcat=133, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^crypt\$[a-f0-9]{5}\$[a-z0-9\/.]{13}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(DES Crypt Wrapper)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$django\$\*1\*)?pbkdf2_sha256\$[0-9]+\$[a-z0-9]{1,}\$[a-z0-9\/+]{43}=$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(PBKDF2-HMAC-SHA256)', hashcat=10000, john='django', extended=False)]),
    Prototype(
        regex=re.compile(r'^pbkdf2_sha1\$[0-9]+\$[a-z0-9]{1,}\$[a-z0-9\/+]{27}=$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(PBKDF2-HMAC-SHA1)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^bcrypt(\$2[axy]|\$2)\$[0-9]{0,2}?\$[a-z0-9\/.]{53}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(BCrypt)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^md5\$[a-f0-9]{1,}\$[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='Django(MD5)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\{PKCS5S2\}[a-z0-9\/+]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='PBKDF2(Atlassian)', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^md5[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='PostgreSQL MD5', hashcat=None, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\([a-z0-9\/+]{49}\)$', re.IGNORECASE),
        modes=[
            HashMode(name='Lotus Notes/Domino 8', hashcat=9100, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^SCRYPT:[0-9]{1,}:[0-9]{1}:[0-9]{1}:[a-z0-9:\/+=]{1,}$', re.IGNORECASE),
        modes=[
            HashMode(name='scrypt', hashcat=8900, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$8\$[a-z0-9\/.]{14}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco Type 8', hashcat=9200, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$9\$[a-z0-9\/.]{14}\$[a-z0-9\/.]{43}$', re.IGNORECASE),
        modes=[
            HashMode(name='Cisco Type 9', hashcat=9300, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2007\*[0-9]{2}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name='Microsoft Office 2007', hashcat=9400, john='office', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2010\*[0-9]{6}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='Microsoft Office 2010', hashcat=9500, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$office\$\*2013\*[0-9]{6}\*[0-9]{3}\*[0-9]{2}\*[a-z0-9]{32}\*[a-z0-9]{32}\*[a-z0-9]{64}$', re.IGNORECASE),
        modes=[
            HashMode(name='Microsoft Office 2013', hashcat=9600, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$fde\$[0-9]{2}\$[a-f0-9]{32}\$[0-9]{2}\$[a-f0-9]{32}\$[a-f0-9]{3072}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'Android FDE ≤ 4.3', hashcat=8800, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^\$oldoffice\$[01]\*[a-f0-9]{32}\*[a-f0-9]{32}\*[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'Microsoft Office ≤ 2003 (MD5+RC4)', hashcat=9700, john='oldoffice', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$oldoffice\$[34]\*[a-f0-9]{32}\*[a-f0-9]{32}\*[a-f0-9]{40}$', re.IGNORECASE),
        modes=[
            HashMode(name=u'Microsoft Office ≤ 2003 (SHA1+RC4)', hashcat=9800, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^(\$radmin2\$)?[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='RAdmin v2.x', hashcat=9900, john='radmin', extended=False)]),
    Prototype(
        regex=re.compile(r'^{x-issha,\s[0-9]{4}}[a-z0-9\/+=]+$', re.IGNORECASE),
        modes=[
            HashMode(name='SAP CODVN H (PWDSALTEDHASH) iSSHA-1', hashcat=10300, john='saph', extended=False)]),
    Prototype(
        regex=re.compile(r'^\$cram_md5\$[a-z0-9\/+=-]+\$[a-z0-9\/+=-]{52}$', re.IGNORECASE),
        modes=[
            HashMode(name='CRAM-MD5', hashcat=10200, john=None, extended=False)]),
    Prototype(
        regex=re.compile(r'^[a-f0-9]{16}:2:4:[a-f0-9]{32}$', re.IGNORECASE),
        modes=[
            HashMode(name='SipHash', hashcat=10100, john=None, extended=False)])
]


class HashID(object):

    """HashID with configurable prototypes"""

    def __init__(self, prototypes=prototypes):
        super(HashID, self).__init__()

        # Set self.prototypes to a copy of prototypes to allow
        # modification after instantiation
        self.prototypes = list(prototypes)

    def identifyHash(self, phash):
        """Returns identified HashMode"""
        phash = phash.strip()
        for prototype in self.prototypes:
            if prototype.regex.match(phash):
                for mode in prototype.modes:
                    yield mode


def writeResult(candidate, identified_modes, outfile=sys.stdout, hashcatMode=False, johnFormat=False, extended=False):
    """Create human readable output from identifyHash"""
    outfile.write(u"Analyzing '{0}'\n".format(candidate))
    count = 0
    append = ""
    for mode in identified_modes:
        if not extended:
            if not mode.extended:
                if hashcatMode and mode.hashcat is not None:
                    append += "[Hashcat Mode: {0}]".format(mode.hashcat)
                if johnFormat and mode.john is not None:
                    append += "[JtR Format: {0}]".format(mode.john)
                outfile.write(u"[+] {0} {1}\n".format(mode.name, append))
                append = ""
        else:
            if hashcatMode and mode.hashcat is not None:
                append += "[Hashcat Mode: {0}]".format(mode.hashcat)
            if johnFormat and mode.john is not None:
                append += "[JtR Format: {0}]".format(mode.john)
            outfile.write(u"[+] {0} {1}\n".format(mode.name, append))
            append = ""
        count += 1
    if count == 0:
        outfile.write(u"[+] Unknown hash\n")
    return (count > 0)


def main():
    usage = "{0} [-a] [-m] [-j] [--help] [--version] INPUT".format(os.path.basename(__file__))
    banner = "hashID v{0} by {1} ({2})".format(__version__, __author__, __github__)
    description = "Identify the different types of hashes used to encrypt data"

    parser = argparse.ArgumentParser(usage=usage, description=description, epilog=__license__)
    parser.add_argument("strings", metavar="input", type=str, nargs="*", help="string or filename to analyze")
    parser.add_argument("-a", "--all", action="store_true", help="list all possible hash algorithms including salted passwords")
    parser.add_argument("-m", "--mode", action="store_true", help="include corresponding Hashcat mode in output")
    parser.add_argument("-j", "--john", action="store_true", help="include corresponding JohnTheRipper format in output")
    parser.add_argument("--version", action="version", version=banner)
    args = parser.parse_args()

    hashID = HashID()

    if not args.strings or args.strings[0] == "-":
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            writeResult(line.strip(), hashID.identifyHash(line.strip()), sys.stdout, args.mode, args.john, args.all)
            sys.stdout.flush()
    else:
        for string in args.strings:
            if os.path.isfile(string):
                try:
                    with io.open(string, "r", encoding="utf-8") as infile:
                        print("--File '{0}'--".format(string))
                        for line in infile:
                            if line.strip():
                                writeResult(line.strip(), hashID.identifyHash(line.strip()), sys.stdout, args.mode, args.john, args.all)
                    infile.close()
                except IOError:
                    print("--File '{0}' - could not open--".format(string))
                else:
                    print("--End of file '{0}'--".format(string))
            else:
                writeResult(string, hashID.identifyHash(string), sys.stdout, args.mode, args.john, args.all)


if __name__ == "__main__":
    main()
