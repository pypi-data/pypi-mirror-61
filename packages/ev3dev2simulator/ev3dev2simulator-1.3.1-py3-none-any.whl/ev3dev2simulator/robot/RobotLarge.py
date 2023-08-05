import math

from ev3dev2simulator.obstacle import ColorObstacle
from ev3dev2simulator.robot import BodyPart
from ev3dev2simulator.robot.Arm import Arm
from ev3dev2simulator.robot.ArmLarge import ArmLarge
from ev3dev2simulator.robot.Body import Body
from ev3dev2simulator.robot.ColorSensor import ColorSensor
from ev3dev2simulator.robot.Led import Led
from ev3dev2simulator.robot.Robot import Robot
from ev3dev2simulator.robot.TouchSensor import TouchSensor
from ev3dev2simulator.robot.UltrasonicSensorBottom import UltrasonicSensorBottom
from ev3dev2simulator.robot.UltrasonicSensorTop import UltrasonicSensor
from ev3dev2simulator.robot.Wheel import Wheel
from ev3dev2simulator.util.Util import apply_scaling


class RobotLarge(Robot):
    """
    Class representing the simulated robot. This robot has a number
    of parts defined by BodyParts and ExtraBodyParts.
    """


    def __init__(self, cfg, center_x: int, center_y: int, orientation: int):
        super(RobotLarge, self).__init__(cfg, center_x, center_y)

        img_cfg = cfg['image_paths']
        alloc_cfg = cfg['alloc_settings']


        address_motor_left = alloc_cfg['motor']['left']
        address_motor_right = alloc_cfg['motor']['right']
        address_cs_center = alloc_cfg['color_sensor']['center']
        address_cs_left = alloc_cfg['color_sensor']['left']
        address_cs_right = alloc_cfg['color_sensor']['right']
        address_ts_left = alloc_cfg['touch_sensor']['left']
        address_ts_right = alloc_cfg['touch_sensor']['right']
        address_ts_rear = alloc_cfg['touch_sensor']['rear']
        address_us_front = alloc_cfg['ultrasonic_sensor']['front']
        address_us_rear = alloc_cfg['ultrasonic_sensor']['rear']

        self.wheel_distance = apply_scaling(cfg['wheel_settings']['spacing'])

        self.left_body = Body(img_cfg, self, apply_scaling(39), apply_scaling(-22.5))
        self.right_body = Body(img_cfg, self, apply_scaling(-39), apply_scaling(-22.5))

        self.arm = Arm(img_cfg, self, apply_scaling(15), apply_scaling(102))
        self.arm_large = ArmLarge(img_cfg, apply_scaling(1450), apply_scaling(1100))

        self.left_wheel = Wheel(address_motor_left, img_cfg, self, (self.wheel_distance / -2), 0.01)
        self.right_wheel = Wheel(address_motor_right, img_cfg, self, (self.wheel_distance / 2), 0.01)

        self.center_color_sensor = ColorSensor(address_cs_center, img_cfg, self, 0, apply_scaling(84))
        self.left_color_sensor = ColorSensor(address_cs_left, img_cfg, self, apply_scaling(-69), apply_scaling(95))
        self.right_color_sensor = ColorSensor(address_cs_right, img_cfg, self, apply_scaling(69), apply_scaling(95))

        self.left_touch_sensor = TouchSensor(address_ts_left, img_cfg, self, apply_scaling(-65), apply_scaling(102), 'left')
        self.right_touch_sensor = TouchSensor(address_ts_right, img_cfg, self, apply_scaling(65), apply_scaling(102), 'right')
        self.rear_touch_sensor = TouchSensor(address_ts_rear, img_cfg, self, 0, apply_scaling(-165), 'rear')

        self.front_ultrasonic_sensor = UltrasonicSensor(address_us_front, img_cfg, self, apply_scaling(-22), apply_scaling(56))
        self.rear_ultrasonic_sensor = UltrasonicSensorBottom(address_us_rear, img_cfg, self, 0, apply_scaling(-145))

        self.left_brick_left_led = Led(img_cfg, self, apply_scaling(-20), apply_scaling(-55))
        self.left_brick_right_led = Led(img_cfg, self, apply_scaling(-60), apply_scaling(-55))

        self.right_brick_left_led = Led(img_cfg, self, apply_scaling(20), apply_scaling(-55))
        self.right_brick_right_led = Led(img_cfg, self, apply_scaling(60), apply_scaling(-55))

        self.movable_sprites = [self.left_wheel,
                                self.right_wheel,
                                self.left_body,
                                self.right_body,
                                self.center_color_sensor,
                                self.left_color_sensor,
                                self.right_color_sensor,
                                self.left_touch_sensor,
                                self.right_touch_sensor,
                                self.rear_touch_sensor,
                                self.rear_ultrasonic_sensor,
                                self.front_ultrasonic_sensor,
                                self.left_brick_left_led,
                                self.left_brick_right_led,
                                self.right_brick_left_led,
                                self.right_brick_right_led,
                                self.arm]

        self.sprites = self.movable_sprites.copy()
        self.sprites.append(self.arm_large)

        if orientation != 0:
            self._rotate(math.radians(orientation))


    def execute_arm_movement(self, dfp: float):
        """
        Move the robot arm by providing the speed of the center motor.
        :param dfp: speed in degrees per second of the center motor.
        """

        self.arm_large.rotate(dfp)


    def set_left_brick_led_colors(self, left_color, right_color):
        self.left_brick_left_led.set_color_texture(left_color)
        self.left_brick_right_led.set_color_texture(right_color)


    def set_right_brick_led_colors(self, left_color, right_color):
        self.right_brick_left_led.set_color_texture(left_color)
        self.right_brick_right_led.set_color_texture(right_color)


    def set_color_obstacles(self, obstacles: [ColorObstacle]):
        """
        Set the obstacles which can be detected by the color sensors of this robot.
        :param obstacles: to be detected.
        """

        self.center_color_sensor.set_sensible_obstacles(obstacles)
        self.left_color_sensor.set_sensible_obstacles(obstacles)
        self.right_color_sensor.set_sensible_obstacles(obstacles)


    def set_touch_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the touch sensors of this robot.
        :param obstacles: to be detected.
        """

        self.left_touch_sensor.set_sensible_obstacles(obstacles)
        self.right_touch_sensor.set_sensible_obstacles(obstacles)
        self.rear_touch_sensor.set_sensible_obstacles(obstacles)


    def set_falling_obstacles(self, obstacles):
        """
        Set the obstacles which can be detected by the wheel of this robot. This simulates
        the entering of a wheel in a 'hole'. Meaning it is stuck or falling.
        :param obstacles: to be detected.
        """

        self.left_wheel.set_sensible_obstacles(obstacles)
        self.right_wheel.set_sensible_obstacles(obstacles)
        self.rear_ultrasonic_sensor.set_sensible_obstacles(obstacles)


    def get_sensors(self) -> [BodyPart]:
        return [self.center_color_sensor,
                self.left_color_sensor,
                self.right_color_sensor,
                self.left_touch_sensor,
                self.right_touch_sensor,
                self.rear_touch_sensor,
                self.front_ultrasonic_sensor,
                self.rear_ultrasonic_sensor]


    def get_anchor(self) -> BodyPart:
        return self.left_body
