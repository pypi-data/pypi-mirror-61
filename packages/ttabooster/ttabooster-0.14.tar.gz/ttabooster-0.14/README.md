# TTABoost - Boost Your  pre-trained Model With Test Time Augmentation Selection #

Test time augmentation selection for image detection and classification.

### Install ###
```bash
pip install ttabooster
```

### Usage example ###
```python
from ttabooster.TTABoost import TTABooster

model = load_model('pretrained-model.h5')  # Load any keras model
x_test, y_test = ...  # Load your validation set

AUGMENTATIONS_TEST = Compose([
    RandomSizedCrop((28, 28), 32, 32, w2h_ratio=1.0, interpolation=1, always_apply=False, p=1.0), 
    # Add your augmentations...
])

booster = TTABooster(model, batch_size=100, augmentations=AUGMENTATIONS_TEST)
booster.benchmark_results(x_test, y_test)
```
