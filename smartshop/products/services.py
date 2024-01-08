def get_product_photo(instance, file):
    return f'product/photo/{instance.name}/{file}'


def get_attachment_photo(instance, file):
    return f'product/attachments/photo/{instance.product}/{file}'


def get_product_video(instance, file):
    return f'product/video/{instance.name}/{file}'
