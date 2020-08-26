#!/usr/bin/env python
# coding: utf-8

# In[34]:


get_ipython().run_line_magic('pylab', 'inline')
import numpy as np
import pandas as pd
import scipy 
import sys
import warnings
warnings.filterwarnings('ignore')


# In[35]:


# load results from 'home_team_prediction.ipynb' and 'away_team_prediction.ipynb'
df_home = pd.read_excel('C:\Users\vishn\Documents\Spring Semester Courses\Termination Project-SSIE 598 Fall 2020\Github Codes\df_both_seasons_home.xlsx')
df_away = pd.read_excel('C:\Users\vishn\Documents\Spring Semester Courses\Termination Project-SSIE 598 Fall 2020\Github Codes\df_both_seasons_away.xlsx')


# In[36]:


{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Populating the interactive namespace from numpy and matplotlib\n"
     ]
    }
   ],
   "source": [
    "%pylab inline\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import scipy \n",
    "import sys\n",
    "import bookie_package as bp\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "# load results from 'home_team_prediction.ipynb' and 'away_team_prediction.ipynb'\n",
    "df_home = pd.read_excel('df_both_seasons_home.xlsx')\n",
    "df_away = pd.read_excel('df_both_seasons_away.xlsx')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "cols_to_use = df_home.columns.difference(df_away.columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_both = pd.merge(df_away, df_home[cols_to_use], left_index=True, right_index=True, how='outer')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "del df_both['Unnamed: 0']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "# create predicted goal differences subtracting predicted home and away goals from each other and vice vers\n",
    "df_both['pred_HTGDIFF'] = df_both['FTHG'] - df_both['FTAG']\n",
    "df_both['pred_ATGDIFF'] = df_both['FTAG'] - df_both['FTHG']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_both.rename(columns={\"HTGDIFF\": \"test_HTGDIFF\", \"ATGDIFF\": \"test_ATGDIFF\", 'FTHG': 'pred_FTHG', 'FTAG':'pred_FTAG'}, inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_both = df_both.reindex(columns = ['Day', 'Month', 'Year', 'HomeTeam', 'AwayTeam', 'pred_FTHG', 'pred_FTAG',\n",
    "       'test_HTGDIFF', 'pred_HTGDIFF', 'test_ATGDIFF', 'pred_ATGDIFF', 'AVGATGDIFF', 'AVGFTAG','AVGFTHG', 'AVGHTGDIFF'])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_both.to_excel('both.xlsx')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "MAE: 1.46 Goals.\n",
      "Accuracy: 23.17 %.\n"
     ]
    }
   ],
   "source": [
    "# counting where error = 0 which means prediction and test data are the same = success\n",
    "# then dividing it by the length of all errors\n",
    "errors = abs(df_both['pred_HTGDIFF'] - df_both['test_HTGDIFF'])\n",
    "accuracy = (errors==0).sum() / len(errors) * 100\n",
    "print('MAE:', round(np.mean(errors),2), 'Goals.')\n",
    "print('Accuracy:', round(accuracy, 2), '%.')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [],
   "source": [
    "total_wins=(df_both[\"pred_HTGDIFF\"] > 0).sum()\n",
    "total_draw=(df_both[\"pred_HTGDIFF\"] == 0).sum()\n",
    "total_loss=(df_both[\"pred_HTGDIFF\"] < 0).sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [],
   "source": [
    "common_win = ((df_both[\"test_HTGDIFF\"] > 0) & (df_both[\"pred_HTGDIFF\"] > 0)).sum()\n",
    "common_draw = ((df_both[\"test_HTGDIFF\"] == 0) & (df_both[\"pred_HTGDIFF\"] == 0)).sum()\n",
    "common_lost = ((df_both[\"test_HTGDIFF\"] < 0) & (df_both[\"pred_HTGDIFF\"] < 0)).sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Correct Prediction Total: 50.8 %\n",
      "Correct Prediction Share Wins: 58.91 %\n",
      "Correct Prediction Share Draws: 29.24 %\n",
      "Correct Prediction Share Lost: 63.48 %\n"
     ]
    }
   ],
   "source": [
    "print('Correct Prediction Total: {} %'.format(np.round(((common_win+common_draw+common_lost)/df_both.shape[0]) * 100,2)))\n",
    "print('Correct Prediction Share Wins: {} %'.format(np.round((common_win /total_wins)*100, 2)))\n",
    "print('Correct Prediction Share Draws: {} %'.format(np.round((common_draw / total_draw)*100,2)))\n",
    "print('Correct Prediction Share Lost: {} %'.format(np.round((common_lost / total_loss)*100,2)))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}


# In[ ]:




