import numpy as np
import mrcfile
import imageio
from PIL import Image

def image_read(image_path, region=None):
    image_path = str(image_path)
    if image_path.endswith(("jpg", "png")):
        if not is_single_channel(image_path):
            raise Exception("Not supported image format. Movie files are not supported")
            return None
        img = imageio.imread(image_path, pilmode="L", as_gray=True)
        img = np.squeeze(img)
        img = img.astype(np.uint8)
    elif image_path.endswith(("tiff", "tif")):
        img = imageio.imread(image_path)
        img = np.squeeze(img)
       # img = np.flipud(img)
    elif image_path.endswith("mrc"):
        if not is_single_channel(image_path):
            raise Exception("Not supported image format. Movie files are not supported")
            return None

        img = read_mrc(image_path)


    else:
        raise Exception("Not supported image format: " + image_path)
    # OpenCV has problems with some datatypes
    if np.issubdtype(img.dtype, np.uint32):
        img = img.astype(dtype=np.float64)

    if np.issubdtype(img.dtype, np.float16):
        img = img.astype(dtype=np.float32)

    if np.issubdtype(img.dtype, np.uint16):
        img = img.astype(dtype=np.float32)

    #img = np.max(img) - 1 - img + np.min(img)

    if region is not None:
        return img[region[1], region[0]]
    return img

def is_single_channel(image_path):
    if image_path.endswith(("jpg", "png", "tiff", "tif")):
        im = Image.open(image_path)
        if len(im.size) > 2:
            return False

    if image_path.endswith("mrc"):
        with mrcfile.open(image_path, permissive=True) as mrc:
            if mrc.header.nz > 1:
                return False

    return True

def read_mrc(image_path):
    with mrcfile.open(image_path, permissive=True) as mrc:
        mrc_image_data = np.copy(mrc.data)
    mrc_image_data = np.squeeze(mrc_image_data)
    mrc_image_data = np.flipud(mrc_image_data)

    return mrc_image_data

