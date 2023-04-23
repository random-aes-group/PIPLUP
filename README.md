# PIPLUP Pixel-location Image Password for LSB-Steganography UI Program

## Dependencies

```sh
pip install Pillow pyaes numpy pycryptodome pbkdf2 fire opencv-python
```
# CLI

## Example Encryption

```sh
NAME
    cli.py encrypt - Encrypt a secret message into an input image using AES and LSB-Steganography.

SYNOPSIS
    cli.py encrypt INPUT_IMAGE_PATH OUTPUT_IMAGE_PATH MESSAGE MESSAGE_PASSWORD

DESCRIPTION
    Encrypt a secret message into an input image using AES and LSB-Steganography.

POSITIONAL ARGUMENTS
    INPUT_IMAGE_PATH
        Type: str
        Input image's file path.
    OUTPUT_IMAGE_PATH
        Type: str
        Output stego-image's file path.
    MESSAGE
        Type: str
        Secret message to conceal.
    MESSAGE_PASSWORD
        Type: str
        Password to encrypt the secret message with.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

```sh
# for example:
(base) PIPLUP % python cli.py encrypt demo/in.png demo/out.png 'Some longer secret message' 'Somepass123WithSymbols!'

["vMAUkraiYAydNmoL5otFk9hvVOdA0zo6q9C9Hd4sZqIavqaVh4tEV54H8rnMvyAH", 52]
```


## Example Decryption

```sh
NAME
    cli.py decrypt - Decrypt a secret message from an input stego-image using AES and LSB-Steganography.

SYNOPSIS
    cli.py decrypt OUTPUT_IMAGE_PATH MESSAGE_PASSWORD PIXEL_LOCATION_PASSWORD LEN_ENCODED_MESSAGE

DESCRIPTION
    Decrypt a secret message from an input stego-image using AES and LSB-Steganography.

POSITIONAL ARGUMENTS
    OUTPUT_IMAGE_PATH
        Type: str
        Input stego-image's file path.
    MESSAGE_PASSWORD
        Type: str
        Password used to encrypt the secret message.
    PIXEL_LOCATION_PASSWORD
        Type: str
        Password for pixel locations.
    LEN_ENCODED_MESSAGE
        Type: int
        Length of the encoded message.

NOTES
    You can also use flags syntax for POSITIONAL ARGUMENTS
```

```sh
(base) PIPLUP % python cli.py decrypt demo/out.png 'Somepass123WithSymbols!' 'vMAUkraiYAydNmoL5otFk9hvVOdA0zo6q9C9Hd4sZqIavqaVh4tEV54H8rnMvyAH' 52 
Some longer secret message
```
