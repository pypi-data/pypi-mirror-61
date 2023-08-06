cdef extern from "iarduino_I2C_Dummy.cpp":
    pass

cdef extern from "iarduino_I2C_Dummy.h":
    cdef cppclass iarduino_I2C_Dummy:
        iarduino_I2C_Dummy() except +
        iarduino_I2C_Dummy(unsigned char) except +
        bint begin()
        bint changeAddress(unsigned char)
        bint reset()
        unsigned char getAddress()
        unsigned char getVersion()
