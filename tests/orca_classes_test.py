import unittest
from dataclasses import asdict
from audithub_client.api.start_orca_task import OrCaParameters, ORCA_DEFAULT_TIMEOUT
from audithub_client.library.utils import asdict_exclude_none
from audithub_client.library.orca_utils import restructure_fuzzing_blacklist


class TestOrCaInvocation(unittest.TestCase):

    def test_timeout(self):
        op = OrCaParameters()
        assert op.timeout == ORCA_DEFAULT_TIMEOUT

        op = OrCaParameters(timeout=None)
        assert op.timeout == ORCA_DEFAULT_TIMEOUT

        op = OrCaParameters(timeout=1)
        assert op.timeout == 1

    def test_extracted_dictionary(self):
        op = OrCaParameters()
        dict_full = asdict(op)
        assert len(dict_full.keys()) > 2
        dict_stripped = asdict_exclude_none(op)
        assert len(dict_stripped.keys()) == 2
        assert "timeout" in dict_stripped.keys()
        assert "language" in dict_stripped.keys()

    def test_fuzzing_blacklist_decoding(self):
        assert restructure_fuzzing_blacklist(None) is None
        assert restructure_fuzzing_blacklist([]) is None
        l = restructure_fuzzing_blacklist(["contract.function"])
        assert len(l) == 1
        assert l[0].contract == "contract"
        assert l[0].function == "function"
        with self.assertRaises(RuntimeError):
            restructure_fuzzing_blacklist([""])
        with self.assertRaises(RuntimeError):
            restructure_fuzzing_blacklist(["."])
        with self.assertRaises(RuntimeError):
            restructure_fuzzing_blacklist(["a."])
        with self.assertRaises(RuntimeError):
            restructure_fuzzing_blacklist([".a"])


if __name__ == "__main__":
    unittest.main()
