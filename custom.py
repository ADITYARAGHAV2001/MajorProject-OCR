# custom.py
import json
import cv2
from pathlib import Path
from htr_pipeline import read_page, DetectorConfig, LineClusteringConfig, ReaderConfig, PrefixTree

# Load configuration and word list
with open('data/config.json') as f:
    sample_config = json.load(f)

with open('data/words_alpha.txt') as f:
    word_list = [w.strip().upper() for w in f.readlines()]
prefix_tree = PrefixTree(word_list)

def perform_ocr(image_path):
    img_filename = Path(image_path)
    decoder = 'word_beam_search'
    print(f'Reading file {img_filename} with decoder {decoder}')

    # Read image
    img = cv2.imread(str(img_filename), cv2.IMREAD_GRAYSCALE)
    scale = sample_config[img_filename.stem]['scale'] if img_filename.stem in sample_config else 1
    margin = sample_config[img_filename.name]['margin'] if img_filename.name in sample_config else 0
    read_lines = read_page(img,
                            detector_config=DetectorConfig(scale=scale, margin=margin),
                            line_clustering_config=LineClusteringConfig(min_words_per_line=2),
                            reader_config=ReaderConfig(decoder=decoder, prefix_tree=prefix_tree))

    # Extract text from OCR result
    processed_text = ''
    for read_line in read_lines:
        processed_text += ' '.join(read_word.text for read_word in read_line) + '\n'
    
    return processed_text
