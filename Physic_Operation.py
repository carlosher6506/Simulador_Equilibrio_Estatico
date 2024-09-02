import math

angle_1 = 10
angle_2 = 10

def resolve_the_problem():
    block_weight = float(500)
    angle_1_rad = math.radians(angle_1)
    angle_2_rad = math.radians(angle_2)
    
    strain_1 = block_weight / (math.sin(angle_1_rad) + math.cos(angle_1_rad) * math.tan(angle_2_rad))
    strain_2 = block_weight / (math.sin(angle_2_rad) + math.cos(angle_2_rad) * math.tan(angle_1_rad))
    print(f'tension 1: {strain_1}')
    print(f' tension 2: {strain_2}')
    
    

resolve_the_problem()


