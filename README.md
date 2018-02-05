# THC_BlueBorne
Projet long TLS-SEC pour la réalisation d'un challenge "tuto" lors de la Toulouse Hacking Convention. Exploitation de la faille Blueborne.

In this project, we are going to reproduce a POC of the bluetooth vulnerability. The main purpuse is to achieve to spread a worm using bluetooth communications using Linux and Android systems (and Windows system if we have enough time).
This project is mainly based on the Armis BlueBorne researches https://www.armis.com/blueborne/ and several open source github repositories.

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
  https://github.com/hook-s3c/blueborne-scanner
    
## 2. Exploits

  ### a. BlueBorne L2CAP Testing Framework
  https://github.com/ArmisSecurity/blueborne/tree/master/l2cap_infra
  
  ### b. BlueBorne Linux-Bluez RCE Exploits
  All Linux devices running BlueZ are affected by the information leak vulnerability (CVE-2017-1000250).
  The following directory contains a PoC code for the Linux-RCE vulnerability (CVE-2017-1000251). The exploits are specifically tailored for specific fw images of two devices: The Amazon Echo and Samsung Gear S3.
  https://github.com/ArmisSecurity/blueborne/tree/master/linux-bluez
  We are going to reproduce it using a vulnerable Linux image on a Raspberry Pi.
  
  ### c. BlueBorne Android Exploit PoC
  All Android phones, tablets, and wearables (except those using only Bluetooth Low Energy) of all versions are affected by four vulnerabilities found in the Android operating system, two of which allow remote code execution (CVE-2017-0781 and CVE-2017-0782), one results in information leak (CVE-2017-0785) and the last allows an attacker to perform a Man-in-The-Middle attack (CVE-2017-0783)
  https://github.com/ArmisSecurity/blueborne/tree/master/android
  
  ### d. Exploit on Windows
  All Windows computers since Windows Vista are affected by the “Bluetooth Pineapple” vulnerability which allows an attacker to perform a Man-in-The-Middle attack (CVE-2017-8628).
  Microsoft issued has security patches to all supported Windows versions on July 11, 2017, so we are going to find an older vulnerable image to reproduce the attack.
    
    
