import math

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

#True Moles
def true_moles(true_ph,initial_mensicus_level,final_mensicus_level,room_temperature):
    return (0.000016034*true_ph*(initial_mensicus_level-final_mensicus_level)/(273.15+room_temperature))

#check for valid moles
def mole_check(moles_hydrogen,true_moles):
    if(abs(moles_hydrogen-true_moles) < 0.0000022):
        #"Your calculation of moles hydrogen gas is consistent with the data entered."
        return True
    else:
        #"Your calculation of moles hydrogen gas is NOT consistent with the data entered."
        return False

#true ka
def true_ka(a_acid,a_buffer,a_base):
    return (0.0000977*(a_acid-a_buffer)/a_buffer-a_base)

#checks ka
def ka_check(ka,true_ka):
    if(abs(ka-true_ka) < 0.00002):
        #"Your calculated equilibrium constant is consistent with the data entered.
        return True
    else:
        #"Your calculated equilibrium constant is NOT consistent with the data entered.
        return False
       
       
#MgO enthalpy lab

#initial temps equation
def mgTi(mg_reaction_initiation_time,mg_slope_before_addition,mg_intercept_before_addition):
    return (mg_reaction_initiation_time*mg_slope_before_addition+mg_intercept_before_addition)
    
#final temps equation
#CcTf: this is the equation for the final temperature of the calorimeter constant lab
def calorimeter_constant_lab(reaction_initiation_time,cc_slope_after_addition,cc_intercept_after_addition):
    return(reaction_initiation_time*cc_slope_after_addition+cc_intercept_after_addition)
    
#final temp check
def final_temp_check(final_temperature,true_final_temperature):
    if(abs(final_temperature-true_final_temperature) < 0.02):
        #"Your calculated final temperature is consistent with the data entered."
        return True
    #"Your calculated final temperature is NOT consistent with the data entered."
    return False

#collisionary 5000

#calorimeter constant equation
def ccal_true(oxalic_acid_mass,cctf,ccti,na_oh_mass):
    return((663.76*oxalic_acid_mass/(cctf-ccti))-4.04*oxalic_acid_mass+na_oh_mass)

def ccal_check(calorimeter_constant,ccal_true):
    if(abs(calorimeter_constant-ccal_true) < 1.2):
        #,"Your calculated calorimeter constant is consistent with the data entered.",
        return True
    else:
        #"Your calculated calorimeter constant is NOT consistent with the data entered.
        return False
    
def molar_mg_enthalpy_equation(magnesium_mass,mg_hci_mass,ccal_true,mgtf,mgti):
    return(-0.024305*((magnesium_mass+mg_hci_mass)*3.68+ccal_true)*mgtf-mgti/magnesium_mass)

def enthalpy_check(mg_molar_enthalpy,mgenthalpy):
    if(abs(mg_molar_enthalpy-mgenthalpy) < 2):
        #"Your calculated enthalpy is consistent with the data entered."
        return True
    else:
        #"Your calculated enthalpy is NOTconsistent with the data entered."
        return False
    
def mgo_enthalpy(mgo_mass,mgo_hcl_mass,ccal_true,mgotf,mgoti):
    return (-0.040304*((mgo_mass+mgo_hcl_mass)*3.86+ccal_true)*(mgotf-mgoti)/mgo_mass)

def enthalpy_check_mgo(mgo_molar_enthalpy,mgoenthalpy):
  if(abs(mgo_molar_enthalpy-mgoenthalpy) < 1):
    #"Your calculated enthalpy is consistent with the data entered."
    return True
  else:
    #,"Your calculated enthalpy is NOT consistent with the data entered.")
    return False

def true_wavelength_equation(distance_along_white_board,distance_to_white_board):
    return(833.333*distance_along_white_board/(math.sqrt(distance_to_white_board**2+distance_along_white_board**2)))

def wave_length_check(calculated_wavelength,true_wavelength):
    if(abs(calculated_wavelength-true_wavelength)<0.6):
      #"Your calculated wavelength is consistent with the data entered."
      return True
    else:
      #,"Your calculated wavelength is NOT consistent with the data entered."
      return False

def true_photon_energy(wavelength):
    return (0.0000000000000001986449/wavelength)

def energy_check(energy,true_energy):
    if(abs(energy-true_energy) < 0.00000000000000000002):
      #"Your calculated energy is consistent with the data entered."
      return True
    else:
      #,"Your calculated energy is NOT consistent with the data entered."
      return False

#initial quantum number equation
#I'm not confident I understand what is occuring
#with the quantum number equations, so I am not
#including them to avoid disaster and or innacuracy