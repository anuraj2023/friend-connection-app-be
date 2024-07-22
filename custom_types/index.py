from pydantic import BaseModel
from datetime import datetime
from typing import List

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreation(UserLogin):
    email: str
    first_name: str
    last_name: str 

class UserResponse(BaseModel):
    id: int
    username: str
    email: str 
    first_name: str
    last_name: str

class FriendRequestUpdateInput(BaseModel):
    friend_request_id: int
    status: str

class FriendshipCreateInput(BaseModel):
    user1_id: int
    user2_id: int

class StatusUpdateCreateUpdateInput(BaseModel):
    user_id: int
    status: str

class FriendStatus(BaseModel):
    id: int
    user_id: int
    status: str
    created_at: datetime

class SearchUserCriteria(BaseModel):
    query: str

class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str

class StatusUpdateResponse(BaseModel):
    id: int
    status: str
    created_at: str

class UserProfile(User):
    status_updates: List[StatusUpdateResponse]  

class FriendRequestResponse(BaseModel):
    id: int
    requestor_id: int
    recipient_id: int
    requestor_username: str
    requestor_email: str
    status: str
    created_at: datetime

class FriendRequestInput(BaseModel):
    requestor_id: int
    recipient_id: int

class Friend(BaseModel):
    id: int
    user1: User
    user2: User
    createdAt: datetime

class FriendDetailResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    status: str = None
    status_updated_at: str = None

class FriendListDetails(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    latest_status: str
    status_created_at: str
