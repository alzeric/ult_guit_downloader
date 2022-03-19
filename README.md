# ult_guit_downloader

## What does this do? ##
Downloads the tab file from Ultimate Guitar into a usable format for use in other software's like TuxPro, Guitar Pro, Editor on Fire (EoF) ..etc 

## PreReqs ##
| ITEM          | Notes                                                             |
| ------------- | ----------------------------------------------------------------- |
| Python 3.9.10 | could work with other versions, just not tested/supported |
| requests pkg | ```````pip install requests``````` |
| UG Account | Tested with Premium/Paid account, could work with free, not tested |
| cookies.txt | Be sure to follow the instructions on *How to get cookies?* |

## Usage ## 
  *Python ult_guit_download.py https://tabs.ultimate-guitar.com/tab/EXAMPLE/EXAMPLE-SONG-TITLE-12345678*
  
## How to get cookies? ##
  Login to Ultimate-Guitar website, open inspector window "***Ctrl+Shift+I***" (chrome)
  
  (yes, fully login, not just visiting the site as guest)
  
  In the console window type ***document.cookie*** and press Enter
  
  Copy the text that appears and paste it in a ***cookies.txt*** file in the same folder as this script

## Security ##
  **cookies.txt** - Be sure to keep this file safe do not share with anyone!
