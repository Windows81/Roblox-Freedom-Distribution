import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
import util.resource

def signUTF8(contentToSign: str, formatAutomatically: bool = True, addNewLine: bool = True, useNewKey: bool = False,
             twelveclient: bool = False) -> str | bytes:
    """
        Signs the content given ( Expected UTF8 ) and returns the signature
        but if formatAutomatically is set to True, it will return it in the
        proper format that the Roblox Client expects --rbxsig%signature% then the content

        addNewLine will add a new line to the start of the content before signing
        useNewKey will use RSA_PRIVATE_KEY_PATH2 instead of RSA_PRIVATE_KEY_PATH which is a 2048 bit key instead of 1024

        :param contentToSign: The content to sign
        :param formatAutomatically: Whether to format the signature automatically
        :param addNewLine: Whether to add a new line to the start of the content before signing
        :param useNewKey: Whether to use RSA_PRIVATE_KEY_PATH2 instead of RSA_PRIVATE_KEY_PATH

        :returns: str | bytes (Signature or Formatted Signature)

        https://github.com/InnitGroup/syntaxsource/blob/main/syntaxwebsite/app/util/signscript.py
    """
    RSA_PRIVATE_KEY_PATH = util.resource.retr_full_path(
            util.resource.dir_type.MISC,
            'PrivateKey2020.pem',
        )

    if addNewLine:
        contentToSign = "\n" + contentToSign
    contentToSign: bytes = contentToSign.encode("utf-8")
    with open(RSA_PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
            backend=default_backend()
        )

    signature = private_key.sign(
        contentToSign,
        padding.PKCS1v15(),
        hashes.SHA1()
    )

    if formatAutomatically:
        if twelveclient:
            return "%{}%{}".format(
                base64.b64encode(signature).decode("utf-8"),
                contentToSign.decode("utf-8")
            )
        if useNewKey:
            return "--rbxsig2%{}%{}".format(
                base64.b64encode(signature).decode("utf-8"),
                contentToSign.decode("utf-8")
            )
        return "--rbxsig%{}%{}".format(
            base64.b64encode(signature).decode("utf-8"),
            contentToSign.decode("utf-8")
        )
    else:
        return signature