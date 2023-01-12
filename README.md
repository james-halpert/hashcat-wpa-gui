# hashcat-wpa-gui
This is a python gui for hashcat. It is optimized for users of wifite which stores cap files in the folder ~/hs. This can be changed to your own settings in the source code which is noted.
Please update all file locations in the source before using or the code will default to your home directory and assume all installations and files are branched from your home directory (linux).
You must have hcxtools installed (specifically hcxpcapngtool)
You must have hashcat installed (and update the path as listed to your install dir)
Once all your paths are mapped the program allows for easy cap file selection and hccap destination saving. Additionally you may select hccap files that are already created and pair them with dictionary files for hashcat -m 22000 attacks (with -w 3 speed enhancement).
To execute brute force or masked attacks you will need to change the hardcoded commands prior to execution.
All commands prompt for sudo rights during execution.
The ideal execution of this application is for those of you with several dictionaries and a single hccap file you wish to run tests against. If you have already solved the raw text of a hash in hashcat the "show" button will display the previously captured data in the pot.
Feel free to make any changes to the commands as you see fit.
