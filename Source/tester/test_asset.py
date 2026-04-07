# Standard library imports
from typing import override
import unittest

# Local application imports
import assets.serialisers as serialisers
import assets.extractor as extractor


class TestAssets(unittest.TestCase):
    '''
    Tests for the asset extraction module.
    '''

    @override
    @classmethod
    def setUpClass(cls):
        if extractor.get_rōblox_cookie() is None:
            raise unittest.SkipTest(
                'No cookie provided; skipping asset tests.',
            )

    def get_rōblox_asset(self, iden: int) -> bytes:
        data = extractor.download_rōblox_asset(iden)
        self.assertIsNotNone(data, 'Unable to load asset')
        assert data is not None
        return data

    def test_place_load(self) -> None:
        '''
        Tests that the data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it can be
        parsed by the RBXL parser.
        '''
        data = self.get_rōblox_asset(1818)
        self.assertTrue(serialisers.rbxl.check(data))

    def test_audio_load(self) -> None:
        '''
        Tests that audio data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all,
        then checks if it is either an OGG or a WAVE audio file.
        '''
        data = self.get_rōblox_asset(12222084)
        self.assertRegex(data, b'(OggS|RIFF)')

    def test_video_load(self) -> None:
        '''
        Tests that video data can be loaded and parsed by the parser.
        '''
        data = self.get_rōblox_asset(5608333583)
        self.assertTrue(serialisers.video.check(data))
        webm_data = serialisers.video.parse(data)
        self.assertIsNotNone(webm_data)

    def test_image_load(self) -> None:
        '''
        Tests that specific image data can be loaded and is in the PNG format.
        '''
        data = self.get_rōblox_asset(270995247)
        # Asserts that the data starts with the PNG header, indicating it is a valid PNG image.
        self.assertTrue(data.startswith(b'\x89PNG'))

    def test_mesh_load(self) -> None:
        '''
        Tests that mesh data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it can be parsed by the `mesh` parser.
        '''
        data = self.get_rōblox_asset(120627289)
        result = serialisers.mesh.parse(data) or data
        self.assertTrue(
            serialisers.mesh.check(result),
            'Invalid mesh',
        )

    def test_mesh_load_100(self) -> None:
        '''
        Tests that mesh data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it has been processed by the `mesh` parser.
        '''
        data = self.get_rōblox_asset(54983181)
        self.assertEqual(
            serialisers.mesh.get_version(data), '1.00',
            'Original mesh was probably modified by Rōblox before it was loaded here.',
        )
        result = serialisers.mesh.parse(data) or data
        self.assertLess(
            serialisers.mesh.get_version(result), '4.01',
            'Mesh version processed by RFD is too high.',
        )

    def test_mesh_load_401(self) -> None:
        '''
        Tests that mesh data can be loaded and parsed by the parser.
        Asserts that the data has been loaded at all, then checks if it has been processed by the `mesh` parser.
        '''
        data = self.get_rōblox_asset(7018365851)
        result = serialisers.mesh.parse(data) or data
        self.assertLess(
            serialisers.mesh.get_version(result), '4.01',
            'Mesh version processed by RFD is too high.',
        )

    def test_rbxlx_load(self) -> None:
        '''
        Tests that XML files can be loaded and parsed by the parser.
        '''
        data = self.get_rōblox_asset(63043890)
        result = serialisers.rbxlx.parse(data) or data
        self.assertTrue(
            serialisers.rbxlx.check(result),
            'Invalid RBXLX stream',
        )

    @unittest.skip("AttributeError: type object 'method' has no attribute 'convert_csg'")
    def test_csg_load(self) -> None:
        '''
        Tests that CSG v3 unions can be parsed.
        '''
        data = self.get_rōblox_asset(4500696697)
        serialisers.rbxl.parse(
            data, methods={serialisers.rbxl.method.convert_csg},
        )
