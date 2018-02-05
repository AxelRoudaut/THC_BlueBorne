# THC_BlueBorne
"Projet long" TLS-SEC: realization of a tutorial challenge for the Toulouse Hacking Convention. Exploit of the bluetooth vulnerability called Blueborne.

In this project, we are going to reproduce a POC of the bluetooth vulnerability. The main purpuse is to achieve to spread a worm using bluetooth communications using Linux and Android systems (and Windows system if we have enough time).
This project is mainly based on the [Armis BlueBorne researches](https://www.armis.com/blueborne/) and several open source github repositories.

## 0. Project progress

- [ ] Bluetooth Sniffer
- [ ] Vulnerability Scanner
- [ ] Android Exploit
- [ ] Linux Exploit
- [ ] Windows Exploit

## 1. Bluetooth Sniffer

  ### a. Hardware 
  We are going to use a NRF24L01+ Transceiver Module (with PA+LNA in order to have a better reach) to receive/emit bluetooth signals, connected to a Raspberry Pi 3 as follows:
  https://www.amazon.fr/Kuman-Emetteur-R%C3%A9cepteur-NRF24L01-Antistatique/dp/B06WD17WLS/ref=sr_1_1?ie=UTF8&qid=1517826874&sr=8-1&keywords=nrf24l01+%2B+pa+%2B+lna
  https://www.mysensors.org/build/raspberry
  https://forum.mysensors.org/topic/2437/step-by-step-procedure-to-connect-the-nrf24l01-to-the-gpio-pins-and-use-the-raspberry-as-a-serial-gateway-mysensors-1-x
  https://rlogiacco.wordpress.com/2014/02/26/nrf24-on-raspberry-pi/

  ### b. Firmware
  We are going to use existing bluetooth sniffer project:
  https://github.com/ArmisSecurity/blueborne/tree/master/nRF24_BDADDR_Sniffer
  https://github.com/DigitalSecurity/raspjack
  https://github.com/yetifrisstlama/nRF24L01-sniffer
    
  ### c. BlueBorne vulnerability scanner
  Bluetooth scanner for local devices that may be vulnerable to Blueborne exploit
  https://github.com/hook-s3c/blueborne-scanner
    
## 2. Exploits

  ### a. BlueBorne L2CAP Testing Framework
This direcotory contains a general testing framework to send and receive raw l2cap messages (using scapy). It is used to establish L2CAP connections, and allows the ability to control all l2cap messages sent in the process of creating the connection.

Sources:
  - [Original Armis code](https://github.com/ArmisSecurity/blueborne/tree/master/l2cap_infra)
  
  ### b. BlueBorne attack on Linux
- Information leak vulnerability (CVE-2017-1000250)
  All Linux devices running BlueZ are affected. This vulnerability resides in the SDP server responsible for identifying other services using Bluetooth around the device. The flaw allows the attacker to send a set of crafted requests to the server, causing it to disclose memory bits in response. This can be used by an attacker to expose sensitive data from the Bluetooth processthat may also contain encryption keys of Bluetooth communications. These can be used by the attacker to initiate an attack that very much resembles heartbleed.
  
- A stack overflow in BlueZ (CVE-2017-1000251)
  This vulnerability was found in the Bluetooth stack of the Linux Kernel, which is the very core of the operating system. An internal flaw in the L2CAP (Logical Link Control and Adaptation Protocol) that is used to connect between two devices causes a memory corruption. An attacker can use this memory corruption to gain full control of the device.
  
The following directory contains a PoC code for the Linux-RCE vulnerability (CVE-2017-1000251). The exploits are specifically tailored for specific fw images of two devices: The Amazon Echo and Samsung Gear S3.

Sources: 
  - [Orginal Armis code](https://github.com/ArmisSecurity/blueborne/tree/master/linux-bluez)
  - [White paper](https://go.armis.com/hubfs/ExploitingBlueBorneLinuxBasedIoTDevices.pdf?t=1517293112971)
  - [Blueborne explained at BlackHat EU 2017](https://www.youtube.com/watch?v=WWQTlogqF1I)
  - [Bluetooth Worm and Linux Exploit Revealed by Armis](https://www.armis.com/armis-demonstrates-bluetooth-worm-and-linux-exploit-at-black-hat/)
  - [Blueborne CVE-2017-1000251 PoC for linux machines](https://github.com/ojasookert/CVE-2017-0781)
  
Our contribution:

We are going to reproduce it using a vulnerable Linux image on a Raspberry Pi. We need a Linux Kernel earlier than 4.14  which can run on a Raspberry Pi 3 and run BlueZ for bluetooth management. Therfore we will test our exploitation using ARMv7 which is an Arch Linux Os build for Raspberry Pi 3.
  
  ### c. BlueBorne attack on Android
  
- Information Leak Vulnerability (CVE-2017-0785)
The first vulnerability in the Android operating system reveals valuable information which helps the attacker leverage one of the remote code execution vulnerabilities described below. The vulnerability was found in the SDP (Service Discovery Protocol) server, which enables the device to identify other Bluetooth services around it. The flaw allows the attacker to send a set of crafted requests to the server, causing it to disclose memory bits in response. These pieces of information can later be used by the attacker to overcome advanced security measures and take control over the device. This vulnerability can also allow an attacker to leak encryption keys from the targeted device and eavesdrop on Bluetooth communications, in an attack that very much resembles heartbleed.

- Remote Code Execution Vulnerability #1 (CVE-2017-0781)
This vulnerability resides in the Bluetooth Network Encapsulation Protocol (BNEP) service, which enables internet sharing over a Bluetooth connection (tethering). Due to a flaw in the BNEP service, a hacker can trigger a surgical memory corruption, which is easy to exploit and enables him to run code on the device, effectively granting him complete control. Due to lack of proper authorization validations, triggering this vulnerability does not require any user interaction, authentication or pairing, so the targeted user is completely unaware of an ongoing attack.

- Remote Code Execution vulnerability #2 (CVE-2017-0782)
This vulnerability is similar to the previous one, but resides in a higher level of the BNEP service – the Personal Area Networking (PAN) profile – which is responsible for establishing an IP based network connection between two devices. In this case, the memory corruption is larger, but can still be leveraged by an attacker to gain full control over the infected device. Similar to the previous vulnerability, this vulnerability can also be triggered without any user interaction, authentication or pairing.

- The Bluetooth Pineapple – Man in The Middle attack (CVE-2017-0783)
Man-in-The-Middle (MiTM) attacks allow the attacker to intercept and intervene in all data going to or from the targeted device. To create a MiTM attack using Wi-Fi, the attacker requires both special equipment, and a connection request from the targeted device to an open WiFi network. In Bluetooth, the attacker can actively engage his target, using any device with Bluetooth capabilities. The vulnerability resides in the PAN profile of the Bluetooth stack, and enables the attacker to create a malicious network interface on the victim’s device, re-configure IP routing and force the device to transmit all communication through the malicious network interface. This attack does not require any user interaction, authentication or pairing, making it practically invisible.
  
All Android phones, tablets, and wearables (except those using only Bluetooth Low Energy) of all versions are affected by four vulnerabilities found in the Android operating system, two of which allow remote code execution (CVE-2017-0781 and CVE-2017-0782), one results in information leak (CVE-2017-0785) and the last allows an attacker to perform a Man-in-The-Middle attack (CVE-2017-0783)
  
Sources:
  - [Original Armis code](https://github.com/ArmisSecurity/blueborne/tree/master/android)
  - [White paper](https://go.armis.com/hubfs/BlueBorne%20-%20Android%20Exploit.pdf)
  - [Blueborne - Android Take Over Demo](https://www.youtube.com/watch?v=Az-l90RCns8)
  - [BlueBorne explained at Hacktivity 2017](https://www.youtube.com/watch?v=NBAqzGtz9ts&t=3s)
  - [BlueBorne on Android: Exploiting an RCE Over the Air](https://www.armis.com/blueborne-on-android-exploiting-rce-over-the-air/)
  - [CVE-2017-0785 PoC](https://github.com/ojasookert/CVE-2017-0785)
  - [PoC for CVE-2017-0785](https://github.com/Sydpy/sdp-leak-it)
  - [Another CVE-2017-0785 PoC](https://github.com/Unknown025/CVE-2017-0785)
  - [Implementation of the CVE-2017-0781 Android heap overflow vulnerability](https://github.com/OtherChen32/CVE-2017-0781)
  - [CVE-2017-0781 PoC](https://github.com/ojasookert/CVE-2017-0781)
  - [littl tools](https://github.com/marsyy/littl_tools)
  
Our contribution:

We are going to reproduce this attacks using not patched Samsung Galaxy S3 and/or Sony Xperia 2.
  
  ### d. BlueBorne attack on Windows
  
- The Bluetooth Pineapple #2 – Man in The Middle attack (CVE-2017-8628)
This vulnerability is identical to the one found in the Android operating system, and affects both systems since they shared the same principals in implementing some of the Bluetooth protocol. The vulnerability resides in the Bluetooth stack, and enables the attacker to create a malicious  network interface on the victim’s device, re-configure IP routing and force the device to transmit all communication through it. This attack does not require any user interaction, authentication or pairing, making it also practically invisible.

All Windows computers since Windows Vista are affected by the “Bluetooth Pineapple” vulnerability which allows an attacker to perform a Man-in-The-Middle attack. Microsoft issued has security patches to all supported Windows versions on July 11, 2017, so we are going to find an older vulnerable image to reproduce the attack
  
Sources:
  - [Armis BlueBorne](https://www.armis.com/blueborne/)
  - [BlueBorne - Windows MiTM Demo](https://www.youtube.com/watch?v=QrHbZPO9Rnc)
  
Our contributions:

If we have enough time, we will try to reproduce Bluetooth Pineapple vulnerability using 'Windows 10 IoT Core Dashboard' on a Raspberry Pi 3, or non patch Windows on an old PC.
  
  ## 3. Protections and Mitigations
  Armis Guide: [PROTECTING THE ENTERPRISE FROM BLUEBORNE](http://go.armis.com/hubfs/BlueBorne%20Technical%20White%20Paper.pdf)
    
    
