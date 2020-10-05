"""
This program generates a list of residue sites to replace based on
their involvement in protein secondary structures, their presence
near the surface of the protein, or their presence in homologous proteins.
The program requires a Phyre2 Output file, as well as an input for the
target residue for replacement.

Author: Akshaj Darbar
Date: 2020-09-27
"""

#Python Modules
import sys
import os
from collections import Counter

#Custom Module
import sable

#Initializing Function
def assignPositionScores(positions, secondary_structure, homology_scores, RSA, surface):
  """This function assigns a score to each target residue position based on
  secondary structure at site, surface area, homology, and IDF regions"""
  
  temp = []
  for index in positions:
    position_score = 0
    secondary = False   #Part of alpha helix or beta sheet?
    IDF = False   #In IDF region?

    #Checking if position is part of double helix or beta sheet
    if (secondary_structure[index] == "E" or secondary_structure[index] == "H"):
      position_score = position_score - 2
      secondary = True

    #Checking if position is in an IDF (range of 10 residues on either side)
    lower_bound = index - 10
    upper_bound = index + 10
    if ((lower_bound >= 0 and upper_bound < len(secondary_structure)) and
        ("H" in secondary_structure[lower_bound:upper_bound] or
         "E" in secondary_structure[lower_bound:upper_bound])):
      position_score = position_score - 1
      IDF = True

    #Checking how much the residue is conserved in similar proteins
    residue_homology = 0
    for element in homology_scores:
      if int(element[0]) == index:
        for score in element[1]:
          if score[0] == "C":
            residue_homology = score[1]
    position_score = position_score + (100-residue_homology)/100.00

    #Adding Score for Surface Area
    if surface:
      position_score = position_score + float(RSA[index])

    #Appends all the scores/info from above into the large list
    temp.append([index, position_score, {'Homology': residue_homology,
                                           'Secondary Structure': secondary,
                                           'IDF': IDF, 'RSA': RSA[index]}])
  #Sorts by the score in ascending order
  temp = sorted(temp, key=lambda x: x[1])
  temp.reverse()  #Reverses list to descending order
  return temp

def get_file(path):
  """This functions opens the input file to be read"""
  
  try:
    f = open(path, "r")
    return f, True
  except FileNotFoundError:
    return "File not found", False

def get_sequences(file):
  """This function gets all the FASTA sequences from the PHYRE2 file"""
  
  #Add all sequences from Phyre2 Output file to an array called sequences
  sequences = []
  for line in file:
    if not line.startswith(">"):
      sequences.append(line.replace("    ", "").replace("\n", ""))
  return sequences

def get_positions(sample, target_residue):
  """This function finds the positions of the target residue in the sample
  sequence"""
  
  positions = []      #All positions of target residue in sample sequence
  #Find positions of target residue in sample sequence
  for p in range(0, len(sample)):
      if (sample[p] == target_residue):
          positions.append(p)
  return positions

def analyze_homology(sequences, positions):
  """This function checks how conserved a residue is across homologues"""
  num_sequences = len(sequences) - 1     #Number of total homologous AA sequences
  total_scores = []
  #Generate scores
  for p in positions:
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
    total_scores.append([p, position_scores])
  return total_scores

def output_to_file(homology_list, position_scores, positions):
  #Get input for where to save output file
  output_directory = input("Enter the path to the directory where you would" \
                           " like to save the output file: ")

  # Try to change current working directory to specified directory, and
  # keep getting an input from the user if the directory does not work
  dir_changed = False
  while not dir_changed:
    try:
      os.chdir(output_directory)
      dir_changed = True
    except:
      print("Error in finding directory. Please enter a correct path: ")

  output_file = open("MutaGuide_Output.txt", "w")
  output_file.write("Position\tHomology\tSecondary Structure\tIDF\t" \
                    "Surface Area\tScore\n")
  for x in position_scores:
    position = x[0]
    homology = x[2]['Homology']
    secondary = x[2]['Secondary Structure']
    IDF = x[2]['IDF']
    RSA = x[2]['RSA']
    score = x[1]
    output_file.write(f"{position+1}\t\t{homology:.2f}%\t\t{secondary}" \
                      f"\t\t\t{IDF}\t{RSA}\t\t{score}\n")
  output_file.write("\n")
  
  #Checking how much the residue is conserved in similar proteins
  for p in positions:
    output_file.write("Position " + str(p) + "\n")
    residue_homology = 0
    for element in homology_list:
      if int(element[0]) == p:
        for score in element[1]:
          output_file.write("Percentage of " + str(score[0]) + " is: "
                            + str(score[1]) + "\n")
    output_file.write("\n")
  output_file.close()

#Main Code
def main():
  """This is the main section of the code"""
  #Get user input for PHYRE2 output file
  path_to_file = input("Enter the path to the Phyre2 FASTA output file: ")

  #Open readable file and check if path exists
  input_file, file_found = get_file(path_to_file)
  
  if not file_found:    #path does not exist
    #Print error message and exit program
    print("File path entered cannot be found. Please run the program again")
    sys.exit()

  #if path does exist
  seqs = get_sequences(input_file)  #All the homologous sequences
  sample = seqs[0]    #User's inputted sequence
  input_file.close()

  #Residue the user is targetting
  target_res = input("Enter the FASTA code for the target residue: ")
  surface_res_input = input("Would you like residues on the surface "\
                            " of the protein? Answer Y or N: ")
  #Ask if user prefers residue on surface
  surface_res = True
  if surface_res_input.upper() == "Y":
    surface_res = True
  elif surface_res_input.upper() == "N":
    surface_res = False
  else:
    print("Input not recognized. Default set to optimizing for surface residues")
    surface_res = True
  print("Thank you! The program is now running and should take" +
        " between 5-10 minutes. Please do not close this window.\n")

  #Positions of target residue in sample sequence
  positions = get_positions(sample, target_res)
  #Conservation of the residue across all homologous sequences
  homology_scores = analyze_homology(seqs, positions)

  #Secondary Structure and Surface Area prediction using SABLE
  predictions = sable.main_function(sample)
  if "ERROR" in predictions:    #If sable class returns error message
    #print error message and exit program
    print("SABLE NOT RESPONDING. PLEASE TRY TO RUN THE PROGRAM AGAIN LATER")
    sys.exit()

  #Separate secondary structure and surface area predictions into variables
  secondary_structure = predictions[0]
  RSA = predictions[1]

  #Get scores for each position
  scores = assignPositionScores(positions, secondary_structure,
                                homology_scores, RSA, surface_res)

  #Output scores for each position to SHELL
  print("Position\tHomology\tSecondary Structure\tIDF\tSurface Area\tScore")
  for x in scores:
    position = x[0]
    homology = x[2]['Homology']
    secondary = x[2]['Secondary Structure']
    IDF = x[2]['IDF']
    RSA = x[2]['RSA']
    score = x[1]
    print(f"{position+1}\t\t{homology:.2f}%\t\t{secondary}\t\t\t{IDF}" \
          f"\t{RSA}\t\t{score}")

  output = input("Would you like to save the homology data and the data" \
                 " from above to a text file? Answer with a Y or N: ")
  if output.upper() == "Y":
    output_to_file(homology_scores, scores, positions)
  elif output.upper() != "N":
    print("Input not recognized. Data will not be saved to a file")

#Runs the program   
main()
