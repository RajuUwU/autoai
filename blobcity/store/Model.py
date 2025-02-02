# Copyright 2021 BlobCity, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pickle
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
from blobcity.code_gen import code_generator
import yaml
"""
Python file consists of Class Model to initialize/store and retrive data associated to trained machine learning model.
"""
class Model:
    params=dict()
    featureList=[]
    model=None
    metrics=dict()
    yamldata=None
    feature_importance_=dict()
    plot_data=None
    def __init__(self):
        self.params=dict()
        self.featureList=[]
        self.model=None
        self.metrics=dict()
        self.yamldata=None
        self.feature_importance_=dict()
        self.plot_data=None
        

    def predict(self,test):
        """
        param1: self
        param2: 2D Array
        return: List/Array

        Function returns List/Array for predicted value from the trained model.
        """
        result=self.model.predict(test)
        return result

    def parameters(self):
        """
        return: Dictionary

        Function returns dictionary consisting of tuned parameters value for the trained model.
        """
        return self.params

    def features(self):
        """
        return: List/Array

        Function returns List of features used by model to train. This is also used to recognise the features to be passed as input into the predict function.
        """
        return self.featureList

    def save(self, path_pref='./'):
        """
        param: Path Prefix or Entire Path. Supported formats are .pkl and .h5. Default is .pkl
        returns: Final filepath of stored serialized file

        Function saves the model and its weights serially and returns the filepath where it is saved.
        """
        path_components = path_pref.split('.')
        if len(path_components)<=2:
            extension = path_components[1]
        else:
            extension = path_components[2]

        if extension == '/':
            final_path = os.path.join(path_pref, 'autoaimodel.pkl')
            pickle.dump(self, open(final_path, 'wb'))
            print("The model is stored at {}".format(final_path))
            return final_path

        elif extension == 'pkl':
            final_path = path_pref
            pickle.dump(self, open(final_path, 'wb'))
            print("The model is stored at {}".format(final_path))
            return final_path

        elif extension == 'h5':
            final_path = path_pref
            try:
                self.model.save(final_path)
                print("The model is stored at {}".format(final_path))
                return final_path
            except:
                raise TypeError("Your model is not a Keras model of type .h5. Try .pkl extension.")

        else:
            raise TypeError(f"{extension} file type must be .pkl or .h5")


    def stats(self):
        """
        Function to print/log/display all the metrics associated with problem type for the selected trained model. Usally used to check the effectiveness of training, or to assess the model fit. 
        """
        print ("\nMetrics on trained data:\n{:<10} {:<10}".format('METRIC', 'VALUE'))
        for key, value in self.metrics.items():
            print ("{:<10} {:<10}".format(key, value))

    def spill(self,filepath=None,doc=None):
        """
        param1: string : Filepath and format of generated file to store. either .py or .ipynb
        param2: boolean :  Whether generate code along with documentation.

        Function calls generator functions to generate source code for the AutoAI Procedure
        """
        data=self.yamldata
        code_generator(data,filepath,doc)

    def generate_yaml(self,path=None):
        """
        param1: string : File path to store .yaml file,if not specified store in current directory with `Process.yaml`
        
        Function generated and create YAML configuration file for the complete AutoAI procedures.
        """
        if path!=None:
            extension = os.path.splitext(path)[1]
            filepath=path
        else:
            filepath = './Process.yaml'
            extension=".yaml"
        if extension in [".yaml",".yml"]:
            with open(filepath, 'w') as file:
                yaml.dump(self.yamldata, file,sort_keys=False)
        else:
            raise TypeError(f"{extension} file type must be .yml or .yaml")

    def plot_feature_importance(self):
        val=self.feature_importance_
        if(val!=None):
            val=dict(sorted(val.items(), key=lambda item: item[1],reverse=False))
            plt.figure(figsize = (12, 6))
            plt.barh(range(len(val)), list(val.values()), align='center')
            plt.yticks(range(len(val)),list(val.keys()))
            plt.show()
        else:
            print("Feature importance not available for dataset with less then 2 columns") 
