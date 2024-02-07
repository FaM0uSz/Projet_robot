from controller import Robot, Motor, DistanceSensor

# maximal speed allowed
MAX_SPEED = 12.3

# how many sensors are on the robot
MAX_SENSOR_NUMBER = 16

# maximal value returned by the sensors
MAX_SENSOR_VALUE = 1024

# minimal distance, in meters, for an obstacle to be considered
MIN_DISTANCE = 1.0

# minimal weight for the robot to turn
WHEEL_WEIGHT_THRESHOLD = 100

class MyController:
    def __init__(self, robot):
        self.robot = robot
        self.timestep = int(robot.getBasicTimeStep())
        
        # Get handles for motors
        self.left_wheel = self.robot.getDevice('left wheel')
        self.right_wheel = self.robot.getDevice('right wheel')
        
        # Set the maximum motor speed
        self.left_wheel.setPosition(float('inf'))
        self.right_wheel.setPosition(float('inf'))
        
        # Enable the motors
        self.left_wheel.setVelocity(0)
        self.right_wheel.setVelocity(0)
        
        # Get handles for distance sensors
        self.distance_sensors = []
        for i in range(MAX_SENSOR_NUMBER):
            sensor = self.robot.getDevice('so' + str(i))
            sensor.enable(self.timestep)
            self.distance_sensors.append(sensor)
        

    def run(self):
        while self.robot.step(self.timestep) != -1:
            # Initialize speed and wheel weight arrays
            speed = [0.0, 0.0]
            wheel_weight_total = [0.0, 0.0]
            
            # Compute wheel weights based on sensor readings
            for i, sensor in enumerate(self.distance_sensors):
                sensor_value = sensor.getValue()
                
                if sensor_value == 0:
                    speed_modifier = 0.0
                else:
                    distance = 5.0 * (1.0 - (sensor_value / MAX_SENSOR_VALUE))
                    
                    if distance < MIN_DISTANCE:
                        speed_modifier = 1 - (distance / MIN_DISTANCE)
                    else:
                        speed_modifier = 0.0
                
                wheel_weight_total[0] += 150 * speed_modifier if i < 4 else 0
                wheel_weight_total[1] += 150 * speed_modifier if i >= 4 and i < 12 else 0
            
            # Adjust motor velocities based on wheel weights
            if wheel_weight_total[0] > WHEEL_WEIGHT_THRESHOLD:
                speed[0] = 0.5 * MAX_SPEED
                speed[1] = -0.5 * MAX_SPEED
            elif wheel_weight_total[1] > WHEEL_WEIGHT_THRESHOLD:
                speed[0] = -0.5 * MAX_SPEED
                speed[1] = 0.5 * MAX_SPEED
            else:
                speed[0] = MAX_SPEED
                speed[1] = MAX_SPEED
                       
            # Set motor velocities
            self.left_wheel.setVelocity(speed[0])
            self.right_wheel.setVelocity(speed[1])

# create the Robot instance.
robot = Robot()

# Create an instance of the controller
controller = MyController(robot)

# Run the controller
controller.run()



#oui