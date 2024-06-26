# import sys
# import cv2
# import numpy as np

# from copy import deepcopy
# from scipy import ndimage
# from skimage import morphology, exposure
# from scipy.ndimage import binary_dilation

# sys.path.append("..")
# from segment_anything import sam_model_registry, SamPredictor

def init_sam():
	sam_checkpoint = "../weights/sam_vit_h_4b8939.pth"
	model_type = "vit_h"
	device = "cuda"
	sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
	sam.to(device=device)

def generate_masks(image, coordinates):
	sam = init_sam()
	predictor = SamPredictor(sam)
	predictor.set_image(image)
	all_masks = []
	for idx, coordinate in enumerate(coordinates):
		masks, scores, logits = predictor.predict(
			point_coords=np.array([coordinate]),
			point_labels=np.array([1]),
			multimask_output=True,
		)
		zero_mask = np.zeros_like(masks[0], dtype=np.uint8)
		for mask in masks:
			my_mask = mask.astype(np.uint8) * 255
			zero_mask += my_mask
		all_masks.append(zero_mask)
	return all_masks

def merge_masks(masks):
	merged_mask = np.zeros_like(masks[0], dtype=np.uint8)
	for mask in masks:
		merged_mask += mask
	return merged_mask

def fill_mask_holes(mask):
	iterations = 15
	dilated_mask = binary_dilation(mask, iterations=iterations) * 255
	filled_mask = ndimage.binary_fill_holes(dilated_mask)
	return filled_mask

def remove_isolated_mask_pixels(mask):
  input = deepcopy(mask)
  gray = input
  img = cv2.pyrDown(gray)
  _, threshed = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
  contours,_ = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cmax = max(contours, key = cv2.contourArea)
  epsilon = 0.009 * cv2.arcLength(cmax, True)
  approx = cv2.approxPolyDP(cmax, epsilon, True)
  cv2.drawContours(input, [approx], -1, (0, 255, 0), 3)
  width, height = gray.shape
  img = np.zeros( [width, height, 3],dtype=np.uint8 )
  cv2.fillPoly(img, pts =[cmax], color=(255,255,255))
  return img

def smooth_out_mask(mask):
  blur = cv2.GaussianBlur(mask, (0,0), sigmaX=3, sigmaY=3, borderType = cv2.BORDER_DEFAULT)
  result = exposure.rescale_intensity(blur, in_range=(127.5,255), out_range=(0,255))
  return result