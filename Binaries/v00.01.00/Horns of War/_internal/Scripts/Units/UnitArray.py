from Scripts.Units.Unit import Unit

class UnitArray():

    def __init__(self):
        self.unit_array = []
    
    def get_unit_array(self):
        return self.unit_array


    def print_units(self):
        print("units in array: ")
        for unit in self.unit_array:
            print(unit)
            unit.toString()


    # IS_EMPTY
    # Returns true if there is no unit in the vector
    def is_empty(self):
        if not self.unit_array:
            return True
        else:
            return False
    

    # LENGTH
    # Returns number of units in the array
    def length(self):
        return len(self.unit_array)


    # GET
    # Returns unit in the indicated position
    def get_unit(self, position):
        return self.unit_array[position]
    

    # ADD_UNIT
    # Adds a unit to the unit array
    def add_unit(self, unit):
        self.unit_array.append(unit)


    # REMOVE_UNIT
    # deletes a unit from the vector
    def remove_unit(self, deleted_unit):

        self.unit_array.remove(deleted_unit)


    # GET_UNIT_IN_POSITION
    # returns the unit occupying the argument position
    def get_unit_in_position(self, position):
        for unit in self.unit_array:
            if unit.get_position() == position:
                return unit
        return None



    # TO_STRING
    # Returns a string with the units information
    def to_string(self):
        for unit in self.unit_array:
            print(type(unit).__name__ + " " + "(" + str(unit.get_position()[0]) + ", " + str(unit.get_position()[1]) + ")")

            
    
    def modify_unit_position(self, unit, nodebase):
        for i in range(len(self.unit_array)):
            if unit == self.unit_array[i]:
                self.unit_array[i].set_position(nodebase)



    def set_unit_moved(self, unit, moved):
        for i in range(len(self.unit_array)):
            if unit == self.unit_array[i]:
                self.unit_array[i].set_moved(moved)



