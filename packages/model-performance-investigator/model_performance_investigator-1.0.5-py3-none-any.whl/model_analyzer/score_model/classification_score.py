__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.5'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

# Importing required packages
def import_required_package():
    try:
        global jaccard
        global confusion_matrix
        global f1_score
        global log_loss
        global auc
        global accuracy_score
        global balanced_accuracy_score
        global average_precision_score
        
        from sklearn.metrics import jaccard_score as jaccard
        from sklearn.metrics import f1_score as f1_score
        from sklearn.metrics import log_loss as log_loss
        from sklearn.metrics import roc_auc_score as auc
        from sklearn.metrics import accuracy_score as accuracy_score
        from sklearn.metrics import balanced_accuracy_score as balanced_accuracy_score
        from sklearn.metrics import average_precision_score as average_precision_score
        
        return 'imported'
    except Exception as  e:
        e = 'Kindly install or update Packages \n' + str(e)
        return e

# get_model_score function calculates the Score
def get_model_score(score_type, data, grid_predict):
    output = import_required_package()
    
    if output == 'imported':
        if score_type == 'jaccard':
            val = jaccard(data[1], grid_predict)
            score = {
                        "jaccard_score":val
                    }
        elif score_type == 'f1':
            val = f1_score(data[1], grid_predict)
            score = {
                        'f1_score': val
                    }
        elif score_type == 'neg_log_loss':
            val = log_loss(data[1], grid_predict)
            score = {
                        'neg_log_loss': val
                    }
        elif score_type == 'roc_auc':
            val = auc(data[1], grid_predict)
            score = {
                        'roc_auc_score': val
                    }
        elif score_type == 'accuracy':
            val = accuracy_score(data[1], grid_predict)
            score = {
                        'accuracy': val
                    }
        elif score_type == 'balanced_accuracy':
            val = balanced_accuracy_score(data[1], grid_predict)
            score = {
                        'balanced_accuracy': val
                    }
        elif score_type == 'average_precision':
            val = average_precision_score(data[1], grid_predict)
            score = {
                        'average_precision': val
                    }
        else:
            score = {score_type: 'Not a valid ScoreType'}
        
        return score
    else:
        return output