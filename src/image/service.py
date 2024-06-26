from fastapi import HTTPException

from .schema import ImageSchema
from .scraper import ImageScraper
from .repository import ImageRepository


class ImageService:
    def __init__(self, *, scraper: ImageScraper, repository: ImageRepository):
        self._scraper = scraper
        self._repository = repository

    def search_urls(self, search: str, size: int):
        if not (urls := self._scraper.get_urls(search, size)):
            raise HTTPException(500, "Could not find the URLs")

        images = [ImageSchema(search_term=search, url=url) for url in urls]

        self._repository.save_urls(images)
        return images

    def list(self):
        return self._repository.list()
