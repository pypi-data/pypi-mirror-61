
from distutils.core import setup
import snip_basic_verify

setup(
    py_modules=['snip_basic_verify'],
    ext_modules=[snip_basic_verify.ffi.verifier.get_extension()])
