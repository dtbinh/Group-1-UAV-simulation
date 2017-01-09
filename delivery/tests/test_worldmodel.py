from delivery.model.worldmodel import WorldModel
from delivery.agents.baseStation import BaseStation
from delivery.agents.uav import Uav
import configparser
import unittest
from mesa.datacollection import DataCollector


class worldModel_Test(unittest.TestCase):
    def setUp(self):
        self.model = WorldModel()

    def test_init(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        self.assertEqual(self.model.width,config.getint('Grid', 'width'))
        self.assertEqual(self.model.height,config.getint('Grid', 'height'))
        self.assertEqual(self.model.pixel_ratio,config.getint('Grid', 'pixel_ratio'))
        self.assertEqual(self.model.range_of_base_station,config.getfloat('Basestation', 'range_of_base_station'))
        self.assertEqual(self.model.number_of_uavs_per_base_station,config.getint('Uav', 'number_of_uavs_per_base_station'))
        self.assertEqual(self.model.max_battery,config.getint('Uav','max_battery'))
        self.assertEqual(self.model.battery_low,config.getint('Uav','battery_low'))
        self.assertEqual(self.model.number_of_repellents,0)
        self.assertEqual(self.model.grid.width,config.getint('Grid', 'width'))
        self.assertEqual(self.model.grid.height,config.getint('Grid', 'height'))
        self.assertEqual(self.model.landscape.width, config.getint('Grid', 'width'))
        self.assertEqual(self.model.landscape.height, config.getint('Grid', 'height'))
        self.assertEqual(self.model.number_of_delivered_items,0)
        self.assertIsInstance(self.model.datacollector,DataCollector)


    def test_create_base_station(self):
        # Test: Place a base station at any valid position
        # After that the base station must be in the scheduler and be placed on the landscape grid
        self.model.landscape.place_obstacle((30,30))
        self.model.create_base_station(123,(30,30))

        found = False
        base = None
        for elem in self.model.grid.get_cell_list_contents((30,30)):
            if isinstance(elem,BaseStation):
                found = True
                base = elem
                break

        self.assertTrue(found)

        self.assertTrue(self.model.landscape.is_base_station_at((30,30)))

        self.assertIn(base,self.model.schedule.agents)

    def test_create_uav(self):
        # Test: Place a uav at a valid position

        base = BaseStation(model=self.model, pos=(30, 30), id=1, center=(30, 30), range_of_base_station=250)
        self.model.create_uav(uid=123,base_station=base)

        # Find UAV in grid
        found = False
        uav = None
        for elem in self.model.grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, Uav):
                uav = elem
                found = True
                break

        # Test: UAV is in grid
        self.assertTrue(uav.id,123)

        # Test: UAV is in perceived_world_grid
        found = False
        uav = None
        for elem in self.model.perceived_world_grid.get_cell_list_contents((30, 30)):
            if isinstance(elem, Uav):
                uav = elem

                break

        # Is it in perceived_world_grid?
        self.assertTrue(uav.id,123)

        # Test: The UAV has to be added to the schedule
        self.assertIn(uav,self.model.schedule.agents)

    def test_compute_number_of_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method...
        # 1st Test: No items created. Value should be 0

        self.assertEqual(self.model.compute_number_of_items(self.model),0)


        # Let us do some 1000 steps and hope some items were created
        for i in range(1,1000):
            self.model.step()

        # 2nd Test: Numbers should still match after 1000 steps!
        number_of_items = 0
        for base_station in self.model.schedule.agents_by_type[BaseStation]:
            number_of_items += base_station.get_number_of_items()

        self.assertEqual(self.model.compute_number_of_items(self.model), number_of_items)

    def test_computer_number_of_picked_up_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method..
        # 1st Test: No items created. Value should be 0
        self.assertEqual(self.model.compute_number_of_picked_up_items(self.model),0)

        # Let us do some 1000 steps and hope some items were created
        for i in range(1, 1000):
            self.model.step()

        # Make sure, we actually really created items at least..
        while self.model.compute_number_of_items(self.model) == 0:
            self.model.step

        number_of_picked_up_items = 0
        for base_station in self.model.schedule.agents_by_type[BaseStation]:
            number_of_picked_up_items += base_station.get_number_of_items(picked_up=True)
        return number_of_picked_up_items

        # 2nd Test: Numbers of picked up items
        self.assertEqual(self.model.compute_number_of_picked_up_items(self.model),number_of_picked_up_items)

    def test_compute_number_of_delivered_items(self):
        # Hard to test with specific values. But at least can test if my self-computed values match the values from the method..
        # 1st Test: no items created, none delivered. 0 should be result
        self.assertEqual(self.model.compute_number_of_delivered_items(self.model),0)

        # Let us do some 1000 steps and hope some items were created
        for i in range(1, 1000):
            self.model.step()

        # 2nd Test: Numbers should still match after 1000 steps!
        self.assertEqual(self.model.compute_number_of_delivered_items(self.model),self.model.number_of_delivered_items)

    def test_compute_average_walk_length(self):
        print("puhh..")

