Longleding Operation OCR Engine SDK

# Supported Python Versions

Python >= 3.6

# Installation

longleding-ocr-engine-sdk is available for Linux, macOS, and Windows.

```shell script
$ pip install longleding-ocr-engine-sdk
```

# Basic Usage

```python
# -*- coding: utf-8 -*-
import ocr_engine

ocr_engine_endpoint = "localhost:80"
ocr_engine_src = "demo"
ocr_engine.init_service(endpoint=ocr_engine_endpoint, src=ocr_engine_src)

if __name__ == '__main__':
    print(ocr_engine.ocr_with_image_oss_path('upload/some_image.jpg'))
    print(ocr_engine.ocr_with_image_url('https://some.domain.com/some_image.jpg'))
    with open('some_image.jpg', 'rb') as f:
        img = f.read()
        print(ocr_engine.ocr_with_image(img))

```
