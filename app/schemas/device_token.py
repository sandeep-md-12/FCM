from pydantic import BaseModel


class RegisterTokenRequest(BaseModel):

    user_id: int

    fcm_token: str

class UnregisterTokenRequest(BaseModel):

    user_id: int

    fcm_token: str

from pydantic import ConfigDict


class DeviceTokenResponse(BaseModel):

    id: int

    user_id: int

    fcm_token: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )