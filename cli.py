import os
import fire
import random
import string
import numpy as np
import binascii
import pbkdf2
import pyaes
from PIL import Image
from hashlib import sha512
from typing import Tuple, List


class AES:
    """This class contains static functions for AES encryption and decryption."""
    salt: bytes = b'\\`\xd6\xdaB\x03\xdd\xd4z\xb6p\xe8O\xf0\xa8\xc0'
    iv: int = 113573230825063269301116483319046608643543151989648198772824118452040014644050

    @staticmethod
    def encrypt(message: str, password: str) -> str:
        """Encrypt input message with AES using an input password.

        Args:
            message (str): Input message to encode with AES.
            password (str): Password for AES encryption.

        Returns:
            str: Encrypted message using AES and password.
        """
        # salt password
        key = pbkdf2.PBKDF2(password, AES.salt).read(32)
        # initialize aes encryptor with key
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(AES.iv))
        # encrypt message using aes
        encrypted_bytes = aes.encrypt(message)
        # decode encrypted bytes into utf-8 characters
        return binascii.hexlify(encrypted_bytes).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_message: str, password: str) -> str:
        """Decrypt an encrypted message with AES using an input password.

        Args:
            encrypted_message (str): Input encrypted message to decode with AES.
            password (str): Password for AES decryption.

        Returns:
            str: decrypted original message using AES and password.
        """
        # decode encrypted message back into bytes
        encrypted_bytes = binascii.unhexlify(bytes(encrypted_message, 'utf-8'))
        # salt the password and initialize AES object
        key = pbkdf2.PBKDF2(password, AES.salt).read(32)
        aes = pyaes.AESModeOfOperationCTR(key, pyaes.Counter(AES.iv))
        # decrypt encrypted bytes
        decrypted_bytes = aes.decrypt(encrypted_bytes)
        # decode decrypted bytes back to string
        return decrypted_bytes.decode('utf-8')


class LSB:
    """This class contains static functions for LSB-Steganography encoding and decoding."""

    @staticmethod
    def _generate_pixel_locations(
            width: int, height: int,
            len_encoded_message: int,
            pixel_location_password: str
    ) -> List[int]:
        """This function generates a list of pixel locations given the pixel location password,
        dimensions of the image, and the length of the encoded message.

        Args:
            width (int): Width of the image.
            height (int): Height of the image.
            len_encoded_message (int): Length of the encoded message.
            pixel_location_password (str): Password for pixel locations.

        Returns:
            List[int]: The list of pixel locations.
        """
        # seed prng with pixel location password
        seed = pixel_location_password.encode()
        seed = int.from_bytes(seed + sha512(seed).digest(), 'little') % (2 ** 32 - 1)
        np.random.seed(seed)
        # randomly select locations for LSB-steganography
        locations = np.arange(width * height)
        np.random.shuffle(locations)
        # take the first len_encoded_message*3 locations (3 pixels used for each byte)
        # 8 bit -> LSB of rgb/rgb/rg, b in the last pixel will simply be copied
        pixel_locations = locations[:len_encoded_message * 3]
        return pixel_locations

    @staticmethod
    def _char_to_bits(data: str) -> List[str]:
        """Convert input string into list of 8 bit binary strings. 

        Args:
            data (str): Input stirng.

        Returns:
            List[str]: list of binary strings.
        """
        data_bits = list(format(c, '08b') for c in bytearray(data.encode('latin-1')))
        return data_bits

    @staticmethod
    def encode(
            input_image_path: str,
            encoded_message: str,
            pixel_location_password: str
    ) -> Image:
        """Encode a message into a input image using LSB-Steganography to pixel locations 
        specified by the pixel locaiton password.

        Args:
            input_image_path (str): Input image's file path.
            encoded_message (str): Message to encode into image.
            pixel_location_password (str): Password to determine pixel location to encode message.

        Returns:
            Image: PIL Image object with message concealed within. 
        """
        # Load input image with PIL and extract it's dimensions
        img = Image.open(input_image_path)
        [width, height] = img.size

        # Obtain pixel loactions with the pixel location password.
        pixel_locations = LSB._generate_pixel_locations(width, height, len(encoded_message), pixel_location_password)

        # convert message string to list of binary strings.
        encoded_message_bits = LSB._char_to_bits(encoded_message)
        char_idx = 0
        # 3 pixels in sequence defined in the pixel locations are used to encode every 8 bit character.
        # LSB's of R0 G0 B0 R1 G1 B1 R2 G2 corresponds to the 8 bits in the character.
        for i in range(0, len(encoded_message) * 3, 3):  # i advance in steps of 3
            bit_idx = 0
            # take three consecutive pixels in pixel locations pl[i],pl[i+1],pl[i+2]
            for j in range(0, 3):
                # these are the pixel locations in question
                pixel_loc = (pixel_locations[i + j] // height, pixel_locations[i + j] % height)

                # get the original rgb before steganography
                original_rgb = img.getpixel(pixel_loc)

                new_rgb = []

                # for each channel's raw value, 
                for k in original_rgb:
                    # if LSB is different then edit the lsb by shifing the intensity by 1.
                    # k&1 extracts lsb of k
                    if ((k & 1) != int(encoded_message_bits[char_idx][bit_idx])):
                        # to prevent underflow, if k is already a 0 then add 1
                        if (k == 0):
                            k += 1
                        # otherwise simply minus 1 (this prevents an overflow too)
                        else:
                            k -= 1

                    # add this new color into the new rgb tuple
                    new_rgb.append(k)

                    bit_idx += 1  # forward to the next bit in character
                    if bit_idx >= 8:  # if all 8 bits has been encoded then break out
                        break

                # if all 8 bits has been encoded (3rd pixel), simply copy the last green pixel
                if bit_idx >= 8:
                    new_rgb.append(original_rgb[2])
                # convert the list into a tuple and write to the pixel location
                new_rgb = (new_rgb[0], new_rgb[1], new_rgb[2])
                img.putpixel(pixel_loc, new_rgb)

            char_idx += 1  # move to next character
        # returns the stegnographed image
        return img

    @staticmethod
    def decode(
            output_image_path: str,
            pixel_location_password: str,
            len_encoded_message: int
    ) -> str:
        """Decode a message of given length from an input stego-image using LSB-Steganography to pixel locations 
        specified by the pixel locaiton password.

        Args:
            output_image_path (str): Input stego-image's file path.
            pixel_location_password (str): Password to determine pixel location to encode message.
            len_encoded_message (int): Length of the encoded message.

        Returns:
            str: Encoded message extracted from the stego-image.
        """
        # load the stego-image, and extract its dimensions.
        output_image = Image.open(output_image_path)
        [width, height] = output_image.size
        # obtain pixel loactions with the pixel location password.
        pixel_locations = LSB._generate_pixel_locations(width, height, len_encoded_message, pixel_location_password)
        pixel_locations = pixel_locations.astype(int)

        # initialize list to cache bits read.
        encrypted_bytes = []

        for i in range(0, len(pixel_locations), 3):
            # for each 3 pixel, recover 1 byte of information
            encrypted_byte = ""
            for j in range(0, 3):
                pixel_loc = (pixel_locations[i + j] // height, pixel_locations[i + j] % height)
                rgb = output_image.getpixel(pixel_loc)
                # extract the lsb for each channel in pixel and append to character
                for k in rgb:
                    if k & 1:
                        encrypted_byte += '1'
                    else:
                        encrypted_byte += '0'
            # drop the extra 9th bit and append to list of encrypted bits
            encrypted_byte = encrypted_byte[:-1]
            encrypted_bytes.append((encrypted_byte))

        # recover the encrypted message characters from the bytes.
        encrypted_message = ''
        for i in encrypted_bytes:
            encrypted_message += chr(int(i, 2))
        return encrypted_message


class CLI:
    @staticmethod
    def encrypt(
            input_image_path: str,
            output_image_path: str,
            message: str,
            message_password: str
    ) -> Tuple[str, int]:
        """Encrypt a secret message into an input image using AES and LSB-Steganography.

        Args:
            input_image_path (str): Input image's file path.
            output_image_path (str): Output stego-image's file path.
            message (str): Secret message to conceal.
            message_password (str): Password to encrypt the secret message with.

        Returns:
            Tuple[str, int]: (pixel_location_password, len_encoded_message)
                pixel_location_password (str): Password for pixel locations.
                len_encoded_message (int): Length of the encoded message.
        """

        def _generate_pixel_location_password() -> str:
            """Generates a random password string to determine pixel location to encode message.

            Returns:
                (str): Password to determine pixel location to encode message.
            """
            return ''.join(random.choices(string.digits + string.ascii_letters, k=64))

        # assert the existence of input image
        if os.path.exists(input_image_path):
            # Deletes output stego-image if already exists
            if os.path.exists(output_image_path):
                os.remove(output_image_path)
            # encrypt secret message with AES
            encoded_message = AES.encrypt(message, message_password)
            # obtain pixel location password
            pixel_location_password = _generate_pixel_location_password()
            # encode message into input image's lsb in pixel location specified by the password
            output_img = LSB.encode(input_image_path, encoded_message, pixel_location_password)
            # serialize image to disk
            output_img.save(output_image_path)
            # outputs the generated pixel_location_password and length of encoded message
            return pixel_location_password, len(encoded_message)
        else:
            # Display error when assertion failed
            print("Input image is not Present")
            return 'Input image is not Present', None

    @staticmethod
    def decrypt(
            output_image_path: str,
            message_password: str,
            pixel_location_password: str,
            len_encoded_message: int
    ) -> str:
        """Decrypt a secret message from an input stego-image using AES and LSB-Steganography.

        Args:
            output_image_path (str): Input stego-image's file path.
            message_password (str): Password used to encrypt the secret message.
            pixel_location_password (str): Password for pixel locations.
            len_encoded_message (int): Length of the encoded message.

        Returns:
            str: The concealed secret message extracted from the stego-image.
        """
        # assert the existance of output stego-image
        if os.path.exists(output_image_path):
            # extract decoded message from the stego-imnage
            decoded_text = LSB.decode(output_image_path, pixel_location_password, len_encoded_message)
            # decrypt secret message with AES
            decrypted_message = AES.decrypt(decoded_text, message_password)
            # returns the decrypted secret message
            return decrypted_message
        else:
            # Display error when assertion failed
            print("Input image is not Present")
            return "Input image is not Present"


fire.Fire(CLI)
