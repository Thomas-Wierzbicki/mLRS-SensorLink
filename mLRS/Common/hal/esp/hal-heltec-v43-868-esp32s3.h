//*******************************************************
// Copyright (c) MLRS project
// GPL3
// https://www.gnu.org/licenses/gpl-3.0.de.html
//*******************************************************
// hal
//********************************************************

//-------------------------------------------------------
// ESP32-S3, Heltec WiFi LoRa 32 V4.3, SX1262, TX/RX
//-------------------------------------------------------

#define DEVICE_HAS_SINGLE_LED
#define DEVICE_HAS_NO_DEBUG
//#define DEVICE_HAS_NO_SERIAL


//-- UARTS
// UARTB = serial port
// UART = output port, SBus or whatever
// UARTF = debug port

#define UARTB_USE_SERIAL
#ifdef DEVICE_IS_TRANSMITTER
#define UARTB_BAUD TX_SERIAL_BAUDRATE
#define UARTB_TXBUFSIZE TX_SERIAL_TXBUFSIZE
#define UARTB_RXBUFSIZE TX_SERIAL_RXBUFSIZE
#else
#define UARTB_BAUD RX_SERIAL_BAUDRATE
#define UARTB_TXBUFSIZE           RX_SERIAL_TXBUFSIZE
#define UARTB_RXBUFSIZE           RX_SERIAL_RXBUFSIZE
#endif


#define UARTF_USE_SERIAL
#define UARTF_BAUD                115200


//-- SX1: SX12xx & SPI

#define SPI_CS_IO                 IO_P8
#define SPI_SCK IO_P9
#define SPI_MISO IO_P11
#define SPI_MOSI IO_P10
#define SPI_FREQUENCY             10000000L
#define SX_RESET                  IO_P12
#define SX_DIO                    IO_P14
#define SX_BUSY IO_P13
#define SX126X_USE_DIO2_RF_SWITCH

IRQHANDLER(void SX_DIO_EXTI_IRQHandler(void);)

void sx_init_gpio(void)
{
    gpio_init(SX_BUSY, IO_MODE_INPUT_PU);
    gpio_init(IO_P7, IO_MODE_OUTPUT_PP_HIGH); // FEM supply
    gpio_init(IO_P2, IO_MODE_OUTPUT_PP_HIGH); // KCT8103L enable
    gpio_init(IO_P5, IO_MODE_OUTPUT_PP_LOW);  // RX LNA
    gpio_init(SX_RESET, IO_MODE_OUTPUT_PP_HIGH);
    gpio_init(SX_DIO, IO_MODE_INPUT_ANALOG);
}

IRAM_ATTR bool sx_busy_read(void) { return gpio_read_activehigh(SX_BUSY); }
IRAM_ATTR void sx_amp_transmit(void) { gpio_high(IO_P5); }
IRAM_ATTR void sx_amp_receive(void) { gpio_low(IO_P5); }

void sx_dio_init_exti_isroff(void) { detachInterrupt(SX_DIO); }
void sx_dio_enable_exti_isr(void) { attachInterrupt(SX_DIO, SX_DIO_EXTI_IRQHandler, RISING); }
IRAM_ATTR void sx_dio_exti_isr_clearflag(void) {}


// PRG is also the ESP32-S3 boot strap. Press after startup to bind.
void button_init(void) { gpio_init(IO_P0, IO_MODE_INPUT_PU); }
IRAM_ATTR bool button_pressed(void) { return gpio_read_activelow(IO_P0); }

#ifdef DEVICE_IS_TRANSMITTER
// Hold GPIO4 low at startup to select CLI on USB.
#define DEVICE_HAS_COM_ON_SERIAL
bool ser_or_com_init(void)
{
    gpio_init(IO_P4, IO_MODE_INPUT_PU);
    return !gpio_read_activelow(IO_P4);
}
#define DEVICE_HAS_I2C_DISPLAY
#define I2C_SDA_IO IO_P17
#define I2C_SCL_IO IO_P18
#define I2C_CLOCKSPEED 400000L
// Status-only OLED: no five-way switch is fitted.
void fiveway_init(void) {}
IRAM_ATTR uint8_t fiveway_read(void) { return 0; }
#endif

//-- LEDs

#define LED_RED                   IO_P35
// Arduino ESP32 2.x: hardware PWM, 13/255 duty (~5%).
#define HELTEC_LED_PWM_CHANNEL    7
#define HELTEC_LED_PWM_DUTY       3
static bool heltec_led_is_on = false;

void leds_init(void)
{
    gpio_init(IO_P36, IO_MODE_OUTPUT_PP_LOW); // OLED Vext
    gpio_init(IO_P21, IO_MODE_OUTPUT_PP_LOW); // OLED reset
    delay(10);
    gpio_high(IO_P21);
    delay(10);
    gpio_init(LED_RED, IO_MODE_OUTPUT_PP_LOW);
    ledcSetup(HELTEC_LED_PWM_CHANNEL, 5000, 8);
    ledcWrite(HELTEC_LED_PWM_CHANNEL, 0);
    ledcAttachPin(LED_RED, HELTEC_LED_PWM_CHANNEL);
    heltec_led_is_on = false;
}

void led_red_off(void)
{
    if (!heltec_led_is_on) return;
    heltec_led_is_on = false;
    ledcWrite(HELTEC_LED_PWM_CHANNEL, 0);
}
void led_red_on(void)
{
    if (heltec_led_is_on) return;
    heltec_led_is_on = true;
    ledcWrite(HELTEC_LED_PWM_CHANNEL, HELTEC_LED_PWM_DUTY);
}
void led_red_toggle(void)
{
    if (heltec_led_is_on) led_red_off();
    else led_red_on();
}


//-- POWER

// Initial low-power profile. +13 dB nominal FEM gain in its linear range.
// Output levels require hardware measurement at 868 MHz.
#define POWER_GAIN_DBM 13
#define POWER_SX126X_MAX 0
#define POWER_USE_DEFAULT_RFPOWER_CALC
#define RFPOWER_DEFAULT 0
const rfpower_t rfpower_list[] = {
    { .dbm = 4, .mW = 3 },
    { .dbm = 10, .mW = 10 },
    { .dbm = 13, .mW = 20 },
};
