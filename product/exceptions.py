from django.conf import settings

from reusable.exceptions import CustomApiValidationError


class NoFileProvidedException(CustomApiValidationError):
    default_detail: str = "ارسال فایل تصویر الزامی است"
    default_code: str = "no file provided."


class FileSizeExceedMaxSizeException(CustomApiValidationError):
    default_detail: str = (
        f" اندازه حجم فایل نباید بیشتر از{settings.IMAGE_MAX_SIZE_MB}باشد "
    )
    default_code: str = "no file provided."


class InvalidFileTypeException(CustomApiValidationError):
    default_detail: str = f" فایل تصویر نامعتبر است. لطفا از ارسال فایل با پسوند‌های غیر از{settings.ALLOWED_IMAGE_TYPES}خودداری نمائید "
    default_code: str = "invalid file type."


class ImageNotFoundException(CustomApiValidationError):
    default_detail: str = "تصویر مورد نظر یافت نشد"
    default_code: str = "image not found."


class ItemNotFoundException(CustomApiValidationError):
    default_detail: str = "آیتم مورد نظر یافت نشد"
    default_code: str = "item not found."


class InvalidTitleException(CustomApiValidationError):
    default_detail: str = "عنوان نامعتبر است"
    default_code: str = "invalid title."


class CategoryDoesNotExistException(CustomApiValidationError):
    default_detail: str = "دسته‌بندی با این شناسه وجود ندارد"
    default_code: str = "category does not exist."


class InvalidPriceException(CustomApiValidationError):
    default_detail: str = "قیمت نامعتبر است"
    default_code: str = "invalid price."


class InvalidBannerException(CustomApiValidationError):
    default_detail: str = "بنر نامعتبر است"
    default_code: str = "invalid banner."


class SellerUserIsRequiredException(CustomApiValidationError):
    default_detail: str = "برای ایجاد یک آیتم، مشخص بودن فروشنده الزامی است"
    default_code: str = "seller user is required."
