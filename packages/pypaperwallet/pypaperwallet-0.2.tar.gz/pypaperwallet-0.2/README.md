<!--
# [rights]  Copyright 2020 brianddk at github https://github.com/brianddk
# [license] Apache 2.0 License https://www.apache.org/licenses/LICENSE-2.0
# [repo]    https://github.com/brianddk/pypaperwallet
# [btc]     BTC-b32: bc1qwc2203uym96u0nmq04pcgqfs9ldqz9l3mz8fpj
# [tipjar]  https://gist.github.com/brianddk/3ec16fbf1d008ea290b0
-->

# pypaperwallet
Python Paper Wallet based on github/pointbiz/bitaddress.org

To install `choco` see the [Chocolatey install page](https://chocolatey.org/install)

From Windows shell run:
```shell
choco install python --version=3.7.1
choco install -y MSYS2
refreshenv.cmd
pip install pypaperwallet WeasyPrint mnemoic qrcode[pil] pycoin
```

From MSYS2 shell run:
```shell
pacman -S mingw-w64-x86_64-gtk3
```

From Python 3.7 run:
```python
from pypaperwallet.pdf_wallet import mk_wallet

mk_wallet('wallet.pdf')
```
