import cv2
from typing import Union
import numpy as np
from mltu.utils.text_utils import ctc_decoder
from mltu.inferenceModel import OnnxInferenceModel
from mltu.transformers import ImageResizer

class HTR(OnnxInferenceModel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.char_list = '\'3.FR20JWIe8CyBowxTV5rgOYQ,ipPcqDGnMAK(Eb6)fH:"9LlUt;jsz m4&1#kZ-adNhvu7!S?'
        self.char_list: Union[str, list]
        
    # scan the image using pre trained onnx model and output the text
    def scan(self,image_path):
        image = cv2.imread(image_path)
        image: np.ndarray
        image = ImageResizer.resize_maintaining_aspect_ratio(image, *self.input_shapes[0][1:3][::-1])
        image = np.expand_dims(image, axis=0).astype(np.float32)
        predict = self.model.run(self.output_names, {self.input_names[0]: image})[0]
        result = ctc_decoder(predict, self.char_list)[0]
        return result
    



# htr_pipeline package is needed
# it can be installed from https://github.com/githubharald/HTRPipeline/blob/master/README.md
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig
class HTR_page_reader:

    def scan(self, image_path):
        result = ''
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        read_lines = read_page(img, DetectorConfig(scale=0.4, margin=5), line_clustering_config=LineClusteringConfig(min_words_per_line=2))
        for read_line in read_lines:
            result += ' '.join(read_word.text for read_word in read_line) + "\n"
        return result




