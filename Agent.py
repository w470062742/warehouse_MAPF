import copy


class Pickup(object):
    def __init__(self, item, worker):
        self.target_list = [item, worker, item]
        self.state = 0

    def other_worker_that_needs_item(self, workers, is_copy):
        for worker in workers:
            if worker.items and worker.items[0]:
                for item in worker.items[0]:
                    if item.id == self.target_list[0].id:
                        if not is_copy:
                            worker.remove_item(item)
                        return worker
        return None

    def advance_pickup_state(self, workers, is_copy):
        if self.state == 1:
            other_worker = self.other_worker_that_needs_item(workers, is_copy)
            if other_worker:
                self.target_list[1] = other_worker
                return True
            else:
                self.state += 1
                return True
        elif self.state == 2:
            self.target_list[0].booked = False
            return False
        else:
            self.state += 1
            return True



    def get_target(self):
        return self.target_list[self.state]

    def is_carrying_shelf(self):
        return self.state > 0

class Agent(object):
    def __init__(self, pos, id):
        self.id = id
        self.pos = pos
        self.path = []
        self.pickup = None
        self.walking_path = []
        self.target_path = []
        self.is_copy = False
        self.is_carrying_shelf = False
        self.was_at_target = False

    def copy(self):
        new_agent = Agent(self.pos, self.id)
        new_agent.path = self.path.copy()

        if self.pickup:
            # new_agent.pickup = Pickup(self.pickup.target_list[0], self.pickup.target_list[1])
            # new_agent.pickup.state = self.pickup.state
            new_agent.pickup = copy.deepcopy(self.pickup)

        new_agent.walking_path = self.walking_path.copy()
        new_agent.target_path = self.target_path.copy()
        new_agent.is_copy = self.is_copy
        new_agent.is_carrying_shelf = self.is_carrying_shelf
        new_agent.was_at_target = self.was_at_target

        return new_agent

    def move_on_path(self, steps, pickup):
        "This method is used in WHCA"

        if len(self.path) <= steps:
            self.pos = self.path[-1]
            self.walking_path += self.path[1:]
            if pickup:
                self.target_path += [pickup.target_list[0].id for x in self.path[1:]]
            else:
                self.target_path += [-1 for x in self.path[1:]]
        else:
            self.pos = self.path[steps]
            self.walking_path += self.path[1:steps+1]
            if pickup:
                self.target_path += [pickup.target_list[0].id for x in self.path[1:steps+1]]
            else:
                self.target_path += [-1 for x in self.path[1:steps+1]]
        # reset pos node for next interation
        self.pos.g = None
        self.pos.h = None
        self.pos.f = None
        self.pos.came_from = None
        self.pos.depth = 0

    def one_step_in_path(self, other=None):
        "This method is used in DKBR"

        if other:
            print("other in one step BEFORE POP is:")
            print([c.id for c in other.path])

        if len(self.path) > 1:
            self.path.pop(0)
            if other:
                print("other in one step is:")
                print([c.id for c in other.path])
            self.pos = self.path[0]
            #print("new pos is %d "% (self.pos.id))
            self.walking_path += [self.pos]
        elif len(self.path) > 0:
            self.pos = self.path[0]
            self.walking_path += [self.pos]
            #print("standing still at %d " % (self.pos.id))


    def done_with_target(self):
        if self.was_at_target:
            self.was_at_target = False
            return True
        elif self.pos.coordinates == self.pickup.get_target().coordinates:
            self.was_at_target = True
            return False
        else:
            self.was_at_target = False
            return False
