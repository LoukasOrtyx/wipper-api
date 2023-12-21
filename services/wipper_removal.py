import cv2
import torch
import numpy as np
import gradio as gr

from PIL import Image
from scipy.ndimage import binary_dilation
from diffusers import StableDiffusionInpaintPipeline
from services.wipper_recognition import *

def init_inpaint_pipe():
	device = "cuda"
	model_path = "runwayml/stable-diffusion-inpainting"
	pipe = StableDiffusionInpaintPipeline.from_pretrained(
		model_path,
		torch_dtype=torch.float16,
	).to(device)
	return pipe

def inpaint_image(image, mask, prompt, negative_prompt, dilation_it=1):
	pipe = init_inpaint_pipe()
	image = Image.fromarray(image)
	mask = Image.fromarray(mask)
	resized_img = image.resize((512, 512))
	resized_mask = mask.resize((512, 512))
	generator = torch.Generator(device="cuda").manual_seed(0)
	guidance_scale=7.5
	num_samples = 1
	result = pipe(
		prompt=prompt,
		negative_prompt=negative_prompt,
		image=resized_img,
		mask_image=resized_mask,
		guidance_scale=guidance_scale,
		generator=generator,
		num_images_per_prompt=num_samples,
	).images[0]
	resized_inpaint = result.resize(image.size)
	overlayed = overlay_empty_background(np.array(image), mask, np.array(resized_inpaint), dilation_it)
	return overlayed

def overlay_empty_background(original_image, mask, inpainted_image, iterations=1):
  mask = binary_dilation(mask, iterations=iterations) * 255
  original_image[mask > 0] = 0
  inpainted_image[mask < 255] = 0
  return original_image + inpainted_image

def remove_isolated_mask_pixels(mask):
  gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
  result = cv2.pyrDown(gray)
  _, threshed = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
  contours,_ = cv2.findContours(threshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cmax = max(contours, key = cv2.contourArea)
  epsilon = 0.009 * cv2.arcLength(cmax, True)
  approx = cv2.approxPolyDP(cmax, epsilon, True)
  cv2.drawContours(mask, [approx], -1, (0, 255, 0), 3)
  width, height = gray.shape
  result = np.zeros([width, height],dtype=np.uint8)
  cv2.fillPoly(result, pts =[cmax], color=(255,255))
  return result