from typing import Tuple
import math


class Drone:
    def __init__(
        self,
        drone_id: int,
        position: Tuple[float, float],
        velocity: Tuple[float, float],
        battery: float = 100.0
    ):
        self.drone_id = drone_id
        self.position = position 
        self.velocity = velocity
        self.battery = battery
        self.status = "idle"
        self.destination = (None,None,None) # x,y,altitude
    
    def update_position(self, dt: float):
        x, y = self.position
        vx, vy = self.velocity

        self.position = (
            x + vx * dt,
            y + vy * dt
        )

        self.consume_battery(dt)
    def consume_battery(self, dt: float):
        speed = self.get_speed()
        self.battery -= speed * 0.05 * dt

        if self.battery <= 0:
            self.battery = 0
            self.status = "dead"
            self.velocity = (0.0, 0.0)
    
    def distance_to_destination(self):
        if self.destination[0] is None:
            return float('inf')
        
        dx = self.destination[0] - self.position[0]
        dy = self.destination[1] - self.position[1]
        return math.sqrt(dx**2 + dy**2)

    
    def has_arrived(self, threshold: float = 1.0):
        return self.distance_to_destination() <= threshold
    
    def stop(self):
        self.velocity = (0.0, 0.0)
        self.status = "idle"
    
    def set_velocity_towards_destination(self, speed: float):
        """If the drone has a destination, set its velocity towards it with the given speed."""
        if self.destination[0] is None:
            return
        
        dx = self.destination[0] - self.position[0]
        dy = self.destination[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            self.stop()
            return
        
        vx = (dx / distance) * speed
        vy = (dy / distance) * speed
        self.velocity = (vx, vy)
    
    def get_speed(self):
        return (self.velocity[0]**2 + self.velocity[1]**2) ** 0.5      

    def is_low_battery(self, threshold: float = 20.0):
        return self.battery <= threshold

    def reroute(self, new_destination):
        self.set_destination(new_destination)
        self.set_velocity_towards_destination(self.get_speed())
    
    def handoff_package(self, next_drone):
        self.status = "handoff_complete"
        next_drone.status = "carrying_package"
        self.successor = next_drone.drone_id
        next_drone.predecessor = self.drone_id
    
    def get_eta(self):
        speed = self.get_speed()
        if speed == 0:
            return float('inf')
        distance = self.distance_to_destination()
        return distance / speed

    def set_destination(self, destination: Tuple[float, float]):
        self.destination = destination
        self.status = "en_route"