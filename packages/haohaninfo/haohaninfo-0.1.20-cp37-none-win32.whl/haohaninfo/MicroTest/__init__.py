import platform
bit = platform.architecture()[0]

if(bit == '32bit'):
    from haohaninfo.MicroTest.MicroTest import MicroTest
    from haohaninfo.MicroTest import microtest_db

else:
    from haohaninfo.MicroTest.MicroTest64 import MicroTest
    from haohaninfo.MicroTest import microtest_db64 as microtest_db
