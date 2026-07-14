from generator.behavior_engine import assign_profile
from generator.behavior_engine import get_profile

for i in range(10):

    profile = assign_profile()

    print(profile)

    print(get_profile(profile))

    print("-"*60)