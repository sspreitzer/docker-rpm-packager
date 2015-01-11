#!/usr/bin/env python2

import subprocess
import sys
import os
import re

def installReqs(package):
	reqs = []
	for line in open(package):
		rel = re.match('^BuildRequires:(.*)$', line)
		if rel is not None:
			reqs.append('\'' + rel.group(1).strip() + '\'')
	if reqs != []:
		print '>>> /usr/bin/yum install -y ' + ' '.join(reqs) + ' && yum clean -y all'
		return subprocess.call('/usr/bin/yum install -y ' + ' '.join(reqs) + ' && yum clean -y all', shell=True)
	else:
		return

def buildPackage(package):
	print '>>> /usr/bin/rpmbuild -ba ' + package
	return subprocess.call('/usr/bin/rpmbuild -ba ' + package, shell=True)

def doPackage(package):
	os.chdir('/rpmbuild/SPECS')
	os.access(package, os.R_OK)
	st = os.stat(package)
	os.chown(package, os.getuid(), os.getgid())
	installReqs(package)
	buildPackage(package)
	os.chown(package, st.st_uid, st.st_gid)

def main():
	if len(sys.argv) > 1:
		doPackage(sys.argv[1] + '.spec')
	else:
		os.execv('/bin/bash', ['bash'])

if __name__=='__main__':
	main()

