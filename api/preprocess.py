#画像の前処理を行う　画像サイズのリサイズ（preparationでも行っている）、色の標準化

from torchvision import models, transforms

def image_to_tensor(image):
    class Transform():
        """画像サイズのリサイズ、色情報の標準化"""
        def __init__(self, resize, mean, std):
            self.transform = transforms.Compose([
                transforms.Resize(resize),
                transforms.CenterCrop(resize),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ])

        def __call__(self, img):
            return self.transform(img)

    resize = 224
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)
    transform = Transform(resize, mean, std)
    img_transformed = transform(image)
    return img_transformed