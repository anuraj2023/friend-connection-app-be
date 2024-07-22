from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from db import prisma
from custom_types.index import FriendRequestInput, FriendRequestResponse, FriendRequestUpdateInput, FriendshipCreateInput, FriendStatus

router = APIRouter()

@router.post("/friend/request/")
async def create_friend_request(request_data: FriendRequestInput):
    created_request = await prisma.friendrequest.create(
        data={
            "requestor_id": request_data.requestor_id,
            "recipient_id": request_data.recipient_id,
            "status": "pending",
            "created_at": datetime.utcnow()
        }
    )
    return created_request

@router.get("/friend/requests", response_model=List[FriendRequestResponse])
async def read_friend_requests_by_user_id(user_id: int = Query(..., title="User ID")):
    friend_requests = await prisma.friendrequest.find_many(
        where={
            "recipient_id": user_id,
            "status": "pending"
        },
        include={
            "requestor": True
        }
    )
    
    friend_requests_response = [
        {
            "id": fr.id,
            "requestor_id": fr.requestor_id,
            "recipient_id": fr.recipient_id,
            "requestor_username": fr.requestor.username,
            "requestor_email": fr.requestor.email,
            "requestor_first_name": fr.requestor.first_name,
            "requestor_last_name": fr.requestor.last_name,
            "status": fr.status,
            "created_at": str(fr.created_at)
        }
        for fr in friend_requests
    ]
    
    return friend_requests_response

@router.put("/friend/request/action")
async def update_friend_request(friend_request_update: FriendRequestUpdateInput):
    try:
        updated_request = await prisma.friendrequest.update(
            where={"id": friend_request_update.friend_request_id},
            data={"status": friend_request_update.status}
        )
        
        if not updated_request:
            raise HTTPException(status_code=404, detail="Friend request not found")
        
        if friend_request_update.status.lower() == 'accept':
            existing_friendship = await prisma.friend.find_first(
                where={
                    "OR": [
                        {"AND": [
                            {"user1_id": updated_request.requestor_id},
                            {"user2_id": updated_request.recipient_id}
                        ]},
                        {"AND": [
                            {"user1_id": updated_request.recipient_id},
                            {"user2_id": updated_request.requestor_id}
                        ]}
                    ]
                }
            )
            
            if not existing_friendship:
                new_friendship = await prisma.friend.create(
                    data={
                        "user1_id": updated_request.requestor_id,
                        "user2_id": updated_request.recipient_id
                    }
                )
        
        return updated_request

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")
