from typing import Tuple
from .drone_utils import Drone
  
class DroneFleet:
    def __init__(self):
        self.drones = {}
    
    def add_drone(self, drone: Drone):
        self.drones[drone.drone_id] = drone
    
    def remove_drone(self, drone: Drone):
        del self.drones[drone.drone_id]
    
    def update_swarm(self, dt: float):
        for drone in self.drones.values():
            if drone.status != "dead":
                drone.update_position(dt)
    
    def assign_delivery(self, package: Package):
        nearest_drone = self.find_nearest_available_drone(package.destination)
        if nearest_drone:
            nearest_drone.set_destination(package.destination)
            nearest_drone.status = "en_route"
    
    def find_nearest_available_drone(self, destination: Tuple[float, float]) -> Drone:
        available_drones = [drone for drone in self.drones.values() if drone.status == "idle"]
        if not available_drones:
            return None
        return min(available_drones, key=lambda d: d.distance_to_destination())
            
    def get_idle_drones(self):
            return [drone for drone in self.drones.values() if drone.status == "idle"]

    def reroute_failed_drones(self):
            for drone in self.drones.values():
                if drone.status == "en_route" and drone.is_low_battery():
                    new_destination = self.find_nearest_charging_station(drone.position)
                    drone.reroute(new_destination)