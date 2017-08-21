================
Deplyoment Guide
================

.. contents:: Table of Contents
   :local:

Deploying to Corefacility
=========================

Blazegraph
----------

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

``/Warehouse`` is used for long-term data storage and shared across the NML. In order to write to ``/Warehouse``, you need the permissions of either ``claing`` or ``superphy``; there are some problems with passing these permissions into Docker environments, so we run Blazegraph, inside of folder ``/Warehouse/Users/claing/superphy/spfy/docker-blazegraph/2.1.4-inferencing`` and as ``claing``, outside of Docker using:

.. code-block:: sh

	java -server -Xmx4g -Dbigdata.propertyFile=/Warehouse/Users/claing/superphy/spfy/docker-blazegraph/2.1.4-inferencing/RWStore.properties -jar blazegraph.jar

This command is run using ``screen`` allowing us to detach it from our shell.

.. code-block:: sh

	screen
	CTRL+a, d

and to resume:

.. code-block:: sh

	screen -r

See https://github.com/superphy/backend/issues/159

Docker Service
--------------

.. code-block:: sh

	[claing@superphy docker]$ sudo cat /etc/fstab

	#
	# /etc/fstab
	# Created by anaconda on Thu Dec 24 17:40:08 2015
	#
	# Accessible filesystems, by reference, are maintained under '/dev/disk'
	# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
	#
	/dev/mapper/superphy-root /                       xfs     defaults        1 1
	UUID=6c62e5cf-fd55-41e8-8122-e5e78643e3cd /boot                   xfs     defaults        1 2
	/dev/mapper/superphy-swap swap                    swap    defaults        0 0
	warehouse:/ifs/Warehouse	/Warehouse	nfs	defaults	0 0
	/dev/mapper/docker-docker /docker xfs defaults 1 2

Our root filesystem for the Corefacility VM is really small (45G) and we instead have a virtual drive at ``/dev/mapper/docker-docker `` which is mounted on ``/docker`` which has our Docker images / unmapped volumes. This is setup using symlinks:

.. code-block:: sh

	sudo systemctl stop docker
	cd /var/lib/
	sudo cp -rf docker/ /docker/backups/
	sudo rm -rf docker/
	sudo mkdir /docker/docker
	sudo ln -s /docker/docker /var/lib/docker
	sudo systemctl start docker
