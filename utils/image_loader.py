import cv2
import glob
import os

class ImageLoader: 
    def __init__(self, images_dir='./images'):
        self.images_dir = images_dir
        self.images = {}
        
    def load_images(self, resize_specs=None):
        """
        Загружает изображения и применяет resize согласно спецификации
        
        :param resize_specs: словарь с параметрами resize в формате 
                            {'имя_файла': (width, height), ...}
        """
        # Стандартные параметры resize если не переданы свои
        if resize_specs is None:
            resize_specs = {
                'blue_red': (250, 100),
                'green_red': (250, 100),
                'blue': (100, 100),
                'red': (100, 100),
                'green': (100, 100)
            }
        
        for name, size in resize_specs.items():
            # Формируем путь к файлу
            path_pattern = os.path.join(self.images_dir, f'{name}.png')
            files = glob.glob(path_pattern)
            
            if not files:
                raise FileNotFoundError(f'Не найден файл: {path_pattern}')
            
            # Загружаем и обрабатываем изображение
            img = cv2.imread(files[0])
            if img is None:
                raise ValueError(f'Не удалось загрузить изображение: {files[0]}')
                
            self.images[name] = cv2.resize(img, size)
        
        return self.images