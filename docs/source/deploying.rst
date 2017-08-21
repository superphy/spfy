================
Deplyoment Guide
================

.. contents:: Table of Contents
   :local:

Deploying to Corefacility
=========================

Things to Note: Filesystem
--------------------------

Looking at the filesystem:

.. code-block:: sh

	[claing@superphy backend-4.3.3]$ df -h
	Filesystem                 Size  Used Avail Use% Mounted on
	/dev/mapper/superphy-root   45G   31G   14G  69% /
	devtmpfs                    12G     0   12G   0% /dev
	tmpfs                       12G  2.5G  9.3G  21% /dev/shm
	tmpfs                       12G   26M   12G   1% /run
	tmpfs                       12G     0   12G   0% /sys/fs/cgroup
	/dev/vda1                  497M  240M  258M  49% /boot
	/dev/mapper/docker-docker  200G   21G  180G  11% /docker
	warehouse:/ifs/Warehouse   769T  601T  151T  81% /Warehouse
	tmpfs                      2.4G     0  2.4G   0% /run/user/40151
	tmpfs                      2.4G     0  2.4G   0% /run/user/40290

``/Warehouse`` is used for long-term data storage and shared across the NML. 
