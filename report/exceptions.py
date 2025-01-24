from reusable.exceptions import CustomApiValidationError


class ReasonIsNotValid(CustomApiValidationError):
    default_detail: str = "دلیل معتبر نیست"
    default_code: str = "reason is not valid."


class ItemDoesNotExist(CustomApiValidationError):
    default_detail: str = "آیتمی با این شناسه وجود ندارد"
    default_code: str = "item is not exists."


class UserDoesNotExist(CustomApiValidationError):
    default_detail: str = "کاربری با این شناسه وجود ندارد"
    default_code: str = "user is not exists."
