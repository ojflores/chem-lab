def example_equation(data_a, data_b, optional_data=False):
    """
    :param data_a: integer - data_a description
    :param data_b: integer - data_b description
    :param optional_data: boolean - optional_data description
    :return: integer - return description
    """
    if optional_data:
        return data_a * data_b
    return data_a + data_b

def true_ph(barometric_pressure,water_vapor_pressure,height_of_liquid_column):

  """
  :param barometric_pressure: decimal - the barometric pressure
  :param water_vapor_pressure: decimal - the water vapor pressure
  :param height_of_liquid_column: decimal - the heigh of liquid column
  """
  return (barometric_pressure - water_vapor_pressure - (height_of_liquid_column/13.6))

def true_moles(true_ph,initial_mensiscus_level,final_meniscus_level,room_temperature):
  """
  :param true_ph: decimal - the true ph
  :param initial_meniscus_level: decimal - the initial meniscus level
  :param final_meniscus_level: decimal - the final meniscus level
  :param room_temperature: decimal - the temperature of the room in celsius
  """
  return (0.000016034*true_ph*(initial_meniscus_level-final_meniscus_level)/(273.15+room_temperature))

def true_avag(average_current,total_time,true_moles):
  return (3121000000000000000*average_current*total_time/true_moles)

#This function does one more calculation and lets the user know whether his/her calculation is correct
def avag_check(avagt,true_avag,electrons_per_mole):
  if(abs(electrons_per_mole-true_avag) <4500000000000000000000):
    #alert user "Your 'electrons per mole' value is consistent with the data entered."
    return True
  else:
    return False

#checks for relatively valid ph
def ph_check(phydrogent,hydrogen_pressure,true_ph):
  if(abs(hydrogen_pressure-true_ph) < 0.24):
    #"Your calculated hydrogen pressure is consistent with the data entered.
    return True
  else:
    #Your calculated hydrogen pressure is NOT consistent with the data entered.
    return False


