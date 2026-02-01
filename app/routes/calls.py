from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import AsyncSessionLocal
from app.models import Call, CallState, Packet
from app.schemas import PacketIn
import asyncio

router = APIRouter(prefix="/v1/call", tags=["calls"])

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/stream/{call_id}", status_code=202)
async def ingest_packet(
    call_id: str,
    packet: PacketIn,
    db: AsyncSession = Depends(get_db)
):
    # ensure call exists
    result = await db.execute(select(Call).where(Call.id == call_id))
    call = result.scalar_one_or_none()

    if call is None:
        call = Call(id=call_id, state=CallState.IN_PROGRESS)
        db.add(call)
        await db.commit()

    # get last sequence
    last_seq_result = await db.execute(
        select(func.max(Packet.sequence)).where(Packet.call_id == call_id)
    )
    last_seq = last_seq_result.scalar()

    if last_seq is not None and packet.sequence != last_seq + 1:
        print(f"WARNING: missing packet for call {call_id}")

    db.add(
        Packet(
            call_id=call_id,
            sequence=packet.sequence,
            data=packet.data,
            timestamp=packet.timestamp
        )
    )
    await db.commit()

    return {"status": "accepted"}

@router.post("/complete/{call_id}", status_code=202)
async def complete_call(
    call_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Call).where(Call.id == call_id))
    call = result.scalar_one_or_none()

    if call is None:
        return {"error": "call not found"}

    call.state = CallState.COMPLETED
    await db.commit()

    background_tasks.add_task(process_ai_stub, call_id)

    return {"status": "call completed"}

async def process_ai_stub(call_id: str):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Call).where(Call.id == call_id))
        call = result.scalar_one()

        call.state = CallState.PROCESSING_AI
        await db.commit()

    await asyncio.sleep(1)
    print(f"AI processing started for call {call_id}")
