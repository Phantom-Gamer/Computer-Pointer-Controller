from openvino.inference_engine import IENetwork, IECore
import numpy as np
import cv2
import logging

class Head_Pose_Estimation_Model:
    '''
    This is a class for the operation of Head Pose Estimation Model
    '''
    
    def __init__(self, model_name, device='CPU', extensions=None, threshold=0.6):
        '''
        This will initiate Head Pose Estimation Model class object
        '''
        self.logger=logging.getLogger('hp')
        self.model_structure=model_name
        self.model_weights=model_name.replace('.xml','.bin')
        self.device_name=device
        self.threshold=threshold
        try:
            self.core = IECore()
            self.model=IENetwork(self.model_structure, self.model_weights)
        except Exception as e:
            self.logger.error("Error While Initilizing Head Pose Estimation Model Class"+str(e))
            raise ValueError("Could not Initialise the network. Have you enterred the correct model path?")
        self.input_name=next(iter(self.model.inputs))
        self.input_shape=self.model.inputs[self.input_name].shape
        self.output_name=next(iter(self.model.outputs))
        self.output_shape=self.model.outputs[self.output_name].shape

    def load_model(self):
        '''
        This method with load model using IECore object
        return loaded model
        '''
        try:
            self.net = self.core.load_network(network=self.model, device_name=self.device_name, num_requests=1)
        except Exception as e:
            self.logger.error("Error While Loading Head Pose Estimation Model"+str(e)) 

    def predict(self, image):
        '''
        This method will take image as a input and 
        does all the preprocessing, postprocessing
        '''
        try:
            p_image=self.preprocess_input(image)
            outputs=self.net.infer({self.input_name:p_image})
            f_output=self.preprocess_output(outputs)
        except Exception as e:
            self.logger.error("Error While prediction in Head Pose Estimation Model"+str(e))
        return f_output
        
    def preprocess_output(self, outputs):
        '''
        Model output is a dictionary having below three arguments:
             "angle_y_fc", shape: [1, 1] - Estimated yaw (in degrees).
             "angle_p_fc", shape: [1, 1] - Estimated pitch (in degrees).
             "angle_r_fc", shape: [1, 1] - Estimated roll (in degrees).
        '''
        final_output=[]
        try:
            final_output.append(outputs['angle_y_fc'][0][0])
            final_output.append(outputs['angle_p_fc'][0][0])
            final_output.append(outputs['angle_r_fc'][0][0])
        except Exception as e:
            self.logger.error("Error While preprocessing output in Head Pose Estimation Model"+str(e)) 
        return final_output

    def preprocess_input(self, image):
        '''
        Input: image
        Description: We have done basic preprocessing steps
            1. Resizing image according to the model input shape
            2. Transpose of image to change the channels of image
            3. Reshape image
        Return: Preprocessed image
        '''
        try:
            image = cv2.resize(image, (self.input_shape[3], self.input_shape[2]))
            image = image.transpose((2,0,1))
            image = image.reshape(1, *image.shape)
        except Exception as e:
            self.logger.error("Error While preprocessing Image in Head Pose Estimation Model"+str(e)) 
        return image