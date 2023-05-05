import os
import copy
import json
import cv2


root_image_path = "E:/road_damage_detection/dataset/annotated/checked/phase_1_all_img/train"
root_json_path = "E:/road_damage_detection/dataset/annotated/checked/phase_1_all_img/train.json"

augmented_image_save_path = "E:/road_damage_detection/dataset/annotated/checked/phase_1_all_img/augemented"
augmented_json_save_path = "E:/road_damage_detection/dataset/annotated/checked/phase_1_all_img/augmented_train.json"

CROP_SIZE = [100, 200]
CROP_SIDE = ["left", "right", "top", "bottom"]
ROTATE_DEG = [5, 10, 15]


def update_annotation_for_crop(image_name,img_height, img_width, json_data, size, side):
    regions = []
    raw_json = copy.deepcopy(json_data)
    for key, value in raw_json.items():
        if value['filename'] == image_name:
            regions = value['regions']
            for region in regions:
                shape_attributes = region['shape_attributes']
                
                if side == "left":
                    if shape_attributes['x'] < size:
                        shape_attributes['width'] -= (size - shape_attributes['x'])
                        shape_attributes['x'] = 0
                    else:
                        shape_attributes['x'] -= size

                elif side == 'right':
                    if shape_attributes['x'] + shape_attributes['width'] > (img_width - size):
                        shape_attributes['width'] = (img_width - size) - shape_attributes['x']
                        # print("------------>",(img_width - size) - shape_attributes['x'])
                elif side == 'top':
                    if shape_attributes['y'] < size:
                        shape_attributes['height'] -= (size - shape_attributes['y'])
                        shape_attributes['y'] = 0
                    else:
                        shape_attributes['y'] -= size
                elif side == 'bottom':
                    if shape_attributes['y'] + shape_attributes['height'] > (img_height - size):
                        shape_attributes['height'] = (img_height - size) - shape_attributes['y']
                # regions.append(region)
            break
        
    return regions
        

def create_vgg_annotation(up_json, regions, up_img_name):
    key = up_img_name + str(os.path.getsize(os.path.join(augmented_image_save_path, up_img_name)))
    file_data = {}
    file_data['filename'] = up_img_name
    file_data['size'] = os.path.getsize(os.path.join(augmented_image_save_path, up_img_name))
    file_data['regions'] = regions
    file_data['file_attributes'] = {}
    up_json[key] = file_data

    return up_json




def augment_image(crop_image, rotate_image, denoise_image):
    ##read json
    json_data = json.load(open(root_json_path))
    updated_json = {}

    ##read image
    for image_name in os.listdir(root_image_path):
        file_size = os.path.getsize(os.path.join(root_image_path, image_name))
        img = cv2.imread(os.path.join(root_image_path, image_name))
        print(image_name)
        augment_number = 1
        print(img.shape)
        if crop_image:
            for size in CROP_SIZE:
                for side in CROP_SIDE:
                    if side == "left":
                        aug_img = img[:,size:,:]
                        # print(aug_img.shape)
                        augmented_image_name = os.path.join(augmented_image_save_path, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        cv2.imwrite(augmented_image_name, aug_img)
                        regions = update_annotation_for_crop(image_name, img.shape[0], img.shape[1], json_data, size, 'left')
                        updated_json = create_vgg_annotation(updated_json, regions, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        augment_number += 1
                    elif side == "right":
                        aug_img = img[:, :-size, :]
                        # print(aug_img.shape)
                        augmented_image_name = os.path.join(augmented_image_save_path, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        cv2.imwrite(augmented_image_name, aug_img)
                        regions = update_annotation_for_crop(image_name, img.shape[0], img.shape[1], json_data, size, 'right')
                        updated_json = create_vgg_annotation(updated_json, regions, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        augment_number += 1
                    elif side == "top":
                        aug_img = img[size:, :, :]
                        # print(aug_img.shape)
                        augmented_image_name = os.path.join(augmented_image_save_path, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        cv2.imwrite(augmented_image_name, aug_img)
                        regions = update_annotation_for_crop(image_name, img.shape[0], img.shape[1], json_data, size, 'top')
                        updated_json = create_vgg_annotation(updated_json, regions, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        augment_number += 1
                    elif side == "bottom":
                        aug_img = img[:-size, :, :]
                        # print(aug_img.shape)
                        augmented_image_name = os.path.join(augmented_image_save_path, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        cv2.imwrite(augmented_image_name, aug_img)
                        regions = update_annotation_for_crop(image_name, img.shape[0], img.shape[1], json_data, size, 'bottom')
                        updated_json = create_vgg_annotation(updated_json, regions, image_name[:-4] + "_aug_" + str(augment_number) + ".jpg")
                        augment_number += 1
        # break
    return updated_json



if __name__ == '__main__':
    ##augmentation type
    crop_image = True
    rotate_image = False
    denoise_image = True
    updated_json = augment_image(crop_image, rotate_image, denoise_image)

    with open(augmented_json_save_path, 'wb') as f:
        f.write(json.dumps(updated_json, ensure_ascii=False).encode('utf-8'))