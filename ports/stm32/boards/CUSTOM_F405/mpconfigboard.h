#define MICROPY_HW_BOARD_NAME       "CUSTOM_F405"
#define MICROPY_HW_MCU_NAME         "STM32F405VG"

#define MICROPY_PY_THREAD           (1)

#define MICROPY_BOARD_EARLY_INIT    WeAct_Core_board_early_init
void WeAct_Core_board_early_init(void);

/* BOARD Ver 2.0 set 1 ，other set 0 ex.V1.3,V2.1 */
#define VERSION_V20 (0)
/* Use the built-in flash to change to 1 
   use the external flash to change to 0 */
#define MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE (0)


#define MICROPY_HW_HAS_SWITCH       (0)
#define MICROPY_HW_HAS_FLASH        (1)
#define MICROPY_HW_HAS_MMA7660      (0)
#define MICROPY_HW_HAS_LCD          (0)
#define MICROPY_HW_ENABLE_RNG       (0)
#define MICROPY_HW_ENABLE_RTC       (1)
#define MICROPY_HW_ENABLE_SERVO     (0)
#define MICROPY_HW_ENABLE_DAC       (0)
#define MICROPY_HW_ENABLE_USB       (1)
#define MICROPY_HW_ENABLE_SDCARD    (0) //PC12 Pın ?

// HSE is 12MHz
#define MICROPY_HW_CLK_PLLM (8)
#define MICROPY_HW_CLK_PLLN (168)
#define MICROPY_HW_CLK_PLLP (RCC_PLLP_DIV2)
#define MICROPY_HW_CLK_PLLQ (7)
#define MICROPY_HW_CLK_LAST_FREQ (1)

// The Feather has a 32kHz crystal for the RTC
#define MICROPY_HW_RTC_USE_LSE      (1)
#define MICROPY_HW_RTC_USE_US       (0)
#define MICROPY_HW_RTC_USE_CALOUT   (1)

// UART config

#define MICROPY_HW_BLE_UART_BAUDRATE (9600)

#define MICROPY_HW_UART1_NAME "CPU_UART1"
#define MICROPY_HW_UART1_TX (pin_B6)  // TX
#define MICROPY_HW_UART1_RX (pin_B7)  // RX

#define MICROPY_HW_UART3_NAME   "CPU_UART3"    // on RX / TX
#define MICROPY_HW_UART3_TX     (pin_B10)  // TX
#define MICROPY_HW_UART3_RX     (pin_B11)  // RX
#define MICROPY_HW_UART3_RTS    (pin_B14)  // MISO
#define MICROPY_HW_UART3_CTS    (pin_B13)  // SCK

#define MICROPY_HW_UART2_NAME   "CPU_UART2"   // on SDA/SCL
#define MICROPY_HW_UART2_TX     (pin_A2)  // TX
#define MICROPY_HW_UART2_RX     (pin_A3)  // RX
#define MICROPY_HW_UART2_RTS    (pin_A1)  // MISO
#define MICROPY_HW_UART2_CTS    (pin_A0)  // SCK

//~ GSM module uarts
#define MICROPY_HW_UART6_NAME   "CPU_UART6"   // on D5/D6
#define MICROPY_HW_UART6_TX     (pin_C6)  // TX
#define MICROPY_HW_UART6_RX     (pin_C7)  // RX

#define MICROPY_HW_UART4_NAME "CPU_UART4"
#define MICROPY_HW_UART4_TX (pin_C10)  // TX
#define MICROPY_HW_UART4_RX (pin_C11)  // RX


// SPI buses
#define MICROPY_HW_SPI1_NAME "SPI1"
#define MICROPY_HW_SPI1_NSS  (pin_A4) // FLASH CS
#define MICROPY_HW_SPI1_SCK  (pin_A5) // FLASH CLK
#define MICROPY_HW_SPI1_MISO (pin_A6) // FLASH MISO
#define MICROPY_HW_SPI1_MOSI (pin_A7) // FLASH MOSI
//~ #define MICROPY_HW_SPI2_NAME "SPI1"
//~ #define MICROPY_HW_SPI2_NSS  (pin_B12) // SD DETECT
//~ #define MICROPY_HW_SPI2_SCK  (pin_B13) // SCK
//~ #define MICROPY_HW_SPI2_MISO (pin_B14) // MISO
//~ #define MICROPY_HW_SPI2_MOSI (pin_B15) // MOSI

