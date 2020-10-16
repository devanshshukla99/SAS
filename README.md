# SAS
```
   _____               _____ 
  / ____|     /\      / ____|
 | (___      /  \    | (___  
  \___ \    / /\ \    \___ \ 
  ____) |  / ____ \   ____) |
 |_____/  /_/    \_\ |_____/                              

```

**Software Acquisation System for Software Defined Radios**

Includes all necessary codes for acquiring and processing of the collected data.

### Modes Available
  * **RFI Acquisation**: In this mode the program collects data from start frequency to stop frequency with 2 MHz bandwidth and 1 MHz overlap for the given integration and observation times.
  * **Normal Acquisation**

## Initial Setup --
```python
pip3 install -r requirements.txt
```
## Usage --
**Run sas_rfi.py for starting the Program**
```python
python sas_rfi.py [Args]
```
Args:
```
-ns : No Sync
-sch : Scheduled Time || now
-rfi : RFI Module
```

Thanks for checking this page out.

Let me know of any issues.

## Credits --

SAS acquires data using [rtl_power_ffw](https://github.com/AD-Vega/rtl-power-fftw), many thanks to its Creators and Contributors.
