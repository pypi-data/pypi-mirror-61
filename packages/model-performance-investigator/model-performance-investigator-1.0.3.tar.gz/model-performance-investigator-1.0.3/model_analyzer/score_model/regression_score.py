__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.3'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

# Importing required packages
def import_required_package():
    try:
        global r2_score
        global explained_variance
        global max_error
        global mean_absolute_error
        global mean_squared_error
        global mean_squared_log_error
        global median_absolute_error
        global mean_poisson_deviance
        global mean_gamma_deviance
            
        from sklearn.metrics import r2_score as r2_score
        from sklearn.metrics import explained_variance_score as explained_variance
        from sklearn.metrics import max_error as max_error
        from sklearn.metrics import mean_absolute_error as mean_absolute_error
        from sklearn.metrics import mean_squared_error as mean_squared_error
        from sklearn.metrics import mean_squared_log_error as mean_squared_log_error
        from sklearn.metrics import median_absolute_error as median_absolute_error
        from sklearn.metrics import mean_poisson_deviance as mean_poisson_deviance
        from sklearn.metrics import mean_gamma_deviance as mean_gamma_deviance
        
        return 'imported'
    except Exception as  e:
        e = 'Kindly install or update Packages \n' + str(e)
        return e

# get_model_score function calculates the Score
def get_model_score(score_type, data, grid_predict):
    output = import_required_package()
    
    if output == 'imported':
        if score_type == 'r2':
            r2 = r2_score(data[1], grid_predict)
            adj_r2 = 1 - ((1 - r2) * ((data[0].shape[0] - 1) / 
                                                  (data[0].shape[0] - data[0].shape[1] - 1)))
            score = {
                        "r2"        :   r2,
                        "adj_r2"    :   adj_r2
                    }
        elif score_type == 'explained_variance':
            exp_variance = explained_variance(data[1], grid_predict)
            score = {
                    'explained_variance': exp_variance
                    }
        elif score_type == 'max_error':
            mx_error = max_error(data[1], grid_predict)
            score = {
                        'max_error': mx_error
                    }
        elif score_type == 'neg_mean_absolute_error':
            mn_absolute_error = mean_absolute_error(data[1], grid_predict)
            score = {
                        'mean_absolute_error': mn_absolute_error
                    }
        elif score_type == 'neg_mean_squared_error' or score_type == 'neg_root_mean_squared_error':
            mn_squared_error = mean_squared_error(data[1], grid_predict)
            score = {
                        'mean_squared_error': mn_squared_error
                    }
        elif score_type == 'neg_mean_squared_log_error':
            mn_squared_log_error = mean_squared_log_error(data[1], grid_predict)
            score = {
                        'mean_squared_log_error': mn_squared_log_error
                    }
        elif score_type == 'neg_median_absolute_error':
            med_absolute_error = median_absolute_error(data[1], grid_predict)
            score = {
                        'median_absolute_error': med_absolute_error
                    }
        elif score_type == 'neg_mean_poisson_deviance':
            mn_poisson_deviance = mean_poisson_deviance(data[1], grid_predict)
            score = {
                        'mean_poisson_deviance': mn_poisson_deviance
                    }
        elif score_type == 'neg_mean_gamma_deviance':
            mn_gamma_deviance = mean_gamma_deviance(data[1], grid_predict)
            score = {
                        'mn_gamma_deviance': mn_gamma_deviance
                    }
        else:
            score = {score_type: 'Not a valid ScoreType'}
        
        return score
    else:
        return output