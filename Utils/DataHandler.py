import pickle
import io
import json
import functools
import time
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import random
from itertools import islice
import urllib.parse

class DataHandler():
    def __init__(self):
        """
        Instantiate this class, and then pass params for what we want to do
        - source: pointer, roomworld
        - level: cleaned, processed
        - type: rounds, responses, object
        - duplication: none, rise-style, research-style
        """
        pass

    def cleanData(self, rawData):
        """
        Run the process to take the downloaded data and clean it per-participant
        Inputs:
            - rawData: A JSON file. See docs for required keys and structure.
        Returns:
            - cleanData: The raw data structured for more convenient analysis. See docs for keys and structure.
        """
        cleanData = {}
        for user in rawData:
            # pk = user['id']
            # user = userAll['fields']
            tmp = {
                'pk' : user['id'],
                'userId' : urllib.parse.quote(user['userId']),
                'rawData' : json.loads(user['rawData']),
                'sdata' : None,
                'edata' : user['edata'],
                'parameters' : user['parameters'],
                'totalAttempts' : None,
                'completed' : user['completeAttempt'],
                'lastCompletedRound' : None,
                'lastTrialGame' : None,
                'finalRooms' : [],
                'userIP' : user['userIP'],
                'urlParameters' : user['urlParameters'],
                'timestamps' : [],
                'timeCreated' : user['timeCreated'],
                'lastModified' : user['lastModified']
            }
            # Check how many attempts the user has had
            tmp['totalAttempts'] = len(tmp['rawData'])
            # Store timestamp/s
            tmp['timestamps'] = list(tmp['rawData'].keys())
            # If it's one, check if it's complete
            if tmp['totalAttempts'] == 1:
                # Get the attempt timestamp
                timestamp = list(tmp['rawData'].keys())[0]
            elif tmp['totalAttempts'] > 1:
                # For multiple attempts, find the occurence with the highest number of completed trial_layouts
                indAttempts = [] # individual attempts
                for i in range(tmp['totalAttempts']):
                    # Get the sdata for this timestamp, and get the length of the expt_index array
                    try:
                        attNum = len(json.loads(tmp['rawData'][tmp['timestamps'][i]]['sdata'])['expt_index'])
                        indAttempts.append(attNum)
                    except:
                        indAttempts.append(0)
                # Get the index of the value with the greatest magnitude
                timestamp = tmp['timestamps'][np.argmax(indAttempts)]
                
            # Use the timestamp to add sdata to tmp
            try:
                tmp['sdata'] = json.loads(tmp['rawData'][timestamp]['sdata'])
            except:
                if tmp['rawData'][timestamp]['sdata'] == None or len(tmp['rawData'][timestamp]['sdata']) == 0:
                    tmp['sdata'] = None
            if tmp['sdata'] != None:
                # Check if complete by:
                #    - trial_layout == 92 or
                #    - trial_game == 80
                # if len(Counter(tmp['sdata']['trial_layout']).keys()) >= 92:
                if max(np.array(tmp['sdata']['trial_game'], dtype=np.float64)) >= 80:
                    tmp['completed'] = True
                    tmp['lastCompletedRound'] = len(tmp['sdata']['trial_game'])
                else:
                    tmp['completed'] = False
                    tmp['lastCompletedRound'] = len(Counter(tmp['sdata']['trial_layout']).keys())
                # Store how many trial_games they've seen
                tmp['lastTrialGame'] = int(tmp['sdata']['trial_game'][-1])
            else:
                tmp['completed'] = False
                tmp['lastCompletedRound'] = 0
                
            cleanData[tmp['pk']] = tmp
        self.cleanData = cleanData
        self.cleanData_df = pd.DataFrame.from_dict(cleanData, orient="index")
        print("Dataset ready.")
        
    def deduplicate(self, path, style):
        """
        Deduplicate the data based on some parameters - none, rise-style, research-style

        Inputs:
            - path (str) : The filepath to where the duplicates.csv data is kept. Must be a csv.
        """
        # Read in duplicates from the filepath provided
        assert path.endswith(".csv"), "Expected path to be to a CSV file."
        try:
            duplicates = pd.read_csv(path)
        except:
            raise FileExistsError(f"Unable to find duplicate file at location: {path}")

        # Parse format in lower case
        style = style.lower()
        # Check for allowed style types
        assert style in ["None", None, "research", "rise", "all"], f"Unrecognised style for deduplication: {style} - allowed types are None, RISE, research, all. See docs for more information."
        self.style = style

        # create a ref to the clean data dataframe
        clean_df = self.cleanData_df
        # Make a list of riseId : [userIds] that contains single-players, and duplicate players lists
        counts = Counter(duplicates["USER_ID"])
        # map riseId to [userIds]
        ids = {id : list(duplicates.loc[duplicates["USER_ID"] == id]["ID"]) for id in counts}
        # Get only duplicate users
        duplicateHashes = {i : ids[i] for i in ids if len(ids[i]) >= 2}
        print(f"# Unique players: {len(ids)} -- # of those who repeated: {len(duplicateHashes)}")

        riseAttempts = [] # the first complete if available - if not, the first incomplete
        researchAttempts = [] # the first attempt available of any type
        allAttempts = [] # for debugging, not important
        # for each attempt made by one individual, check if they completed
        mapping = []
        # Loops over all riseId : serverId mappings, not just duplicates
        for attempt in ids:
            # Get a df for just this participant
            repeats = clean_df.loc[clean_df["userId"].isin(ids[attempt])]
            # Create a df that contains any completes, or empty if none found
            completes = repeats.loc[repeats["completed"] == True]
            # Error mitigation
            if (len(repeats) == 0):
                continue
            if len(completes) == 0:
                # no completed attempts, take just the first attempt
                firstTimestamp = min(list(repeats["timeCreated"]))
                # Stores the hashed ID associated with this attempt
                riseAttempts.append(list(repeats.loc[repeats["timeCreated"] == firstTimestamp]["userId"])[0])
            elif len(completes) == 1:
                # if 1 complete attempt - NB: this could be in any time position, not necessarily first attempted
                riseAttempts.append(list(completes["userId"])[0])
            else:
                # if multiple complete attempts found - take the first for rise
                firstTimestamp = min(list(completes["timeCreated"]))
                riseAttempts.append(list(completes.loc[completes["timeCreated"] == firstTimestamp]["userId"])[0])

            # For research purposes, we want to take only the very first attempt
            firstTimestamp = min(list(repeats["timeCreated"]))
            tmp = repeats.loc[repeats["timeCreated"] == firstTimestamp]["userId"]

            researchAttempts.append(list(tmp)[0])
            allAttempts.append(ids[attempt])

        if style == "rise":
            # keep only the rise ones in cleanData
            clean_df = clean_df.loc[clean_df["userId"].isin(riseAttempts)]
        elif style == "research":
            # keep only the research ones in cleanData
            clean_df = clean_df.loc[clean_df["userId"].isin(researchAttempts)]
        
        return clean_df

    def getRounds(self):
        """
        Process the clean data into round-level data
        """
        pass

    def getResponses(self):
        """
        Process the clean data into response-level data
        """
        pass

    def getConcepts(self):
        """
        Process the clean data into concept-level data
        """
        pass

    def save(self):
        """
        Wrapper to save an object as csv
        """
        pass

    def load(self):
        """
        Wrapper to load a file from disk
        """
        pass