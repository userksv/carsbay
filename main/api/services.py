from main.models import PostImage

def update_post_images():
    # Create new images if there are
    # Delete images if requested
    # Save 
    ...


def fetch_post_images(pk):
    return PostImage.objects.filter(post=pk)