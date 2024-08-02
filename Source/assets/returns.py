import dataclasses


class base_type:
    pass


@dataclasses.dataclass
class ret_none(base_type):
    error: str | None = None


@dataclasses.dataclass
class ret_data(base_type):
    data: bytes


@dataclasses.dataclass
class ret_redirect(base_type):
    url: str


def construct(data: bytes | None = None, redirect_url: str | None = None) -> base_type:
    if redirect_url is not None:
        return ret_redirect(redirect_url)
    elif data is not None:
        return ret_data(data)
    return ret_none()
