cdef extern from "iarduino_I2C_Encoder.cpp":
    pass

cdef extern from "iarduino_I2C_Encoder.h":
    cdef cppclass iarduino_I2C_Encoder:
        iarduino_I2C_Encoder() except +
        iarduino_I2C_Encoder(unsigned char) except +
        bint begin()
        bint reset()
        bint changeAddress(unsigned char)
        unsigned char getAddress()
        unsigned char getVersion()
        bint getPullI2C()
        bint setPullI2C(bint)
        unsigned short getButton(unsigned char)
        short getEncoder(unsigned char)
        short getPosition()
        bint resPosition()
        bint setPosSettings(unsigned char, bint)
        bint setPinOut(unsigned char, unsigned char, unsigned short)
        bint invEncoder(bint)
        bint setServoLimit(unsigned short, unsigned short) 
        unsigned short getServoWidth()
