relax_tasks = [7, 11]
mental_stress_tasks = [14, 15]
physical_tasks = [10, 18]
ema_tasks = [3, 6, 9, 13, 17]
IAPS_neutral_tasks = [12]
IAPS_relax_tasks = [2, 8]
IAPS_stress_tasks = [5, 16]

import numpy as np
task_ids = np.arange(1, 19)

task_names = [
    'RelaxingMusic1',
    'DescribingRelaxingPics1',
    'EMA1',
    'ViewingIAPS',
    'DescribingStressfulPics1',
    'EMA2',
    'RelaxingMusic2',
    'DescribingRelaxingPics2',
    'EMA3',
    'Cycling',
    'RelaxingMusic3',
    'DescribingNeutralPics',
    'EMA4',
    'MentalMath',
    'StroopTest',
    'DescribingStressfulPics2',
    'EMA5',
    'Marching'
]