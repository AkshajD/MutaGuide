#imports
from collections import Counter

def get_positions(sample, target_residue):
  positions = []      #All positions of target residue in sample sequence
  #Find positions of target residue in sample sequence
  for p in range(0, len(sample)):
      if (sample[p] == target_residue):
          positions.append(p)
  return positions

def analyze(sequences, positions):
  num_sequences = len(sequences) - 1     #Number of total homologous AA sequences
  total_scores = []
  #Generate scores
  for p in positions:
    #print("Position: " + str(p + 1))        #Print position being analyzed
    string = ""     #String that will store all residues at said position

    for i in range(1, len(sequences)):
        string = string + sequences[i][p]   #All residues at the specified position 
    unique_residues = list(set(string))     #All different residues in string
    count = Counter(string)     #Counts number of each residue at said position
    position_scores = []
    for residue in unique_residues:     #For each unique residue
        residue_count = count[residue]      #Count number at specified position
        score = (residue_count / num_sequences) * 100.00      #Determine percent of residues at position
        position_scores.append([residue, score])
        """print("Percentage of " + residue + " is: " + str(score))        #Output score"""
    #print()
    total_scores.append([p, position_scores])
  return total_scores