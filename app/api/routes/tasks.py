from fastapi import APIRouter, BackgroundTasks

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


def write_log(
    message: str,
) -> None:
    with open(
        "background.log",
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            f"{message}\n"
        )


@router.post("/log")
async def create_background_log(
    background_tasks: BackgroundTasks,
) -> dict[str, str]:

    background_tasks.add_task(
        write_log,
        "Background task executed",
    )

    return {
        "status": "accepted"
    }