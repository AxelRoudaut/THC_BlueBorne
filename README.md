# THC_BlueBorne
"Projet long" TLS-SEC: réalisation de challenges tutoriel pour la *Toulouse Hacking Convention*. Ce tuto consiste en l'explication et la démonstration d'exploitation de 2 vulnérabilités présentes dans la pile protocolaire Bluetooth. Ce projet reprend en très grande partie les [travaux de recherches  **BlueBorne**](https://www.armis.com/blueborne/) par Armis Labs. ([ici le papier de recherche technique](http://go.armis.com/hubfs/BlueBorne%20Technical%20White%20Paper-1.pdf?t=1517293112971)).

Les 2 vulnérabilités présentées ici sont présentes uniquement pour les systèmes Linux utilisant l'implémentation native Bluez pour les communications Bluetooth.
- La première vulnérabilité est la CVE-2017-1000250 consistant en une fuite de donnée de la *Heap* par l'implémentation d'une fonction du protocole SDP et pouvant conduire à la divulgation de données hautement sensibles.
- La seconde vulnérabilité est la CVE-2017-1000251 consistant au déni de service (voir du contôle distant) d'un système par un *buffer overflow* provoqué par la mauvaise implémentation d'une fonction du protocole L2CAP.

## 1. Installation

Pour la démonstration de ces 2 vulnérabilités nous aurons besoins de 2 systèmes Linux distincts et 2 interfaces Bluetooth.
Pour ma part j'ai utilisé comme système d'attaque une Raspberry Pi avec un dongle bluetooth que je contrôle par ssh avec une VM Kali ainsi qu'une VM Ubuntu (configurée comme ci-dessous) avec un 2eme dongle Bluetooth comme système victime.

Paquets requis:
```
sudo apt-get install git vim libbluetooth-dev bluetooth bluez blueman libffi-dev libssl-dev build-essential
(si raspberry pi : installer également le paquet pi-bluetooth)
```

Pour démarrer le service Bluetooth:
```
sudo systemctl start bluetooth.service
```
Pour voir et contrôler les interfaces Bluetooth:
```
hciconfig -a
sudo bluetoothctl
```
[Comment activer le Bluetooth avec VirtualBox](https://scribles.net/enabling-bluetooth-in-virtualbox/)

### Configuration du système cible

Selon les [recherches d'Armis Labs](https://www.armis.com/blueborne/):
> All Linux devices running BlueZ are affected by the information leak vulnerability (CVE-2017-1000250).

> All Linux devices from version 2.6.32 (released in July 2009) until version 4.14 are affected by the remote code execution vulnerability (CVE-2017-1000251)


Voici la [liste détaillée](https://www.securityfocus.com/bid/100809) des systèmes impactés

Selon [wiki.ubuntu.com](https://wiki.ubuntu.com/SecurityTeam/KnowledgeBase/BlueBorne):
> Ubuntu 14.04 LTS, Ubuntu 16.04 LTS, and Ubuntu 17.04 were affected

J'ai donc choisi de prendre comme cible un système 16.04.03 Ubuntu que je fait tourner dans Virtualbox.
J'ai rétrogradé la version du Kernel Linux à la version 4.13 en suivant [ce guide](http://ubuntuhandbook.org/index.php/2017/09/install-linux-kernel-4-13-ubuntu-16-04-higher/).

Vous pouvez vérifier le succès de cette opération avec la commande:
```
uname -r
4.13.0-041300-generic
``` 

Il faut également vérifier que vous disposez bien de la version vulnérable de Bluez sur votre Ubuntu cible. En effet, il vous faut une version antérieur à la version `5.37-0ubuntu5.1` (cette dernière étant le fix pour la CVE-2017-1000250 selon [Ubuntu bluez package](https://launchpad.net/ubuntu/+source/bluez/5.37-0ubuntu5.1)).

Vous pouvez vérifier celà avec la commande:
```
dpkg --status bluez | grep '^Version:'

Version: 5.37-0ubuntu5.1    == MAUVAIS
Version: 5.37-0ubuntu5      == BON
```
Si vous n'avez pas la bonne version:
```
sudo apt-get purge bluez
sudo apt-get install bluez=5.37-0ubuntu5
```
ou manuellement si vous avez choisi une autre distribution que Ubuntu:
```
Download (cf https://launchpad.net/ubuntu/+source/bluez/5.37-0ubuntu5)
============================
wget https://launchpad.net/ubuntu/+archive/primary/+files/bluez_5.37.orig.tar.xz
tar xf bluez_5.37.orig.tar.xz
or
https://launchpad.net/ubuntu/+archive/primary/+files/bluez_5.37-0ubuntu5.dscc
dpkg-source -x bluez_5.37-0ubuntu1.dsc

Compilation and installation
============================

In order to compile Bluetooth utilities you need following software packages:
  - GCC compiler
  - GLib library
  - D-Bus library
  - udev library (optional)
  - readline (command line clients)
sudo apt-get install gcc glib2.0 libdbus-1-dev libudev-dev libical-dev libreadline-dev

To configure run:
cd bluez-5.37/
./configure --prefix=/usr --mandir=/usr/share/man --sysconfdir=/etc --localstatedir=/var

Configure automatically searches for all required components and packages.

To compile and install run as root:
make && make install
```

Vérifiez que le Bluetooth fonctionne et est en mode **découvrable** chez la victime avant toutes exploitations:
```
hciconfig  # must have at least 1 interface
sudo bluetoothctl
  power on
  agent on
  discoverable on
```

Remarque: Pour pouvoir capturer des packets sur une interface bluetooth0 ou bluetooth1 installez:
```
sudo apt-get install libpcap0.8 libpcap0.8-dev libpcap-dev
```
Pour éviter de faire ramer la raspberry avec un affichage distant de Wireshark par `ssh -X`, nous allons capturer les flux Bluetooth avec tcpdump sur l'interface `bluetooth1`, envoyer ce flux sur un PC distant qui l'affichera avec son propre Wireshark.
```
ssh root@[addr raspberry] "sudo tcpdump -s 0 -U -n -i bluetooth1 -w -"  | sudo wireshark -k -i -
```
Plus d'info sur cette commande : [Creating a netcat pipe for wireshark for remote packet capture](https://www.techdodo.co.uk/creating-netcat-pipe-wireshark)

Remarque : Pour faciliter les connections ssh : [How To Set Up SSH Keys](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2) 

    
## 2. Exploits
  
  ### BlueBorne attack on Linux
- **Information leak vulnerability (CVE-2017-1000250)**
  Tous les périphériques Linux exécutant BlueZ sont affectés. Cette vulnérabilité réside dans le serveur SDP chargé d'identifier d'autres services utilisant Bluetooth autour de l'appareil. La faille permet à l'attaquant d'envoyer un ensemble de requêtes personnalisées au serveur, lui faisant divulguer des bits de mémoire en réponse. Cela peut être utilisé par un attaquant pour exposer des données sensibles du processus Bluetooth qui peuvent également contenir des clés de cryptage des communications Bluetooth. Ceux-ci peuvent être utilisés par l'attaquant pour initier une attaque qui ressemble beaucoup à une attaqua *HeartBleed*.
 
**Challenge 1** : Explications et Démonstration de cette vulnérabilité sur [LEAK_CVE-2017-1000250](https://github.com/AxelRoudaut/THC_BlueBorne/edit/master/LEAK_CVE-2017-1000250).
  
- **A stack overflow in BlueZ (CVE-2017-1000251)**
 Cette vulnérabilité a été trouvée dans la pile Bluetooth du noyau Linux, qui est le noyau même du système d'exploitation. Une faille interne dans le protocole L2CAP (Logical Link Control and Adaptation Protocol) utilisée pour se connecter entre deux périphériques provoque une corruption de la mémoire. Un attaquant peut utiliser cette corruption de mémoire pour obtenir le contrôle total de l'appareil. Cela fournit à un attaquant un exploit au niveau du noyau complet et fiable pour tout périphérique compatible Bluetooth sous Linux, ne nécessitant aucune étape supplémentaire. De plus, chaque hôte compromis peut être utilisé pour lancer des attaques secondaires, ce qui rend cette vulnérabilité vermifuge.

**Challenge 2** : Explications et Démonstration de cette vulnérabilité sur [DOS_CVE-2017-10002501](https://github.com/AxelRoudaut/THC_BlueBorne/tree/master/DOS_CVE-2017-10002501).

**Sources:**
  - [ArmisSecurity-BlueBorne-linux_bluez](https://github.com/ArmisSecurity/blueborne/tree/master/linux-bluez)
  - [White paper](https://go.armis.com/hubfs/ExploitingBlueBorneLinuxBasedIoTDevices.pdf?t=1517293112971)
  - [Blueborne explained at BlackHat EU 2017](https://www.youtube.com/watch?v=WWQTlogqF1I)
  - [Bluetooth Worm and Linux Exploit Revealed by Armis](https://www.armis.com/armis-demonstrates-bluetooth-worm-and-linux-exploit-at-black-hat/)
  - [Blueborne CVE-2017-1000251 PoC for linux machines](https://github.com/own2pwn/blueborne-CVE-2017-1000251-POC)
  - [Exploit CVE-2017-1000251](https://gitlab.com/marcinguy/kernel-exploitation/tree/master)
  - [littl tools](https://github.com/marsyy/littl_tools)  


## Protections and Mitigations
  Armis Guide: [PROTECTING THE ENTERPRISE FROM BLUEBORNE](http://go.armis.com/hubfs/BlueBorne%20Technical%20White%20Paper.pdf)
  
PS: Vous trouverez les sources pour plein d'autres exploitations Bluetooth sur le [wiki de ce répo](https://github.com/AxelRoudaut/THC_BlueBorne/wiki). 
    
    

