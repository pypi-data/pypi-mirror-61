=======
History
=======

0.3.5 (2020-02-18)
------------------

* Fix issue with reading integers from LabJack LJM Library (device's product ID, serial
  number etc.)
* Fix development requirements specification (tox version).

0.3.4 (2019-12-20)
------------------

* New devices using serial connection:
    * Heinzinger Digital Interface I/II and a Heinzinger PNC power supply
    * Q-switched Pulsed Laser and a laser attenuator from CryLas
    * Newport SMC100PP single axis motion controller for 2-phase stepper motors
    * Pfeiffer TPG controller (TPG 25x, TPG 26x and TPG 36x) for Compact pressure Gauges
* PEP 561 compatibility and related corrections for static type checking (now in CI)
* Refactorings:
    * Protected non-thread safe read and write in communication protocols
    * Device sequence mixin: start/stop, add/rm and lookup
    * `.format()` to f-strings
    * more enumerations and a quite some improvements of existing code
* Improved error docstrings (:code:`:raises:` annotations) and extended tests for
  errors.

0.3.3 (2019-05-08)
------------------

* Use PyPI labjack-ljm (no external dependencies)


0.3.2 (2019-05-08)
------------------

* INSTALLATION.rst with LJMPython prerequisite info


0.3.1 (2019-05-02)
------------------

* readthedocs.org support

0.3 (2019-05-02)
----------------

* Prevent an automatic close of VISA connection when not used.
* Rhode & Schwarz RTO 1024 oscilloscope using VISA interface over TCP::INSTR.
* Extended tests incl. messages sent to devices.
* Added Supercube device using an OPC UA client
* Added Supercube 2015 device using an OPC UA client (for interfacing with old system
  version)

0.2.1 (2019-04-01)
------------------

* Fix issue with LJMPython not being installed automatically with setuptools.

0.2.0 (2019-03-31)
------------------

* LabJack LJM Library communication wrapper and LabJack device.
* Modbus TCP communication protocol.
* Schneider Electric ILS2T stepper motor drive device.
* Elektro-Automatik PSI9000 current source device and VISA communication wrapper.
* Separate configuration classes for communication protocols and devices.
* Simple experiment manager class.

0.1.0 (2019-02-06)
------------------

* Communication protocol base and serial communication implementation.
* Device base and MBW973 implementation.
