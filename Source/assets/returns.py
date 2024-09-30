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
class ret_relocate(base_type):
    url: str


def construct(
    data: bytes | None = None,
    redirect_url: str | None = None,
    error: str | None = None,
) -> base_type:
    if data is not None:
        return ret_data(data)
    elif redirect_url is not None:
        return ret_relocate(redirect_url)
    elif error is not None:
        return ret_none(error)
    return ret_none()
