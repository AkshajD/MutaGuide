# MutaGuide
> Author: [Akshaj Darbar](https://www.linkedin.com/in/akshaj-darbar)\
Date: 2020-10-05
## Description
A tool to help iGEM teams to optimize amino acid residue replacement in proteins, to allow for protein immobilization to the hardware.
## Background: Why Do We Want to Optimize Residue Replacement?
When attempting to attach a protein or polypeptide to a surface, it is important to be able to recognize and replace an amino acid residue that would allow for attachment without compromising function. To do this, one must consider the localization of the residue near the surface of the protein, its distance from the active site, its involvement in a secondary structure (either an alpha helix or a beta sheet), and its conservation in homologous protein sequences. Though much of this information can easily be accessed for proteins whose crystal structure and method of acting has already been determined, like proteins that could be found in PDB databases, proteins synthesized for a specific purpose require one to use various complex calculations and methods to predict the information listed above. These complicated steps often have to be performed manually, which can introduce several errors into the calculations that might result in incorrect predictions. Various online servers can also be used to automate some steps, but these servers are often difficult to combine with one another.  
Due to these difficulties, MutaGuide was developed to automate the process of obtaining secondary structure and surface area predictions and combining this with homology analysis to output optimal residues to replace.
## How It Works
1. Determines conservation of target residue across all protein homologues, based on output from PHYRE2 webserver.
2. Obtains predictions for secondary structure and relative solvent accessibility (RSA) from SABLE webserver.
3. Scores occurrences of target residue in the input sequence based on conservation from step 1, and secondary structure and RSA prediction (if user indicates preference for residues with high RSA) from step 2.
4. Outputs results with residues ordered from their scores.

For more information on how Phyre2 works: [Phyre2 Documentation](https://www.nature.com/articles/nprot.2015.053).

For more information on how SABLE works: [SABLE documentation](http://sable.cchmc.org/sable_doc.html).

## How to Use MutaGuide
First, download this repository to your computer. If you download using a ZIP file, make sure you extract the files and rename the folder to <b>MutaGuide</b>
Because the Phyre2 server takes extremely long to make predictions, the user must first enter their sequence and obtain a .txt file of the Phyre2 output, in the FASTA format, separately. This file can then be inputted into the MutaGuide program.
#### Running in Windows
Right now, to run the program in Windows, it is recommended to use the command prompt.
1. In the search bar on your computer, search for 'Command Prompt', and open the program.
2. Navigate to the directory where the code is saved: `cd C:/%USERPROFILE%/path/MutaGuide/MainCode/`
3. Run the `main.py` file: `python main.py`
4. Enter the path to the Phyre2 file when prompted.
   - In the example shown here, the test file provided with the MutaGuide program in the MutaGuide folder is provided with a relative path. If the file is saved outside of this    folder, provide the full path to the file:
   ```
   Enter the path to the Phyre2 FASTA output file: Phyre_output.txt
   ```
5. Indicate the FASTA code for the specific amino acid residue you would like to replace (targeting cystine in example below):
```
Enter the FASTA code for the target residue: C
```
6. Input Y for Yes, or N for No for whether you prefer residues closer to the surface of the protein:
```
Would you like residues on the surface of the protein? Answer Y or N: Y
```
7. Wait for the program to generate its output.
8. If you would like to save the output to a text file, enter Y. Otherwise, enter N.
   - If you chose to save the file, enter the path to the folder where you would like the file to be created and saved:
   ```
   Enter the path to the directory where you would like to save the output file: C:/path/
   ```
   The output text file will be saved in the specified folder with the name <b>MutaGuide_Output.txt</b>.
#### Running in Linux
1. Open the terminal in Linux by searching for it in the dashboard, or using the keyboard shortcut `Ctrl+Alt+T`
2. Navigate to the MutaGuide directory using the command `cd /path/MutaGuide`
3. Run the command `python main.py` to execute the script, and follow the instructions outlined in the Windows section above to use the code. 
> <b>Keep in mind that the paths that you input for the Phyre2 txt file, and the final output directory will have a different format than in Windows.</b>
## Next Steps
Next steps for the program include improvements in the abilities of the program as well as the user experience. One planned improvement to the program involves pairing it with or developing our own software to predict active sites in a protein based on the sequence. The current program is unable to consider that some residues may in fact be part of the active sites of the designed proteins, and thus, cannot be replaced without possible leading to a loss of function. This means that the user must perform this step themselves, which can once again be complex and difficult to carry out without errors.
For the user experience, a front-end will be developed for the program, either in the form of a website/webpage programmed using Django frameworks, or an executable graphical user interface (GUI) paired with the Python backend. This will likely improve the experience for a new user unfamiliar with computer paths, and executing programs in the command line, and will also allow for an easier visualization of the outputs and data generated by the program. Secondly, the program will be expanded to try and use a Phyre2-like server that is able to work in a shorter timespan, to avoid having the user to carry out the extra first step entirely. This once again can make the experience easier, as the user may only have to input their designed sequence and the target residues and parameters to select from.
## References
R. Adamczak, A. Porollo, J. Meller, Accurate Prediction of Solvent Accessibility Using Neural Networks Based Regression, Proteins: Structure, Function and Bioinformatics, 2004, 56:753-67.
R. Adamczak, A. Porollo, J. Meller, Combining Prediction of Secondary Structure and Solvent Accessibility in Proteins, Proteins: Structure, Function and Bioinformatics, 2005, 59:467-75
M.Wagner, R. Adamczak, A. Porollo, J. Meller, Linear regression models for solvent accessibility prediction in proteins, Journal of Computational Biology, 2005, 12:355-69.
A. Porollo, R. Adamczak, M. Wagner and J. Meller, Maximum Feasibility Approach for Consensus Classifiers: Applications to Protein Structure Prediction, CIRAS 2003 (conference proceedings).
Kelley LA et al. Nature Protocols 10, 845-858 (2015).
