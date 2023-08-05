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
```bash
choco install python --version=3.7.1
choco install -y MSYS2
refreshenv.cmd
pip install pypaperwallet WeasyPrint mnemoic qrcode[pil] pycoin
```

From MSYS2 shell run:
```bash
pacman -S mingw-w64-x86_64-gtk3
```

From Python 3.7 run:
```python
from pypaperwallet.pdf_wallet import mk_wallet, write_pdf
from pypaperwallet.template import disclosure

mk_wallet('wallet.pdf')

# For political contributions, generate disclosure form
write_pdf(political_disclosure(), 'disclosure.pdf')
```

PGP Key: [Reddit](https://www.reddit.com/user/brianddk/comments/aojt4u/brianddk_gpg_public_key/), [Website](https://brianddk.github.io/darkweb/brianddk/pub.asc), [SKS Keyserver](https://sks-keyservers.net/pks/lookup?op=get&search=0x6285FA08FB67B72BE4DA4184835F0433A6D51860)

```
6285 FA08 FB67 B72B E4DA  4184 835F 0433 A6D5 1860
```

Verifying package and execute

1. Find latest release at https://github.com/brianddk/pypaperwallet/releases
2. Expand "Assets" and download the "Source code (tar.gz)" as `pypaperwallet.tar.gz`.
3. Download the `*.tar.gz.sig` file naming it `pypaperwallet.tar.gz.sig`
4. Use the GPG command `gpg --verify *.tar.gz.sig` to verify the download
5. Extract the contents of the `.zip` or `.tar.gz` file to any directory
6. Modify `test.py` to your liking and run from python 3.7 to produce the PDFs.
7. To change wording, modify the contents of `template.py`
