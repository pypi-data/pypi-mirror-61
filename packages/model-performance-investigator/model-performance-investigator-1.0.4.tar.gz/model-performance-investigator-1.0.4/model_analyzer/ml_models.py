__author__  = 'Srikandan Raju, Sathish Anandha'
__copyright__ = 'Copyright (C) 2007 Free Software Foundation'
__license__ = 'GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007'
__version__ = '1.0.3'
__maintainer__ = 'Srikandan Raju, Sathish Anandha'

class MLPredictor(object):
    
    # Importing Required Packages
    def import_required_packages():
        try:
            global reg_class
            global classify_class
            global reg_plt
            
            from model_analyzer.models import regression as reg_class
            from model_analyzer.models import classification as classify_class
            from model_analyzer.plot import regression_plot as reg_plt
            
            return 'imported'
        except Exception as  e:
            e = 'Kindly install or update Packages \n ' + str(e)
            return e
            
    # predector is the main method for predicting the score of models
    def predector(prob_type, data, alg_type='default', score_type='default', 
                  tune_param='default', set_plot=True):
        
        import_status = MLPredictor.import_required_packages()
        
        try:
            if import_status == 'imported':
                prob_type = str(prob_type).lower()
                
                if prob_type == 'regression':
                    output = MLPredictor.regression(prob_type, data, alg_type, score_type, tune_param,
                                        set_plot)
                elif prob_type == 'classification':
                    output = MLPredictor.classification(prob_type, data, alg_type, score_type, tune_param,
                                            set_plot)
                else:
                    output = 'Not a valid Machine Learning Techniques'
                return output
            else:
                return import_status
        except Exception as e :
            return e
        
    # draw_plot is the main method of the Plotting
    def draw_plot(prob_type, datafarme, columns='default', plot_type='default'):
        import_status = MLPredictor.import_required_packages()
        
        try:
            if import_status == 'imported':
                prob_type = str(prob_type).lower()
                
                if prob_type == 'regression':
                    output = MLPredictor.regression_plot(datafarme, columns, plot_type)
                else:
                    output = 'This ML Technique is not supported to plot in this package'
                return output
            else:
                return import_status
        except Exception as e :
            return e
    
    # regression function used to call the regression class
    def regression(prob_type, data, alg_type, score_type, tune_param, set_plot):
        reg_main = reg_class.MainRegression
        if alg_type == 'default':
            alg_type = ['linear']
        if score_type == 'default':
            score_type = ['r2']
        try:
            output = reg_main.regression(prob_type, data, alg_type, score_type, tune_param, 
                                         reg_main, set_plot)
            
            return output
        except Exception as e :
            return e
    
    # classification function used to call the classification class
    def classification(prob_type, data, alg_type, score_type, tune_param, set_plot):
        class_main = classify_class.MainClassification
        if alg_type == 'default':
            alg_type = ['logistic']
        if score_type == 'default':
            score_type = ['confusion_matrix']
        try:
            output = class_main.classification(prob_type, data, alg_type, score_type, tune_param, 
                                         class_main, set_plot)
            return output
        except Exception as e :
            return e
    
    
    # regression_plot function used to call the regression_plot file
    def regression_plot(datafarme, columns, plot_type):
        reg_main = reg_plt.MainRegressionPlot
        if plot_type == 'default':
            plot_type = 'hist'
        if columns == 'default':
            columns = 'All'
        try:
            output = reg_main.regression_plot(datafarme, columns, plot_type, reg_main)
            return output
        except Exception as e :
            return e
        