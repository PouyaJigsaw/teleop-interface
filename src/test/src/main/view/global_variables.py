
tutorial_mode = False
bar_controller = False #true stop, false active


social_mode = True 
social_counterbalance = True
nonsocial_counterbalance = False

"""
H - AI - AI - H ==> T-F --- Type A
AI - H - H - AI ==> F-T --- Type B
H - AI - H - AI ==> T-T --- Type C
AI - H - AI - H ==> F-F --- Type D

"""

second_round = False # false is second round, true is first round



in_inspection = False #check whether in inspection screen or not



is_code_list_2 = False #False is Red Papers, True is Blue Papers


second_round_diff = None

if second_round: 
    second_round_diff = 50 
else: 
    second_round_diff = 0





#Non-Social - DS1 for AI and DS2 for Human
ds1_scoreloss_nonsocial = 200 - second_round_diff
ds2_scoreloss_nonsocial = 250 - second_round_diff
ds3_scoreloss_nonsocial = 150  - second_round_diff #AI #Human?


#Social - DS1 for Human and DS2 for AI
ds1_scoreloss_social = 250 - second_round_diff
ds2_scoreloss_social = 200 - second_round_diff
ds3_scoreloss_social = 150  - second_round_diff #AI #Human?





#Social | Non-Social
#===================
# Human    |    AI
#-------------------
# AI       |   Human
#-------------------

