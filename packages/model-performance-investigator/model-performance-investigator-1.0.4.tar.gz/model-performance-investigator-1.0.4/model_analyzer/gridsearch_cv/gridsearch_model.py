__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.3'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

# Importing required packages
def import_required_package():
    try:
        global grid_cv
        global reg_score_class
        global classify_score_class
        global reg_plt
        
        
        from sklearn.model_selection import GridSearchCV as grid_cv
        from model_analyzer.score_model import regression_score as reg_score_class
        from model_analyzer.score_model import classification_score as classify_score_class
        from model_analyzer.plot import regression_plot as reg_plt
        
        return 'imported'
    
    except Exception as e:
        e = 'Kindly install or update Packages \n ' + str(e)
        return e

# gridsearch_cv function runs the GridSearchCV
def gridsearch_cv(model, tune_param, score_type, data, prob, set_plotting, 
                  current_model):
    output = import_required_package()
    
    if output == 'imported':
        try:
            grid_search = grid_cv(estimator = model, 
                                param_grid = tune_param, scoring = score_type, 
                                n_jobs = -1, cv = 10, verbose = 3)
            grid_search.fit(data[0], data[1])
            grid_predict = grid_search.predict(data[2])
            score = ''
            if prob == 'regression':
                score = reg_score_class.get_model_score(score_type, data, grid_predict)
            elif  prob == 'classification':     
                score = classify_score_class.get_model_score(score_type, data, grid_predict)
            
            plot_status = ''
            try:
                if prob == 'regression' and set_plotting == True:
                    reg_main = reg_plt.MainRegressionPlot
                    plot_status = reg_main.draw_resud_plot(data[1], grid_predict, current_model)
                elif prob == 'classification' and set_plotting == True:
                    plot_status = 'Currently it supports Residual Plot for Regression'
                else:
                    plot_status = 'Plotting is OFF'
            except Exception as e:
                plot_status = e
            
            return score, str(grid_search.best_score_), str(grid_search.best_params_), plot_status
        except Exception as e:
            return e
    else:
        return output