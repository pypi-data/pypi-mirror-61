# distutils: language = c++
# cython: language_level = 3

from iarduino_I2C_Encoder cimport iarduino_I2C_Encoder
#from time import sleep

DEF_CHIP_ID_FLASH     = 0x3C
DEF_CHIP_ID_METRO     = 0xC3
DEF_MODEL_ENC         = 0x09

# Адреса регистров модуля:    
REG_FLAGS_0           = 0x00
REG_BITS_0            = 0x01
REG_FLAGS_1           = 0x02
REG_BITS_1            = 0x03
REG_MODEL             = 0x04
REG_VERSION           = 0x05
REG_ADDRESS           = 0x06
REG_CHIP_ID           = 0x07
REG_ENC_FREQUENCY_L   = 0x08
REG_ENC_FREQUENCY_H   = 0x09
REG_ENC_KEY           = 0x10
REG_ENC_KEY_TIM       = 0x11
REG_ENC_PIN_SET       = 0x12
REG_ENC_RES_SET       = 0x13
REG_ENC_RES_CNT_L     = 0x14
REG_ENC_RES_CNT_H     = 0x15
REG_ENC_ENC_CNT_LT    = 0x16
REG_ENC_ENC_CNT_RT    = 0x17
REG_ENC_ENC_SET       = 0x18
REG_ENC_SER_MIN_L     = 0x1A
REG_ENC_SER_MIN_H     = 0x1B
REG_ENC_SER_MAX_L     = 0x1C
REG_ENC_SER_MAX_H     = 0x1D
REG_ENC_SER_NOW_L     = 0x1E
REG_ENC_SER_NOW_H     = 0x1F
                            
# Позиция битов и флагов:     
ENC_KEY_PUSHED        = 0x80
ENC_KEY_RELEASED      = 0x40
ENC_KEY_PRESSED       = 0x20
ENC_KEY_TRIGGER       = 0x10
ENC_KEY_HOLD_05       = 0x08
ENC_KEY_HOLD_10       = 0x04
ENC_KEY_HOLD_20       = 0x02
ENC_KEY_CHANGED       = 0x01
ENC_PIN_MAX_TURN      = 0xF0
ENC_PIN_MODE          = 0x0F
ENC_PIN_MODE_OFF      = 0b00
ENC_PIN_MODE_KEY      = 0b00
ENC_PIN_MODE_TRG      = 0b00
ENC_PIN_MODE_PWM      = 0b00
ENC_PIN_MODE_PWM_LOG  = 0b01
ENC_PIN_MODE_SER      = 0b01
ENC_PIN_MODE_DAC      = 0b01
ENC_RES_SIGN_EN       = 0x80
ENC_RES_RESET         = 0x40
ENC_RES_MAX_TURN      = 0x3F
ENC_RES_SIGN          = 0x80
ENC_ENC_INV_DIR       = 0x01

KEY_PUSHED            = 1   
KEY_RELEASED          = 2   
KEY_PRESSED           = 3   
KEY_TRIGGER           = 4   
KEY_HOLD_05           = 5   
KEY_HOLD_10           = 6   
KEY_HOLD_20           = 7   
KEY_CHANGED           = 8   
KEY_TIME_PRESSED      = 9   
ENC_TURN              = 0   
ENC_TURN_LEFT         = 1   
ENC_TURN_RIGHT        = 2   


cdef class pyiArduinoI2Cencoder:
    cdef iarduino_I2C_Encoder c_module

    def __cinit__(self, address=None, auto=None):

        if address is not None:

            self.c_module = iarduino_I2C_Encoder(address)

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля,"
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

        else:

            self.c_module = iarduino_I2C_Encoder()

            if auto is None:
                #sleep(.5)
                if not self.c_module.begin():

                    print("ошибка инициализации модуля.\n"
                          "Проверьте подключение и адрес модуля, "
                          " возможно не включен интерфейс I2C.\n"
                          " Запустите raspi-config и включите интерфейс"
                          ", инструкция по включению:"
                          " https://wiki.iarduino.ru/page/raspberry-i2c-spi/")

    def begin(self):
        return self.c_module.begin()

    def getPullI2C(self):
        return self.c_module.getPullI2C()

    def setPullI2C(self, flag = True):
        if flag is not True:
                return self.c_module.setPullI2C(flag)
        else:
                return self.c_module.setPullI2C(True)

    def changeAddress(self, unsigned char newAddr):
        return self.c_module.changeAddress(newAddr)

    def reset(self):
        return self.c_module.reset()

    def getAddress(self):
        return self.c_module.getAddress()

    def getVersion(self):
        return self.c_module.getVersion()

    def getButton(self, typ):
        return self.c_module.getButton(typ)

    def getEncoder(self, direction = ENC_TURN):
        if direction is not ENC_TURN:
            return self.c_module.getEncoder(direction)
        else:
            return self.c_module.getEncoder(ENC_TURN)

    def getPosition(self):
        return self.c_module.getPosition()

    def resPosition(self):
        return self.c_module.resPosition()

    def setPosSettings(self, turn, sign = False):
        if sign is not False:
            return self.c_module.setPosSettings(turn, sign)
        else:
            return self.c_module.setPosSettings(turn, False)

    def setPinOut(self, mode, turn=0, freq=0):
        if turn is not 0 and freq is not 0:
            return self.c_module.setPinOut(mode, turn, freq)
        elif turn is not 0:
            return self.c_module.setPinOut(mode, turn, 0)
        else:
            return self.c_module.setPinOut(mode, 0, 0)

    def invEncoder(self, flg):
        return self.c_module.invEncoder(flg)

    def setServoLimit(self, mini, maxi):
        return self.c_module.setServoLimit(mini, maxi)

    def getServoWidth(self):
        return self.c_module.getServoWidth()

