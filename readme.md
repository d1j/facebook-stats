# "Cha Cha" counting script

This script calculates the basic stats of a Facebook chat.

It gathers the following information:
* The number of messages each participant has sent;
* The number of Cha Cha reactions given/received by each participant;

The script also calculates how many times each participant reacted to particular participant's messages in the group chat.

Calculated data is written to a *.csv file.

## Usage

1. Download Facebook Messenger data in JSON format:  
https://www.facebook.com/dyi/?referrer=yfi_settings
2. Run the script specifying a relative path to the target chat folder:  
`python3 cha_counter.py <relative path to the folder>`  
Example:  
`python3 cha_counter.py data/facebook-facebookuser1/messages/inbox/groupname_xyz`
