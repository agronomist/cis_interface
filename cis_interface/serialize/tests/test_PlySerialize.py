import copy
import numpy as np
from cis_interface.serialize.tests.test_DefaultSerialize import \
    TestDefaultSerialize


class TestPlySerialize(TestDefaultSerialize):
    r"""Test class for TestPlySerialize class."""

    def __init__(self, *args, **kwargs):
        super(TestPlySerialize, self).__init__(*args, **kwargs)
        self._cls = 'PlySerialize'
        self._objects = [self.ply_dict]

    def test_apply_scalar_map(self):
        r"""Test applying a scalar colormap."""
        for _o in self._objects:
            o = self.map_sent2recv(_o)
            scalar_arr = np.arange(len(o['faces']))
            self.instance.apply_scalar_map(o, scalar_arr,
                                           scale_by_area=True)

    def map_sent2recv(self, obj):
        r"""Convert a sent object into a received one."""
        out = copy.deepcopy(obj)
        if 'vertex_colors' not in out:
            out['vertex_colors'] = []
            for v in out['vertices']:
                out['vertex_colors'].append(self.instance.default_rgb)
        return out