from datetime import datetime, timezone, timedelta
import uuid

import qrcode


IST = timezone(timedelta(hours=5, minutes=30))

def date_today() -> datetime.date:
    return datetime.now().date()

def time_now_ist() -> datetime:
    return datetime.now(IST)

def gen_community_id() -> str:
    """Generate a new UUID string for community ID."""
    return str(uuid.uuid4())    

def gen_unique_id() -> str:
    """Generate a new UUID string for unique user ID."""
    return str(uuid.uuid4())


def gen_user_qr(membership_id: int) -> qrcode.image.base.BaseImage:
    """Generate a QR code image for a uunique user ID."""
    img = qrcode.make(membership_id)
    return img


def validate_scanned_qr(scanned_id: str) -> bool:
    """Validate that the scanned ID is a canonical UUID4 string."""
    try:
        parsed_uuid = uuid.UUID(scanned_id, version=4)
        return str(parsed_uuid) == scanned_id
    except (ValueError, TypeError):
        return False

