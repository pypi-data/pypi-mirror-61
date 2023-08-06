<h1 align="center">Welcome to LinkFusions 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://app.linkfusions.com/lf-docs/" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
  <a href="#" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

> Python Library to Interface LinkFusions API

### 🏠 [Homepage](https://github.com/CloudPR/EM-LF-Repo)

### ✨ [Demo](https://app.linkfusions.com/lf-docs/)

## Install

```sh
pip install LinkFusions
```

## Usage

Sample

```python
import LinkFusions as lf


CLIENT_ID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
CLIENT_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# Replace these client id and client secret with yours

token = lf.LinkFusions.auth(
    email='xxxx@email.com', password='madasspassword',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
token = lf.LinkFusions(token.get('access_token'))
fusion = lf.LinkFusions(token)
...
...
# You can make requests with the fusion object after here
```

## Author

👤 **Cloud Custom Solutions**

* Website: https://cloudcustomsolutions.com

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_