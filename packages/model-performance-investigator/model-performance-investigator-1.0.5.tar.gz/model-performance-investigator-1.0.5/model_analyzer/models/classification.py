__author__ = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.5'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'


class MainClassification(object):
    
    # Importing required packages
    def import_required_packages():
        try:
            global pd
            global np
            global s_scale
            global grid_class
            global mk_pipeline
            
            import pandas as pd
            import numpy as np
            from sklearn.pipeline import make_pipeline as mk_pipeline
            
            from model_analyzer.gridsearch_cv import gridsearch_model as grid_class
            
            return 'imported'
        except Exception as  e:
            e = 'Kindly install or update Packages \n ' + str(e)
            return e
        
    # classification function identifies the Model Type
    def classification(prob_type, data, alg_type, score_type, tune_param, class_main,
                       set_plot):
        global prob
        global set_plotting
        global current_model
        
        prob = prob_type
        set_plotting = set_plot
        
        try:
            import_status = class_main.import_required_packages()
        
            main_dataframe = pd.DataFrame(columns=['Model', 'Score_Type', 
                                                   'Predicted_Score',
                                                   'Best_Score',
                                                   'Best_Parameter',
                                                   'Plot_Status',
                                                   'Error'])
            result_data = []
            list_data = []
            list_data = data.copy()
            if import_status == 'imported':
                for model in  alg_type:
                    current_model = model
                    if model == 'logistic':
                        output = class_main.logistic(list_data, score_type, 
                                                                        tune_param, 
                                                                        class_main)
                    elif model == 'decision_tree':
                        output = class_main.decision_tree(list_data, score_type, 
                                                                        tune_param, 
                                                                        class_main)
                    elif model == 'random_forest':
                        output = class_main.random_forest(list_data, score_type, 
                                                                        tune_param, 
                                                                        class_main)
                    elif model == 'naive_bayes':
                        output = class_main.naive_bayes(list_data, score_type, 
                                                                        tune_param, 
                                                                        class_main)
                    elif model == 'svc':
                        output = class_main.svc(list_data, score_type, tune_param, 
                                                                        class_main)
                    elif model == 'xgb_classifier':
                        output = class_main.xgb_classifier(list_data, score_type, 
                                                                        tune_param, 
                                                                        class_main)
                    else:
                        output = [{
                            'Model':model, 
                            'Score_Type':'',
                            'Predicted_Score':'',
                            'Best_Score':'',
                            'Best_Parameter':'',
                            'Plot_Status':'',
                            'Error': 'Not a Valid Model'
                            }]
                    
                    if isinstance(output, list):
                        for out_data in output:
                            result_data.append(out_data)
                main_dataframe = main_dataframe.append(result_data, ignore_index=True)
                    
                return main_dataframe
            else:
                return import_status
        except Exception as e:
            return e
            
        
    # Logisitic Classification Model
    def logistic(data, score_types, tune_param, class_main):
        try:
            from sklearn.linear_model import LogisticRegression
            log_mod = LogisticRegression()
            
            grid_tune_param = {
                              'penalty':['l1', 'l2', 'elasticnet'],
                              'C':[0.001, 0.01, 0.1, 1, 10, 100, 1000],
                              'solver':['newton-cg', 'lbfgs', 'sag', 'saga'],
                              'max_iter':[100, 300, 500]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('logistic')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, log_mod, tune_param, data,
                                              'Logistic Classifier')
            return output
        except Exception as e:
            return e
        
    # Decision Tree Classification Model
    def decision_tree(data, score_types, tune_param, class_main):
        try:
            from sklearn.tree import DecisionTreeClassifier
            dec_mod = DecisionTreeClassifier()
            
            grid_tune_param = {
                              'criterion':['gini', 'entropy'],
                              'max_depth':[2, 8, 20, 40],
                              'min_samples_split':[2, 8, 20, 40],
                              'min_samples_leaf':[1, 2, 8, 20, 40],
                              'max_features': ['auto', 'sqrt', 'log2'],
                              'max_leaf_nodes': [2, 8, 20, 40]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('decision_tree')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, dec_mod, tune_param, data,
                                              'Decision Tree')
            return output
        except Exception as e:
            return e
    
    
    # Random Forest Classification Model
    def random_forest(data, score_types, tune_param, class_main):
        try:
            from sklearn.ensemble import RandomForestClassifier
            rand_mod = RandomForestClassifier()
            
            grid_tune_param = {
                              'n_estimators':[100, 300, 500, 1000],
                              'criterion':['gini', 'entropy'],
                              'max_depth':[2, 8, 20, 40],
                              'min_samples_split':[2, 8, 20, 40],
                              'min_samples_leaf':[1, 2, 8, 20, 40],
                              'max_features': ['auto', 'sqrt', 'log2'],
                              'max_leaf_nodes': [2, 8, 20, 40]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('random_forest')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, rand_mod, tune_param, data,
                                              'Random Forest')
            return output
        except Exception as e:
            return e
    
    # Naive Bayes Classification Model
    def naive_bayes(data, score_types, tune_param, class_main):
        try:
            from sklearn.naive_bayes import GaussianNB
            gauss_mod = GaussianNB()
            
            grid_tune_param = {
                              'var_smoothing':[1e-15, 1e-10, 1e-8, 1e-3, 1e-2, 
                                       1, 5, 10, 15, 20, 40, 50,
                                       85, 100, 300, 500, 1000]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('naive_bayes')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, gauss_mod, tune_param, data,
                                              'Naive Bayes')
            return output
        except Exception as e:
            return e
        
    # SVC Classification Model
    def svc(data, score_types, tune_param, class_main):
        try:
            from sklearn.svm import SVC
            svc_mod = SVC()
            
            grid_tune_param = {
                              'C':[0.001, 0.01, 0.1, 1, 10, 100, 1000],
                              'kernel':['poly', 'rbf', 'linear', 'sigmoid'],
                              'degree':[3, 5, 8]
                            }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('svc')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, svc_mod, tune_param, data,
                                              'SVC')
            return output
        except Exception as e:
            return e
        
        
    # XGB Classifier Classification Model
    def xgb_classifier(data, score_types, tune_param, class_main):
        try:
            from xgboost import XGBClassifier
            xgb_mod = XGBClassifier()
            
            grid_tune_param = {
                          'booster':['gbtree', 'dart'] ,
                          'gamma':[ 0.0, 0.1, 0.2],
                          'n_estimators':[100, 300, 500, 1000],
                          'max_depth':[2, 8, 20, 40]
                    }
            if tune_param == 'default':
                tune_param = grid_tune_param
            else:
                tune_param = tune_param.get('xgb_regressor')
                if tune_param is None or tune_param == 'default':
                    tune_param = grid_tune_param
            output = class_main.get_grid_score(score_types, xgb_mod, tune_param, data,
                                              'XGB Classifier')
            return output
        except Exception as e:
            return e
        
    # get_grid_score function calls the gridsearch_cv to get the Grid Search Result
    def get_grid_score(score_types, model, tune_param, data, model_name):
        try:
            score_list = []
            for score_type in score_types:
                score, best_score, best_param, plot_status = grid_class.gridsearch_cv(model,
                                                                                      tune_param,
                                                                                      score_type,
                                                                                      data,
                                                                                      prob,
                                                                                      set_plotting,
                                                                                      current_model)
                output = {
                            'Model'                    :   model_name,
                            'Score_Type'               :   score_type,
                            'Predicted_Score'          :   score,
                            'Best_Score'               :   best_score,
                            'Best_Parameter'           :   best_param,
                            'Plot_Status'              :   plot_status,
                            'Error'                    :   ''
                        }
                score_list.append(output)
            return score_list   
        except Exception as e:
            error = [{
                'Model':model, 
                'Score_Type':'',
                'Predicted_Score':'',
                'Best_Score':'',
                'Best_Parameter':'',
                'Plot_Status':'',
                'Error': str(e)
                }]
            return error
        