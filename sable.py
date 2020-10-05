"""
This program receives a sample sequence, and submits a request to the SABLE
webserver to get a secondary structure and residue surface area prediction

Author: Akshaj Darbar
Date: 2020-09-27
"""

#Import Python Modules
import requests
import re
import time

def main_function(sequence):
  """This function submits the request to the SABLE webserver, gets the results
  and outputs it to the main.py program"""

  #URL of webserver form
  url = 'http://sable.cchmc.org/cgi-bin/sable_server_July2003.cgi'
  #Data to be submitted to webserver
  data = {'seqName': 'solvent_accessibility_pred',
          'txtSeq': sequence,
          'SA': 'SA',
          'SS': 'SS',
          'version': 'sable2'}

  #Post request
  r = requests.post(url, data=data)

  #Get url to check status of the prediction server
  status_url = find_status_url(r.text)
  
  #Check status of predictions
  status = requests.get(status_url)
  status_complete = False   #Initialize variable with incomplete status

  #If request is not initially in the queue
  if ('Your request is in the queue with the following status' not in status.text):
    status_complete = True
  #Check the status of the submission 9 times - 18 minutes maximum
  checks = 0
  while (checks <= 8 and not status_complete):
    #Wait 2 minutes before checking again
    time.sleep(120)
    checks += 1
    status = requests.get(status_url)
    if ('Your request is in the queue with the following status'
        not in status.text):
      status_complete = True

  #If the analysis is complete
  if (status_complete):
    #Get URL for final Polyview Results page
    result_URL = find_results_url(status.text)
    #Request results from Polyview
    result = requests.get(result_URL)
    #Get RSA and Secondary Structure predictions
    RSA_prediction = find_RSA_prediction(result.text)
    SS_prediction = find_SS_prediction(result.text)
    #Return predictions to main.py program
    return SS_prediction, RSA_prediction
  else:
    return "ERROR - SABLE TOOK TOO LONG TO RESPOND"

def find_status_url(text):
  """This function finds the url for the status page"""
  submission_substring = '<a href='
  i = find_substring(text, submission_substring) + 1
  status_url = ""
  while (text[i] != '\"'):
    status_url += text[i]
    i += 1
  return status_url

def find_results_url(text):
  """This function finds the URL for the Polyview results page"""
  results_substring = ';URL='
  i = find_substring(text, results_substring)
  results_url = ""
  while (text[i] != '\"'):
    results_url += text[i]
    i += 1
  return results_url

def find_RSA_prediction(text):
  """This function reads the Polyview code to find the RSA predictions"""
  RSA_substring = '<input type=\"hidden\" name=\"seaSeq\" value=\"'
  i = find_substring(text, RSA_substring)
  RSA_pred = ""
  while (text[i] != '\"'):
    RSA_pred += text[i]
    i += 1
  return RSA_pred

def find_SS_prediction(text):
  """This function reads the Polyview code to find the SS predictions"""
  SS_substring = '<input type=\"hidden\" name=\"ssSeq\" value=\"'
  i = find_substring(text, SS_substring)
  SS_pred = ""
  while (text[i] != '\"'):
    SS_pred += text[i]
    i += 1
  return SS_pred

def find_substring(text, substring):
  """This function finds the target substring, and its position in
  a long string of text"""
  matches = re.finditer(substring, text)
  matches_positions = [match.start() for match in matches]
  n = int(matches_positions[0]) + len(substring)
  return n
