# CMOS_Colposcope
Code for AutoFocussing a Colposcope by contrast index method.

### Contrast Index
The camera looks at the contrast between edges and moves the focus motor until the contrast is the sharpest.

## Algorithm:-
Records the values of contrast values while lens is moving from outermost to innermost point. Gets the maximum of these values and calculates the point of the lens where value was maximum and hence maximum focus. Then lens is moved in that position.

## Usage:-
*main1.py* contains the code for Serial communication and Data class and varibles.
Run *Camera.py* to run the camera. List will be shown for available COMs in the teminal. Enter the COM value in which the microcontroller is connected. This can be seen in Arduino IDE. After the successful connection is established, the code starts displaying video in *Camera Footage* window and values in the terminal.
A new image *open_cv_frame.png* will be created in the same directory where code is stored. Ensure that Camera.py and main1.py are stored in same directory.
Press *a* to start autofocus. This will halt the code for a sec and lens starts moving in outermost direction.
Press *ESC* key to close the Camera. If pressing doesn't work, click on the *Camera Footage* window and then press the key again. This also holds for autofocus.

### Miscellaneous
Lens -> SL-27135MFZ 2MP     https://www.aliexpress.com/item/32817509782.html
Microcontroller Board -> Custom, but in IDE used as Arduino Uno
Programmer(optional) -> Atmel SDK500 development board