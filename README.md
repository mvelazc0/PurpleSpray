# PurpleSpray

PurpleSpray is an adversary simulation tool that executes password spray behavior under different scenarios and conditions with the purpose of generating attack telemetry in properly monitored Windows enterprise environments. Blue teams can leverage PurpleSpray to identify gaps in visibility as well as test the resilience, improve existing and build new detection analytics for password spraying attacks.

PurpleSpray currently supports two [modules](https://github.com/mvelazc0/PurpleSpray/wiki/Modules) that leverage the SMB protocol for the spray scenarios. For more details and [demos](https://github.com/mvelazc0/PurpleSpray/wiki/Demos), visit the [Wiki](https://github.com/mvelazc0/PurpleSpray/wiki/Home).

PurpleSpray was first presented at [BSides Baltimore 2019](https://www.youtube.com/watch?v=8JFP1wj37Vk). 

## Quick Start Guide

PurpleSpray has been tested on Kali Linux 2018.4 and Windows 10 1830 under Python 3.6 and Python 2.7.

### Installation

```
$ git clone https://github.com/mvelazc0/PurpleSpray.git
$ pip install -r PurpleSpray/requirements.txt
```
 ### Usage
 
 ```
 $ python PurpleSpray.py
 ```

 ### Docker Build

 ```
 $ docker build -t purplespray .
 ```

### Docker Usage

 ```
 $ docker run --rm -it purplespray
 ```

## Acknoledgments

This project could not be possible without the following projects:

* [Impacket](https://github.com/SecureAuthCorp/impacket)
* [Powershell Empire](https://github.com/EmpireProject/Empire)
* [Death Star](https://github.com/byt3bl33d3r/DeathStar)
* [The PenTesters Framework](https://github.com/trustedsec/ptf)

## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details
