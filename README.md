# Switch-Windows-EnterpriseEval-to-Enterprise
Guide and files to switch from Windows 11 Enterprise Evaluation to Windows 11 Enterprise for free.

Step 1: 

Go to: C:\Windows\System32\spp\tokens\skus

Step 2:

Download the folder named 'Enterprise' that's linked to this repository and once its downloaded, drag the WHOLE folder into C:\Windows\System32\spp\tokens\skus

Step 3:

Open up Command Prompt as an Administrator and paste the following (if it errors, try one by one)


cscript.exe %windir%\system32\slmgr.vbs /rilc

cscript.exe %windir%\system32\slmgr.vbs /upk >nul 2>&1

cscript.exe %windir%\system32\slmgr.vbs /ckms >nul 2>&1

cscript.exe %windir%\system32\slmgr.vbs /cpky >nul 2>&1

cscript.exe %windir%\system32\slmgr.vbs /ipk NPPR9-FWDCX-D2C8J-H872K-2YT43

sc config LicenseManager start= auto & net start LicenseManager

sc config wuauserv start= auto & net start wuauserv


Step 4:

Now you are on Windows 10/11 Enterprise however windows is NOT activated, now is the time to enter your windows license key or activate windows using Massgravel, to do this paste **irm https://get.activated.win** | iex into powershell and use option 1. 
