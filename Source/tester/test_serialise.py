# Standard library imports
import urllib.request
import unittest

# Local application imports
from assets import serialisers
from assets.serialisers.csg.util import CSG_HEADER, create_hash, recalculate_hash, xor_encrypt


class TestSerialiser(unittest.TestCase):
    '''
    Tests for different `serialiser` modules.
    '''

    def test_csgmdl2_hash(self) -> None:
        '''
        Tests that CSG v2 unions have a correct hashing algorithm.
        '''
        url = 'https://github.com/krakow10/rbx_mesh/raw/refs/heads/master/meshes/5692112940_2.meshdata'
        with urllib.request.urlopen(url) as response:
            data = response.read()

        data_xor = xor_encrypt(data)
        self.assertEqual(
            first=create_hash(
                data_xor[0x32:0x32+0x3a*0x54],
                data_xor[0x0000133E:0x0000133E + 4*0x6c],
                data_xor[0x1a:0x2a]
            ),
            second=data_xor[0xa:0x2a],
        )
        self.assertEqual(
            first=recalculate_hash(data),
            second=data,
        )

    def test_csgmdl5_load(self) -> None:
        '''
        Tests that CSG v3 unions can be parsed.
        '''
        url = 'https://github.com/krakow10/rbx_mesh/raw/refs/heads/master/meshes/13626979828.meshdata5'
        with urllib.request.urlopen(url) as response:
            data = response.read()

        (result, _changed) = serialisers.parse(
            data, methods={serialisers.method.csg},
        )

        self.assertTrue(result.startswith(CSG_HEADER.MDL2.value))

    def test_csgphs8_load(self) -> None:
        '''
        Tests that CSG v3 unions can be parsed.
        '''
        url = 'https://github.com/krakow10/rbx_mesh/raw/refs/heads/master/meshes/13626979828.meshdata5'
        with urllib.request.urlopen(url) as response:
            data = response.read()

        (result, _changed) = serialisers.parse(
            data, methods={serialisers.method.csg},
        )

        self.assertTrue(result.startswith(CSG_HEADER.MDL2.value))