// CAN buses
//~ #define MICROPY_HW_CAN1_NAME "CAN1"
//~ #define MICROPY_HW_CAN1_TX   (pin_B9) // D10
//~ #define MICROPY_HW_CAN1_RX   (pin_B8) // D9


// SD card detect switch
//~ #define MICROPY_HW_SDCARD_DETECT_PIN        (pin_B12)
//~ #define MICROPY_HW_SDCARD_DETECT_PULL       (GPIO_PULLUP)
//~ #define MICROPY_HW_SDCARD_DETECT_PRESENT    (GPIO_PIN_RESET)

// USB config
#define MICROPY_HW_USB_FS              (1)
#define MICROPY_HW_USB_VBUS_DETECT_PIN (pin_A9)
#define MICROPY_HW_USB_OTG_ID_PIN      (pin_A10)

//~ #define MICROPY_HW_UART_REPL        PYB_UART_1
//~ #define MICROPY_HW_UART_REPL_BAUD   115200

// LEDs
#define MICROPY_HW_LED1             (pin_E11) // red
#define MICROPY_HW_LED2             (pin_E12) // green
#define MICROPY_HW_LED3             (pin_B0) // orange
#define MICROPY_HW_LED4             (pin_B1) // blue
#define MICROPY_HW_LED5             (pin_C3) // orange
#define MICROPY_HW_LED6             (pin_C4) // blue
#define MICROPY_HW_LED_ON(pin)      (mp_hal_pin_high(pin))
#define MICROPY_HW_LED_OFF(pin)     (mp_hal_pin_low(pin))

//~ #define MICROPY_HW_USRSW_PIN        (pin_E13)
#define MICROPY_HW_USRSW_PIN        (pin_B3)
#define MICROPY_HW_USRSW_PULL       (GPIO_NOPULL)
#define MICROPY_HW_USRSW_EXTI_MODE  (GPIO_MODE_IT_RISING)
#define MICROPY_HW_USRSW_PRESSED    (1)

// use external SPI flash for storage
// 4MB Flash 32Mbit
// 8MB Flash 64Mbit
// 16MB Flash 128Mbit
#define MICROPY_HW_SPIFLASH_SIZE_BITS (64 * 1024 * 1024)

#define MICROPY_HW_SPIFLASH_CS      (pin_A4)
#define MICROPY_HW_SPIFLASH_SCK     (pin_A5)

#if VERSION_V20
	#define MICROPY_HW_SPIFLASH_MISO    (pin_B4)
#else 
	#define MICROPY_HW_SPIFLASH_MISO    (pin_A6)
#endif

#define MICROPY_HW_SPIFLASH_MOSI    (pin_A7)

//spi flash
#if !MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE

#define MICROPY_HW_SPIFLASH_ENABLE_CACHE (1)
extern const struct _mp_spiflash_config_t spiflash_config;
extern struct _spi_bdev_t spi_bdev;
#define MICROPY_HW_BDEV_IOCTL(op, arg) ( \
    (op) == BDEV_IOCTL_NUM_BLOCKS ? (MICROPY_HW_SPIFLASH_SIZE_BITS / 8 / FLASH_BLOCK_SIZE) : \
    (op) == BDEV_IOCTL_INIT ? spi_bdev_ioctl(&spi_bdev, (op), (uint32_t)&spiflash_config) : \
    spi_bdev_ioctl(&spi_bdev, (op), (arg)) \
)
#define MICROPY_HW_BDEV_READBLOCKS(dest, bl, n) spi_bdev_readblocks(&spi_bdev, (dest), (bl), (n))
#define MICROPY_HW_BDEV_WRITEBLOCKS(src, bl, n) spi_bdev_writeblocks(&spi_bdev, (src), (bl), (n))
#define MICROPY_HW_BDEV_SPIFLASH_EXTENDED (&spi_bdev) // for extended block protocol

#endif
