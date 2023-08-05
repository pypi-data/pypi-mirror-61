backupmystemusb2usb: Backup my system usb to usb
================================================

backupmystemusb2usb is a Creative Commons Python package to copy usb key.

Its runs on Python 3.7 and has a dependency for yaml, and another one for the gui.

Installation without the source
-------------------------------

To install *backupmysytemusb2usb* package run the following command:

.. code-block:: bash

   sudo apt-get install libyaml-dev python3-gi
   sudo -H pip3 install backupmystemusb2usb

You have to create a config.yml file (you can save it into your ~/.local/share/backupmysystemusb2usb directory)

.. code-block:: bash
   
   UUID_1_Master: 790d1fbb-96ed-46c3-868d-08e05e223fa7
   UUID_1_Slave: 790d1fbb-96ed-46c3-868d-08e05e223fa7
   Temp_img: /home/stephane/Temp/Linux.img
   Temp_log: /home/stephane/Temp/BackupMySystem-Temp.log
   Kill_dd: True

UUID list

.. code-block:: bash
   
   sudo blkid

Find your device and to change the label if the device master UUID is the same as the slave UUID (for exemple: if you cancel in copying temporary img to disk slave), you have to put a date upper on master than slave

*Warning* UUID is not Label !

.. code-block:: bash

   sudo e2label /dev/sd_1 "19991231235959"
   
For the deamon, write a *run.py* for running by user root with chmod 700

.. code-block:: bash

   #!/usr/bin/env python3
   import sys
   import yaml
   from backupmysystemusb2usb.usb2usb import usb2usb
   try:
      u2u = usb2usb(sys.argv[1])
      u2u.backup()
   except yaml.YAMLError:
      exit()

You can create a service systemd if you planed to backup your usb key every day in the morning. You can wakeonlan from a raspberrypi or with another technic

.. code-block:: bash

   wakeonlan MACADRESS
   crontab -e
   # write your cron
   sudo service cron reload

Now to create a daemon in startup (without console).

Use this name "backupmysystemusb2usb" because in source const.py this file is a constant for GUI progress for non-root user

.. code-block:: bash

   cd /etc/systemd/system
   vi backupmysystemusb2usb.service

Write
   
.. code-block:: bash

   [Unit]
   After=ssh.service

   [Service]
   WorkingDirectory=/your/working/path/
   ExecStart=/usr/bin/sh -c "/your/working/path/run.py /your/working/path/config.yml"

   [Install]
   WantedBy=default.target

Enable and start

.. code-block:: bash
   
   sudo systemctl daemon-reload
   sudo systemctl enable backupmysystemusb2usb

Then the service start on reboot.
If you will test now the service :

.. code-block:: bash

   sudo systemctl start backupmysystemusb2usb

Check the log (the last 20 messages)

.. code-block:: bash

   sudo journalctl --unit backupmysystemusb2usb -n 20

You can go to check your output log file configured by config.yml
   
Now we have to create the shell return for non-root user gui.py

.. code-block:: bash
   
   touch gui.py
   chmod 700 gui.py
   vi gui.py
  
And write in file

.. code-block:: bash

   #!/usr/bin/env python3
   import yaml
   from backupmysystemusb2usb.usb2usb import usb2usb
   u2u = usb2usb('/path/to/your/config.yml')
   u2u.gui()

You can create a autostart Gnome desktop startup

.. code-block:: bash

   cd ~/.config/autostart
   touch backupmysystemusb2usb.desktop
   chmod 744
   vi backupmysystemusb2usb.desktop

And in your editor enter

.. code-block:: bash

   [Desktop Entry]
   Name=Backup my system usb to usb
   Comment=Copy disk with the same space
   Exec=/your/working/path/gui.py
   Icon=org.gnome.Terminal
   Path=/your/working/path/
   Terminal=true
   Hidden=false
   Type=Application
   Categories=Utility;Application;

Installation from source
------------------------

To install the latest developement version run the following command:

.. code-block:: bash

   git clone https://github.com/stephaneworkspace/backupmysystemusb2usb

Versions
--------
1.04
 - Change license to Creative Commons

1.03
 - Change license to Creative Commons

1.02
 - Fix bug and rename label usb key

1.0.1
 - Add gui Gtk

0.0.16
 - Alpha version
