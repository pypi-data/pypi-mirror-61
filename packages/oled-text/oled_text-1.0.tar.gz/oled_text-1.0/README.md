# OLED SSD1306 Text

Working with Adafruit's adafruit_ssd1306 library can be tedious if all you need is to output to your oled is some lines of text.
This is where this helper tool comes in handy.

### A minimal hello world:


```
from board import SCL, SDA
import busio
from oled_text.oled_text import OledText

i2c = busio.I2C(SCL, SDA)

# Create the display, pass its pixel dimensions
oled = OledText(i2c, 128, 64)

# Write to the oled
oled.text("Hello ...", 1)  # Line 1
oled.text("... world!", 2)  # Line 2

```

### More advanced examples

```
import time
from board import SCL, SDA
import busio
from oled_text.oled_text import OledText

i2c = busio.I2C(SCL, SDA)

# Instantiate the display, passing its dimensions (128x64 or 128x32)
oled = OledText(i2c, 128, 64)

# Output 5 lines (with auto_draw on, the display is painted after every line)
for i in range(1, 6):
	oled.text("Hello Line {}".format(i), i)

time.sleep(1)

# Replacing a single line (keeps the other lines)
oled.text("Brave new line", 2)
time.sleep(2)

# See the repaint framerate
for i in range(10):
    oled.text("Random: {}".format(random.randint(0, 100)), 2)
oled.clear()

# Setting multiple lines with manual .show() (only one display refresh)
oled.layout = OledText.layout_64_1big_3small()
oled.auto_show = False
oled.text("The Title", 1)
oled.text("Line 2 text", 2)
oled.text("Line 3 text", 3)
oled.text("Line 4 text", 4)
oled.show()
oled.auto_show = True
time.sleep(3)

# Use a custom display layout
oled.layout = {
    1: SmallLine(0, 0),
    2: BigLine(5, 15, font="Arimo.ttf", size=24),
    3: BigLine(5, 40, font="Arimo.ttf", size=18)
}
oled.text("I want my layout!")
oled.text("Custom 1", 2)
oled.text("Custom 2", 3)
time.sleep(3)

# Adding own graphics using a onDraw handler
oled.layout = OledText.layout_64_1big_center()
oled.on_draw = lambda draw: draw.rectangle((0, 0, 127, 63), outline=255, fill=0)
oled.text("The Fat Cat", 1)

time.sleep(4)
oled.clear()
```
