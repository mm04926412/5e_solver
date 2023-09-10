from matplotlib import pyplot as plt
from scipy.stats import nbinom
import numpy as np

def avg_dmg(damage_dice,static_modifier):
  return static_modifier+sum([i/2+0.5 for i in damage_dice])

def genAttacksRequiredDistribution(hp,damage_dice,static_damage, damage_trials = 10**6):
  attacks_required = np.zeros(damage_trials)
  damage_dealt = np.zeros(damage_trials)
  resolved = np.zeros(damage_trials,dtype=bool)
  while np.any(~resolved): #Simulatenously roll damage dice on all trials until all of them have halted
    attacks_required[~resolved] += 1 # Add one to attacks required if a trial hasnt resolved
    damage_dealt += sum([np.random.randint(1,dice+1,damage_trials) for dice in damage_dice]) + static_damage #Add damage
    resolved[damage_dealt >= hp] = True #resolve if damage is above the monsters hp
  attacks_required_count = list(np.unique(attacks_required,return_counts=True)) #get a count of the attacks required in dictionary format
  attacks_required_count[1] = attacks_required_count[1]/damage_trials #Normalize the counts
  print(attacks_required_count)
  return np.array(attacks_required_count)

def murder_probability_mass(x,hp,accuracy,damage_dice,static_damage,damage_trials = 10**6):
  attacks_required_distribution = genAttacksRequiredDistribution(hp,damage_dice,static_damage) #Generate attacks required distribution
  distributions = np.array([[(1-nbinom(attacks_required,accuracy).cdf(x_i-attacks_required)) for attacks_required in attacks_required_distribution[0]] for x_i in x])*attacks_required_distribution[1] #create mixture of negative binomial distributions per damage dice result
  return np.sum(distributions,axis=1) #create the weighted sum of negative binomial distributions on accuracy per damage dice determined number of attacks required to kill

x=list(range(20))
hp = 40
base_accuracy = 0.6
damage_dice = [6]
static_modifier = 4
plt.plot(x,murder_probability_mass(x,hp,base_accuracy,damage_dice,static_modifier))
plt.plot(x,murder_probability_mass(x,hp,base_accuracy-0.25,damage_dice,static_modifier+10))
plt.title("Enemy has " + str(hp) + " hp")
plt.ylabel("Chance enemy is still alive after x attacks")
plt.xlabel("attacks made")
non_sharpshooter_damage = avg_dmg([6],static_modifier)
sharpshooter_damage = avg_dmg([6],static_modifier+10)
non_sharpshooter_dpr = base_accuracy*avg_dmg([6],static_modifier)
sharpshooter_dpr = (base_accuracy-0.25)*avg_dmg([6],static_modifier+10)
plt.legend(["DPR: " + str(non_sharpshooter_dpr) + ", "+str(base_accuracy) + " chance to hit, " + str(non_sharpshooter_damage) + " damage","DPR: " + str(sharpshooter_dpr) + ", "+str(base_accuracy-0.25) +" chance to hit, "+str(sharpshooter_damage) + " damage"])
plt.savefig("output.png")

