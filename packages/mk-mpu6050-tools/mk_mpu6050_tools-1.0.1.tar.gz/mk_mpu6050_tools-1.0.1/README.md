# Mk MPU6050 Tools
## MkNxGn MPU - 6050 6-Axis Gyroscope Tools

Install with pip

    -pip3 install mk_mpu6050_tools

Make sure to have py smbus installed on your device.

Use this Module to use the:

    - MPU-6050



---



## Code Example
<pre><code>import mk_mpu6050_tools
import sleep

Chipset = mk_mpu6050_tools.MPU_6050()

while True:
    time.sleep(1)
    print(Chipset.Gyro.x, Chipset.Gyro.y)

</code></pre>

---

## Virtualizing
Mk MPU Tools comes with Panda3D code to make visualization easy.

Make sure to Install Panda3D to 

<pre><code>import mk_mpu6050_tools
import sleep

Chipset = mk_mpu6050_tools.MPU_6050()

from mk_mpu6050_tools import Visulize

Visulize.Run_visiulization_on_Gyro(Chipset.Gyro)

</code></pre>




---



## More on Virtualizing
Visualization comes with multiple models to use for visualization.

<pre><code>#    POSSIBLE MODELS
#    Visulize.MODELS.PLANE
#    Visulize.MODELS.TRUCK
#    Visulize.MODELS.DRONE
#    Visulize.MODELS.GRYO_MULTIPLEX - Default

SELECTED_MODEL = Visulize.MODELS.DRONE

Visulize.Run_visiulization_on_Gyro(Chipset.Gyro, model=SELECTED_MODEL)
</code></pre>





# Made By Mark.
### Endorsed By MkNxGn
#### Progressing Technology.

