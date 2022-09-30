import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pickle


current = ctrl.Antecedent(np.arange(0, 101, 1), 'current')
others = ctrl.Antecedent(np.arange(0, 101, 1), 'others')
green = ctrl.Consequent(np.arange(5, 45.5, 0.5), 'green')


current['low'] = fuzz.trapmf(current.universe, [0, 0, 20, 45])
current['medium'] = fuzz.trapmf(current.universe, [20, 35, 65, 80])
current['high'] = fuzz.trapmf(current.universe, [55, 80, 100, 100])

others['low'] = fuzz.trapmf(others.universe, [0, 0, 20, 45])
others['medium'] = fuzz.trapmf(others.universe, [20, 35, 65, 80])
others['high'] = fuzz.trapmf(others.universe, [55, 80, 100, 100])

green['verylow'] = fuzz.trapmf(green.universe, [5, 5, 10, 15])
green['low'] = fuzz.trapmf(green.universe, [10, 15, 20, 25])
green['medium'] = fuzz.trapmf(green.universe, [20, 25, 30, 35])
green['high'] = fuzz.trapmf(green.universe, [30, 35, 45, 45])


rule1 = ctrl.Rule(current['low'] & others['low'], green['low'])
rule2 = ctrl.Rule(current['low'] & others['medium'], green['verylow'])
rule3 = ctrl.Rule(current['low'] & others['high'], green['verylow'])
rule4 = ctrl.Rule(current['medium'] & others['low'], green['medium'])
rule5 = ctrl.Rule(current['medium'] & others['medium'], green['low'])
rule6 = ctrl.Rule(current['medium'] & others['high'], green['low'])
rule7 = ctrl.Rule(current['high'] & others['low'], green['high'])
rule8 = ctrl.Rule(current['high'] & others['medium'], green['high'])
rule9 = ctrl.Rule(current['high'] & others['high'], green['medium'])


green_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

green_time = ctrl.ControlSystemSimulation(green_ctrl)

pickle.dump(green_time, open('green_time.pkl', 'wb'))

green_time.input['current'] = 12
green_time.input['others'] = 37

# Crunch the numbers
green_time.compute()
print(green_time.output['green'])
